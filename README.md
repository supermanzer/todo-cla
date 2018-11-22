# TODO-CLA
----
A command line application for cataloging TODO comments in project directories.

This application is intended to facilitate communication between teams of developers regarding what needs to be done as well as a means for a single developer to keep track of what needs to be completed.  When called, it will generate a TODO.md document which builds a list of all TODO comments in project files as well as the file and line where the TODO comment was found.

## Usage

The project root directory, file extensions to be used in determining which files to scan, which files to ignore, and directories to ignore can all be specified at the command line when calling the function.  Alternatively, if a config file is present in the root project directory, these parameters can be specified there.  A sample config file is incuded in this project.

----
### Examples

#### Example command
    todo_catalog --file_ext=('.py', '.js', '.css', '.html') --dirs_to_ignore = ['node_modules']

#### Example Config File
    [SETTINGS]
    file_ext = .py, .js

    files_to_ignore = setup.cfg, setup.py

    dirs_to_ignore = node_modules


####  Example Output
    * #1) test_file.py line 1 - (test@example.com) This should be found 
