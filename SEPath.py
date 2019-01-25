import sublime
import sublime_plugin
import subprocess
from sys import platform as platform
import os

class GetFullPath(sublime_plugin.TextCommand):
  def __init__(self, view):
    self.view = view
    self.settings = sublime.load_settings("SEPath.sublime-settings")
    self.base_directory_key = self.settings.get("base_directory_key", ":/")
    self.base_directories = self.settings.get("base_directories", [])
    self.base_folder_name = self.settings.get("base_folder_name", '')
    self.flags = sublime.CLASS_PUNCTUATION_START | sublime.CLASS_PUNCTUATION_END

  def rfind_folder(self, directory, base_folder_name):
    path = directory
    while os.path.basename(path) != base_folder_name:
      if path == os.path.dirname(path):
        sublime.status_message('No "{0}" folder discovered \
          in "{1}"'.format(base_folder_name, directory))
        return None
      path = os.path.dirname(path)
    return path

  def get_selected_path(self, point, left_seps, right_seps):
    line = self.view.line(point)
    point -= line.begin()
    selected_row = self.view.substr(line)
    l = -1
    for i in range(point - 1, 0, -1):
      if selected_row[i] in left_seps:
        l = i
        break
    r = -1 
    for i in range(point, len(selected_row)):
      if selected_row[i] in right_seps:
        r = i
        break
    if l == -1 or r == -1:
      return None
    return selected_row[l + 1 : r]

  def get_base_directory(self):
    result_path = ''
    cur_path = os.path.dirname(self.view.file_name())
    for path in self.base_directories:
      if cur_path.find(path) == 0 and result_path < path:
        result_path = path
    if result_path == '':
      if self.base_folder_name == '':
        return None
      else:
        return self.rfind_folder(cur_path, self.base_folder_name)
    if type (self.base_directories) is dict:
      if self.base_directories[result_path] != '':
        result_path = self.base_directories[result_path]
    return result_path

  def run(self, edit, left_seps, right_seps):
    result_paths = []
    for region in self.view.sel():
      if not region.empty():
        continue
      if region is None:
        continue
      selected_path = self.get_selected_path(region.a, left_seps, right_seps)

      if selected_path is None:
        continue
      fn = self.view.file_name()
      if fn is None:
        self.view.run_command('save')
        continue
      if os.path.isabs(selected_path):
        sublime.status_message("path type: full path")
      elif selected_path.startswith(self.base_directory_key):
        sublime.status_message("path type: base path")
        selected_path = selected_path[len(self.base_directory_key):]
        base_directory = self.get_base_directory()
        if base_directory is None:
          sublime.message_dialog('Couldn\'t find base directory for "' + \
            selected_path + '"')
          continue
        selected_path = os.path.join(base_directory, selected_path)
      else:
        sublime.status_message("path type: relative path")
        current_directory = os.path.dirname(fn)
        selected_path = os.path.join(current_directory, selected_path)
      result_paths.append(selected_path)
    return result_paths

def open_in_file_manager(path):
  if platform == "win32":
    os.startfile(path)
  elif platform == "darwin":
    subprocess.Popen(["open", path])
  else:
    subprocess.Popen(["xdg-open", path])


class OpenCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    get_full_path = GetFullPath(self.view)
    paths = get_full_path.run(edit, '"', '"')
    for path in paths:
      if os.path.exists(path):
        if os.path.isdir(path):
          open_in_file_manager(path)
        else:
          self.view.window().open_file(path)
      else:
        sublime.message_dialog('Path not found: "' + path + '"')


class OpenInFileManagerCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    get_full_path = GetFullPath(self.view)
    paths = get_full_path.run(edit, '"', '"/')
    for path in paths:
      if os.path.exists(path):
        if os.path.isfile(path):
          path = os.path.dirname(path)
        open_in_file_manager(path)
      else:
        sublime.status_message('Path not found: "' + path + '"')