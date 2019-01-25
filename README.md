# SEPath
This script allows you to quickly open file paths from the `sublime text 3` in the same place or in the file manager.

# Installation

Install this `sublime text 3` package via [Package Control]:
1. Through Command Palette <kbd>Ctrl(Cmd) + Shift + P</kbd> find `Package Control: Add Repository` and add `https://github.com/eudorokhov/SEPath` repository to it.

2. Through Command Palette <kbd>Ctrl(Cmd) + Shift + P</kbd> find `Package Control: Install Package` and install `SEPath` package.

# Usage

To open file or folder, click on the path and press <kbd>F5</kbd> key for Linux or Windows or through Command Palette <kbd>Ctrl(Cmd) + Shift + P</kbd> find `SEPath: Open`


To open specific path folder in the file manager, click on it and press <kbd>Ctrl + F5</kbd> keys for Linux or Windows or through Command Palette <kbd>Ctrl(Cmd) + Shift + P</kbd> find `SEPath: Open sub path folder`


For OS X, you can add your own shortcuts in `Preferences/Package Settings/SEPath/Key Bindings - User`.

### Key bindings template:

```
[
    {
      "keys": ["Your shortcut"], 
      "command": "open"
    },
    {
      "keys": ["Your shortcut"],
      "command": "open_in_file_manager"
    }
]
```

# Settings

Settings are accessed via the `Preferences/Package Settings/SEPath` or through Command Palette `Ctrl(Cmd) + Shift + P`. To find them, write `Preferences: SEPath Settings - User/Default` and click on it.

By default you can open only `full` and `relative` path.
For addition `base` path, you need to add `base_folder_name` or `base_directories` or all at once.

### 0. Settings template

```
{
	"base_directory_key" : ":/",
	"base_folder_name" : "data",
	"base_directories" : [

	]
}
```

### 1. base_directory_key (`"base_directory_key" : ":/"`)
The base directory key is a string that replaces a part of the full path. 

Let the full path of the file look like this: `/home/user/downloads/project/data/json/books.json`.
Replace the `/home/user/downloads/project/data` sub path with `:/`, where `:/` is the base directory key. The final path can be written as: `: /json/books.json`.

`root_replacement_key` by default is `:/`.

### 2. base_folder_name (`"base_folder_name" : "base folder name"`)
`base_folder_name` is the name of the folder that replaces the root. If the path of the current file does not contain one of the `base_directories`, then from the end of the current path, a folder with the `base folder name` will be searched. 
If a folder with this name is found, then in the path that was clicked, `base_directory_key` will be replaced with the full path to this folder.

### 3. base_directories [list] (`"base_directories" : [base directory]`)
These settings are used to create different 'base_directories' for different projects.
```
{
	"base_directory_key" : ":/"
	"base_directories": [
		"/home/user/project/data",
		"/home/user/project/build/testdata"
	]
}
```

### 4. base_directories [dict; not fully implemented] (`"base_directories" : {"path, which sub path will be replaced" : "base directory path"}`)
```
{
	"base_directory_key" : ":/"
	"base_directories": {
		"/home/user/project/data0" : "",
		"/home/user/project/data1" : "/home/user/project/data2"
	}
}
```

# License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/eudorokhov/SEPath/blob/master/LICENSE) file for details.