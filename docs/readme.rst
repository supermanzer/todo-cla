.. _readme:

============
TODO Catalog
============

A simple command line application to log TODO comments in a software project.

Description
============
This application traverses the directory of a project and reads all files with the specified extensions, logging all TOOO comments.
Files and directories to ignore can be specified either by a config file or when using the command.
This is recommended as it is surprising just how many Node modules and Python packages are littered with TODO comments.


Parameters
==========
The following parameters are available in the command line when invoking the command.

* ``-d, --dir`` - The root directory to scan for TODO comments. Defaults to current directory
* ``-f, --file_ext`` - The file extensions that should be scanned
* ``-fi, --files_to_ignore`` - The file names that should be ignored during scan
* ``-di, --dirs_to_ignore`` - The directories that should be ignored during scan
* ``-c, --config`` - The config file to read these parameters from.  Defaults to ``todo_config``


Examples
=========

This application can be used with all configuration parameters specified in the function call.::

    get_todo -f ".py, .js, .html" -fi "setup.py, nuxt.config.js" -di ".venv, node_modules"



Alternatively, all these parameters can be specified in a config file.  The default name is ``todo_config`` but that can be specified when the application is called.  The config file follows the specifications identified for the `Python configparser <https://docs.python.org/3/library/configparser.html>`_ ::

    #todo_config
    [DEFAULTS]
    file_ext = .py, .js, .html
    files_to_ignore = setup.py, tests.py,
    dirs_to_ignore = node_modules, .venv 

If not using the default filename ``todo_config`` then simply specify the config file when calling the function.::
    
    get_todo -c "my_special_config"


Usage
======

One place this function can be useful is in the pre-commit step of a `git hook <https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks>`_.  This will ensure that any TODO comments are logged and written to a ``TODO.md`` file upon commit. It is helpful to keep track of where you might be in a project if you have to take a break.  Just add the following two lines of code to ``.git/hooks/pre-commit``.  It can also be a useful place to specify parameters if you don't want one more config file in your project.::

    get_todo # Add additional parameters here if desired.

    git add TODO.md # Ensure we add the resultant TODO.md file to the commit