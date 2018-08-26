# todo_catalog.py
import click
import os
import sys
import re

@click.command()
@click.option('--dir', default=False, help='root directory')
@click.option('--file_ext', default=False, help='File extensions to scan')
@click.option('--files_to_ignore', default=[], help='Files to ignore while scanning for TODO comments.')
@click.option('--dirs_to_ignore', default=[], help='Directories to ignore while scanning for TODO comments.')
def find_todos(dir, file_ext, files_to_ignore, dirs_to_ignore):
    """
    A command line function for walking the directory of a project, scanning the code files, finding TODO statements, and building a catalogue of them. A directory can be passed as the first command line argument to initiate the process somewhere other than the current working directory.  It will create or overwrite a TODO.md document in the root folder.
    ARGS:
        dir - An optional root directory to start from.  If False, this is set to the current working directory.

        file_ext - A tuple of file extensions to pay attention to.

        files_to_ignore - An optional list of filenames to be ignored when compiling TODO comments.

        dirs_to_ignore - An optional list of directory names to ignore when compiling TODO comments <- VERY USEFUL FOR THINGS LIKE node_modules/ DIRS.

    ALTERNATIVE:
        If preferable, the file_ext, files_to_ignore, and dirs_to_ignore can be stored in files in the root directory. This function will check both visible and hidden (leading .) file names.

    EXAMPLE:
        todo_catalog --file_ext=('.py', '.js', '.css', '.html') --dirs_to_ignore = ['node_modules']
    """
    # Checking to see if a directory was passed in
    if dir:
        root = dir
    else:
        root = os.getcwd()

     # File extensions we will pay attention to.  -- THIS SHOULD BE REFACTORED ONCE WE CAN VERIFY PROPER FUNCTIONAITY
    if not file_ext:
        if os.path.isfile(os.path.join(root, 'file_ext')):
            with open(os.path.join(root,'file_ext')) as f:
                file_ext = f.readlines()
                file_ext = [x.strip() for x in file_ext if x[0] !='#']
        elif os.path.isfile(os.path.join(root, '.file_ext')):
            with open(os.path.join(root,'.file_ext')) as f:
                file_ext = f.readlines()
                file_ext = [x.strip() for x in file_ext if x[0] !='#']
        else:
            file_ext = ('.py', '.txt', '.php', '.js', '.css')

    if not files_to_ignore:
        if os.path.isfile(os.path.join(root, 'files_to_ignore')):
            with open(os.path.join(root,'files_to_ignore')) as f:
                files_to_ignore = f.readlines()
                files_to_ignore = [x.strip() for x in files_to_ignore if x[0] !='#']
        elif os.path.isfile(os.path.join(root, '.files_to_ignore')):
            with open(os.path.join(root,'.files_to_ignore')) as f:
                files_to_ignore = f.readlines()
                files_to_ignore = [x.strip() for x in files_to_ignore if x[0] !='#']

    if not dirs_to_ignore:
        if os.path.isfile(os.path.join(root, 'dirs_to_ignore')):
            with open(os.path.join(root,'dirs_to_ignore')) as f:
                dirs_to_ignore = f.readlines()
                dirs_to_ignore = [x.strip() for x in dirs_to_ignore if x[0] !='#']
        elif os.path.isfile(os.path.join(root, '.dirs_to_ignore')):
            with open(os.path.join(root,'.dirs_to_ignore')) as f:
                dirs_to_ignore = f.readlines()
                dirs_to_ignore = [x.strip() for x in dirs_to_ignore if x[0] !='#']

    #  Writing our TODO.md file
    td=open(os.path.join(root,'TODO.md'),'w+')

    # Walking our directory tree with a counter variable
    k=1
    for (dirname, dirs, files) in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in dirs_to_ignore]
        files[:] = [f for f in files if f not in files_to_ignore]
        for filename in files:
            if filename.endswith(file_ext):
                # We dont need to confuse collaborators by including those portions of the project path that are specific to the machine on which this is run.  So we truncate the print_file variable to only include file paths relative to the root directory.
                print_file=os.path.join(dirname,filename)
                print_file=print_file.replace(root+'/','')
                with open(os.path.join(dirname,filename),'r') as f:
                    for n, line in enumerate(f, 1):
                        if "TODO" in line:
                            mObj=re.match(r'.*TODO:*\s*(.*)',line)
                            out_text= "* #%i) %s line %i - %s \n" % (k,print_file,n,mObj.group(1))
                            td.write(out_text)
                            k+=1
