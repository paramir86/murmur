from tests import DATA_DIR
from murmur.register_files import enumerate_files, get_syncsafe, ID3
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


class TestGetSyncsafe(TestCase):
    def test_get_syncsafe(self):
        patterns = [
            ([0b11111111, 0b11111111, 0b11111111, 0b11111111], 268435455),
            ([0b00000000, 0b00000000, 0b00000000, 0b00000000], 0),
            ([0b00000000, 0b00000011, 0b01111111, 0b01111111], 65535),
        ]
        for in_data, out_data in patterns:
            with self.subTest():
                self.assertEqual(get_syncsafe(in_data), out_data)


class TestID3(TestCase):
    path = os.path.join(DATA_DIR, "id3v2.mp3")



    def test_header(self):
        id3v2 = ID3(self.path)
        self.assertEqual(id3v2.is_ID3v2, True)
        self.assertEqual(id3v2.tag_version, "ID3v2.3.0")
        self.assertEqual(id3v2.tag_size, 10426)

    def test_text_frame(self):
        id3v2 = ID3(self.path)
        self.assertEqual(id3v2.frames["TYER"], "2022")
        self.assertEqual(id3v2.frames["TIT2"], "test-title")
        self.assertEqual(id3v2.frames["TPE1"], "test-artist")

if __name__ == '__main__':
    unittest.main()
