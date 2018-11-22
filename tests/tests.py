from unittest import TestCase

import todo_catalog
import os

class TodoTestCase(TestCase):

  def setUp(self):
    # Creating the file we will scan
    test_file = open('test_file.py', 'w+')
      # Adding a TODO comment
    todo_comment = '# TODO (test@example.com) This should be found'
    test_file.write(todo_comment)
      # Closing our file
    test_file.close()

  def test_success(self):
    """
    This test should pass
    """
    # Ensuring we call our program as we intend it, from the command line.
    os.system('''todo_catalog --file_ext='.py' --files_to_ignore='todo_catalog.py, tests.py, setup.py' ''')
    self.assertTrue(os.path.isfile('TODO.md'))
    with open('TODO.md') as tdfile:
        self.assertTrue('This should be found' in tdfile.read())

  def test_fail(self):
    """
    This test represents improperly configured parameters
    """
    os.system('''todo_catalog --file_ext='.py' --files_to_ignore='todo_catalog.py, tests.py, setup.py' ''')
    # This will still be true
    self.assertTrue(os.path.isfile('TODO.md'))
    with open('TODO.md') as tdfile:
      # However, since we are only scanning .js files, we shouldn't
      # find our predfined comment.
        self.assertFalse('This should be found' in tdfile.read())

  def tearDown(self):
    os.remove('test_file.py')
    # os.remove('TODO.md')


if __name__ == '__main__':
    unittest.main()
