import setuptools

with open('README.md','r') as ld:
  long_description = ld.read()

setuptools.setup(
    name = 'todo_catalog',
    version = '0.1.4',
    description='A command line application used to generate a TDOD.md file for a given project.'
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/supermanzer/tools',
    author='C. Ryan Manzer',
    author_email='ryan.manzer@gmail.com',
    py_modules = ['todo_catalog'],
    install_requires = [
        'Click',
    ],
    entry_points = '''
        [console_scripts]
        todo_catalog=todo_catalog:find_todos
    '''
)
