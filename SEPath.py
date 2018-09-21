import sublime
import sublime_plugin
import os

class OpenSePathCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		self.settings = sublime.load_settings("SEPath.sublime-settings")
		default_data_path = self.settings.get("default_data_path", "none")
		flags = sublime.CLASS_PUNCTUATION_START | sublime.CLASS_PUNCTUATION_END
		for region in view.sel():
			line = view.substr(view.line(region))
			expanded_region = view.expand_by_class(region, flags, '"')
			file_path = view.substr(expanded_region)
			file_path = file_path.strip('"')
			file_path = file_path.strip(' ')

			if len(file_path) > len(line): return
			current_path = os.path.dirname(view.file_name())
			
			if file_path[0] == ':':
				file_path = file_path.lstrip(':')
				file_path = file_path.lstrip('/')
				print(default_data_path)
				if (default_data_path == "none"):
					while os.path.basename(current_path) != "data":
						if current_path == os.path.dirname(current_path):
							sublime.status_message("No 'data' folder discovered")
							return
						current_path = os.path.dirname(current_path)
				else:
					current_path = default_data_path
			file_path = os.path.join(current_path, file_path)
			if os.path.exists(file_path):
				view.window().open_file(file_path)
			else:
				sublime.status_message("No filename discovered: " + file_path)