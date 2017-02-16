import unittest
from randomAccessReader import RandomAccessReader, CsvRandomAccessReader
import os


class ReaderTest(unittest.TestCase):

    def test_text_file(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/test_file.csv"
        reader = RandomAccessReader(path)
        line = reader.get_lines(5)
        self.assertTrue('Learn Tons of Blogging Tips &Tricks' in line[0])

    def test_line_count(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/test_file.csv"
        reader = RandomAccessReader(path)
        self.assertTrue(reader.number_of_lines == 34)

    def test_multi_lines(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/test_file.csv"
        reader = RandomAccessReader(path)
        lines = reader.get_lines(3, 3)
        self.assertTrue(len(lines) == 3)
        self.assertTrue('Learn Tons of Blogging Tips &Tricks' in lines[-1])


class CsvReaderTest(unittest.TestCase):

    def test_csv(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/test_file.csv"
        reader = CsvRandomAccessReader(path)
        line = reader.get_line_dicts(5)
        self.assertTrue(line[0]["Description line 1"] == "A Simple, Easy-to-Follow Guide")