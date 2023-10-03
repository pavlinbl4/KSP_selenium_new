import os.path
import unittest

from Fee_in_last_month.create_report_file import create_report_file


class TestFileCreate(unittest.TestCase):

    def test_create_report_file(self):
        path_to_file = create_report_file('May', '/Users/evgeniy/Adobe', 'Pupkin')

        self.assertTrue(os.path.isfile(path_to_file))

        os.remove(path_to_file)


if __name__ == '__main__':
    unittest.main()
