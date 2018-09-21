## Installation

Install this sublime text 2/3 package via [Package Control] search for package: "[**SEPath**]

## Usage

To open file path under cursor:

- Linux: <kbd>F5</kbd>
- Windows: <kbd>F5</kbd>
- OS X: <kbd>cmd+e</kbd>

or through Command Palette <kbd>Ctrl+Shift+P</kbd> find "SEPath: Open file path under cursor"


## Default configuration

"default_data_path": "none"

There are two options to open  ":/some/path" path: 

- "none":
	The path to “data” folder will be found from the tail directory of the active file.
	If there is no such folder, you will receive  "No 'data' folder discovered" status message. 
	For example: 
		A json file has the path:
		 `/home/data/folder/data/folder/file.json`
		You click the path:
		 `:/some/path/file.json`
		The sublime text 3 then will try to open a file with the path:
		 `/home/data/folder/data/some/path/file.json`
		If such path doesn’t exist, you will receive the following status message: 
		 `No filename discovered: /home/data/folder/data/some/path/file.json`

- `/your/data/directory/absolute/path`:
	You have to enter the absolute path to the root folder that has the required files. 
	The path ":/some/path" will be added to the absolute path, e.g. 
	 `/your/data/directory/absolute/path/some/path`

## Settings

Settings are accessed via the `Preferences/Package Settings/SEPath`.
