from murmur.register_files import enumerate_files
from unittest import TestCase
import unittest
import os
import tempfile
import shutil


class TestEnumerateFiles(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file_1 = os.path.join(self.test_dir, "test_file_1.mp3")
        with open(self.test_file_1, 'w'): pass
        self.test_sub_dir = os.path.join(self.test_dir, "sub_dir")
        os.mkdir(self.test_sub_dir)
        self.test_file_2 = os.path.join(self.test_sub_dir, "test_file_2.mp3")
        with open(self.test_file_2, 'w'): pass
        self.test_file_3 = os.path.join(self.test_dir, "test_file_3.jpg")
        with open(self.test_file_3, 'w'): pass

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_enumerate_files(self):
        result = enumerate_files(self.test_dir)
        expect = [self.test_file_1, self.test_file_2]
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
