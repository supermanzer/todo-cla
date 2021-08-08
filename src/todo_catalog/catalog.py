"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = todo_catalog.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import os
import argparse
import logging
import re
import sys
import configparser

from todo_catalog import __version__

__author__ = "Ryan"
__copyright__ = "Ryan"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from todo_catalog.catalog import get_config`,
# when using this Python module as a library.

def get_config(args):
    """Return configuration parameters

    If both args and a config file are detected, the arg values will take priority

    Args:
        args (argparse.Namespace): An argparse Namespace of args passed at runtime

    Raises:
        Exception if config file provided but no DEFAULTS section is present

    Returns:
        dict: a dictionary of configuration parameters
    """
    # Creating default return dict with iterables where needed
    result = {
        "root": args.dir,
        'file_ext': [],
        'files_to_ignore': [],
        'dirs_to_ignore': []
    }
    # Assigning file-specified configurations
    if os.path.isfile(os.path.join(args.dir, args.config)):
        conf = configparser.ConfigParser()
        conf.read(os.path.join(args.dir, args.config))
        if 'DEFAULTS' not in conf.sections():
            raise Exception("DEFAULTS section required if config file is provided.")
        defaults = conf['DEFAULTS']
        result['file_ext'] = [f.strip()
                              for f in defaults.get('file_ext', '').split(',') if f]
        result['files_to_ignore'] = [f.strip()
                                     for f in defaults.get('files_to_ignore', '').split(',') if f]
        result['dirs_to_ignore'] = [f.strip()
                                    for f in defaults.get('dirs_to_ignore', '').split(',') if f]
    # Assinging command line args if provided. This also takes care of assigning values
    result['file_ext'] = args.file_ext.split(
        ',') if args.file_ext else result['file_ext']
    result['files_to_ignore'] = args.files_to_ignore.split(
        ',') if args.files_to_ignore else result['files_to_ignore']
    result['dirs_to_ignore'] = args.dirs_to_ignore.split(
        ',') if args.dirs_to_ignore else result['dirs_to_ignore']
    return result


def log_comment(td_file, file_name, line_n, comment):
    """Log TODO comment in markdown file

    Args:
        td_file (file_object): The markdown file open for writing
        file_name (str): A string indentifying the file in which the TODO comment was found
        line_n (int): Line number in file_name of TODO comment
        comment (str): The TODO comment text
    """
    template_str = "* 1. %s line %i - %s\n"
    text = template_str.format(file_name, line_n, comment)
    td_file.write(text)


def walk_dir(config):
    """Traverse directory to scan for TODO comments

    Args:
        config (dict): Configuration dictionary
    """

    with open(os.path.join(config['root'], 'TODO.md'), "w") as td:
        found = False
        for (root, dirs, files) in os.walk(config['root'], topdown=True):
            # Pruning the files and directories based on config
            dirs[:] = [d for d in dirs if d not in config['dirs_to_ignore']]
            files[:] = [f for f in files if f not in config['files_to_ignore']]
            files[:] = [f for f in files if f.endswith(tuple(config['file_ext']))]
            for filename in files:
                # Generating useful file name with nested directories but
                # without computer specific components (e.g /home/user)
                pfile = os.path.join(root, filename)
                pfile = pfile.replace(config['root'] + "/", "")
                with open(os.path.join(root, filename), "r") as f:
                    for n, line in enumerate(f, 1):
                        if "TODO" in line:
                            found = True
                            comment = re.match(r".*TODO:*\s*(.*)", line).group(1)
                            log_comment(td, pfile, n, comment)

        if not found:
            root = os.path.split(config['root'])[1]
            td.write("# No TODO Comments found in {}".format(root))
            print("""
                No TODO comments found.

                If you think this is incorrect, check configuration settings used.
            """)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Catalog TODO comments in project")
    # -- Generic CLA args --
    parser.add_argument(
        "--version",
        action="version",
        version="todo_catalog {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    # -- Application specific args --
    parser.add_argument(
        "-d",
        "--dir",
        default=os.getcwd(),
        help="Root directory for traversal. Defaults to current dir."
    )
    parser.add_argument(
        "-f",
        "--file_ext",
        default="",
        help="File extensions to scan, defaults to .py"
    )
    parser.add_argument(
        "-fi",
        "--files-to-ignore",
        default="",
        help="Files to ignore during scan"
    )
    parser.add_argument(
        "-di",
        "--dirs-to-ignore",
        default="",
        help="Directories to ignore during scan"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="todo_config",
        help="Specify a config file name in the root directory"
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug(args)
    config = get_config(args)
    _logger.debug(config)
    walk_dir(config)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m todo_catalog.skeleton 42
    #
    run()
