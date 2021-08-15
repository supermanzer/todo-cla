import os

# from todo_catalog.catalog import main

__author__ = "Ryan Manzer"
__copyright__ = "2021 Ryan Manzer"
__license__ = "MIT"

TODO_COMMENT = '# TODO (test@example.com) this comment should be found'


def make_file(filename):
    test_file = open(filename, 'w')

    test_file.write(TODO_COMMENT)

    test_file.close()


def remove_file(filename):
    os.remove(filename)
    os.remove('TODO.md')


def test_todo_found():
    make_file('testfile.py')

    os.system('get_todo -f ".py" -fi "setup.py"')

    assert os.path.isfile('TODO.md')

    with open('TODO.md') as f:
        assert TODO_COMMENT in f.read()

    remove_file()
