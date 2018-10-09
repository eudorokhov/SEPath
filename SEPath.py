import sublime
import sublime_plugin
import subprocess
from sys import platform as platform
import os

class GetFullPath(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.view = view
		self.settings = sublime.load_settings("SEPath.sublime-settings")
		self.root_replacement_key = self.settings.get("root_replacement_key", ":/")
		self.root_replacer = self.settings.get("root_replacer", "#data")	
		self.flags = sublime.CLASS_PUNCTUATION_START | sublime.CLASS_PUNCTUATION_END


	def get_selected_path(self, region):
		selected_row = self.view.substr(self.view.line(region))
		expanded_region = self.view.expand_by_class(region, self.flags, '"')
		file_path = self.view.substr(expanded_region)
		file_path = file_path.strip('"')
		file_path = file_path.strip(' ')		
		if len(file_path) >= len(selected_row):
			return None
		return file_path


	def rfind_folder(self, directory, folder):
		path = directory
		while os.path.basename(path) != folder:
			if path == os.path.dirname(path):
				sublime.status_message("No '{0}' folder discovered in '{1}'".format(folder, directory))
				return None
			path = os.path.dirname(path)
		return path


	def get_root_replacer_path(self):
		directory = os.path.dirname(self.view.file_name())
		if self.root_replacer[0] == '#':
			root_replacer = self.root_replacer[1:];
			return self.rfind_folder(directory, root_replacer)
		else:
			if not os.path.isabs(self.root_replacer):
				sublime.status_message("Bad 'root replacer' path: " + self.root_replacer)
				return None
			return self.root_replacer


	def run(self, edit):
		result_paths = []
		for region in self.view.sel():
			if region is None:
				continue
			file = self.get_selected_path(region);
			if file is None:
				continue
			directory = os.path.dirname(self.view.file_name())
			if not os.path.isabs(file):
				if file.startswith(self.root_replacement_key):
					sublime.status_message("path type: root replacer")
					
					file = file[len(self.root_replacement_key):]
					directory = self.get_root_replacer_path()
					if directory is None:
						continue;
				else:
					sublime.status_message("path type: relative path")
				file = os.path.join(directory, file)
			result_paths.append(file)
		return result_paths


class OpenInSubl3Command(sublime_plugin.TextCommand):
	def run(self, edit):
		get_full_path = GetFullPath(self.view)
		paths = get_full_path.run(edit)
		for path in paths:
			if os.path.exists(path):
				self.view.window().open_file(path)
			else:
				sublime.status_message("No filename discovered: " + path)
				print("No filename discovered: " + path)


class OpenInFileManagerCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		get_full_path = GetFullPath(self.view)
		paths = get_full_path.run(edit)
		for path in paths:
			path = os.path.dirname(path)
			if os.path.exists(path):
				print("platform: {0}".format(platform))
				if platform == "Windows":
					os.startfile(path)
				elif platform == "Darwin":
					subprocess.Popen(["open", path])
				else:
					subprocess.Popen(["xdg-open", path])
			else:
				sublime.status_message("No filename discovered: " + path)