
# TODO CATALOG



A simple command line application used to log TODO comments in a project


## Description
---

This application traverses the directory of a project and reads all files with the specified extensions, logging all TOOO comments.  
Files and directories to ignore can be specified either by a config file or when using the command.  
This is recommended as it is surprising just how many Node modules and Python packages are littered with TODO comments.

## Examples
---

Command with parameters specified at run-time


    get_todo -f ".py, .js, .hmtl" -di "node_modules, .venv", -fi "LICENSE.txt, README.md"


Example config file


    # todo_config
    [DEFAULTS]
    file_ext = .py, .js, .html

    files_to_ignore = config.js, setup.py

    dirs_to_ignore = node_modules, .venv



By default the application will look for the file ``todo_config`` in the root directory.  This filename can be changed with the ``-c`` or ``--config`` parameter.

## Usage
One place this code makes a lot of sense is in the pre-commit step of a ``git`` workflow. I find it useful to add the following lines to my ``pre-commit`` file in ``git/hooks`` for any repository in which I want to track TODO comments.


    # .git/hooks/pre-commit

    # Run the application (with optional configurations)
    get_todo # -f ".py, .js, .vue" -di "node_modules, .venv"

    # Add resulting TODO file to repo contents
    git add TODO.md


If you do not want to add one more config file to your project, they do get confusing after all, 
you can specify all your configuration options in the ``get_todo`` call here as shown in the commented section of the call.