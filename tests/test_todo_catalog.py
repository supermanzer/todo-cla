import os

# from todo_catalog.catalog import main

__author__ = "Ryan Manzer"
__copyright__ = "2021 Ryan Manzer"
__license__ = "MIT"

COMMENT = 'this comment should be found'
TODO_COMMENT = f'# TODO (test@example.com) {COMMENT}'


def make_file(filename):
    test_file = open(filename, 'w')

    test_file.write(TODO_COMMENT)

    test_file.close()


def remove_file(filename):
    os.remove(filename)
    os.remove('TODO.md')


def test_todo_found():
    filename = 'testfile.py'
    make_file(filename)

    os.system('get_todo -f ".py" -fi "setup.py" -di ".tox, .venv"')

    assert os.path.isfile('TODO.md')

    with open('TODO.md') as f:
        assert COMMENT in f.read()
        for line in f:
            assert '.py' in line

    remove_file(filename)
