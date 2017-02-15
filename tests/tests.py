import unittest
from randomAccessReader import RandomAccessReader, CsvRandomAccessReader
import os


class ReaderTest(unittest.TestCase):

    def test_text_file(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/test_file.csv"
        reader = RandomAccessReader(path)
        line = reader.get_line(5)
        self.assertTrue('Learn Tons of Blogging Tips &Tricks' in line)

    def test_line_count(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/test_file.csv"
        reader = RandomAccessReader(path)
        self.assertTrue(reader.number_of_lines == 34)


class CsvReaderTest(unittest.TestCase):

    def test_csv(self):
        path = os.path.dirname(os.path.abspath(__file__)) + "/test_file.csv"
        reader = CsvRandomAccessReader(path)
        line = reader.get_line_dict(5)
        self.assertTrue(line["Description line 1"] == "A Simple, Easy-to-Follow Guide")