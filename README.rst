Random Access File Reader
-------------------------

| This is a small library that allows for reading any given line in a file without having to read all the lines before it
  or load the entire file into memory.  Only the line indexes and lengths are held in memory, which enables random
  access even on very large files at a very minuscule memory cost.

Installation
============
``pip install git+https://github.com/jegesh/python-random-access-file-reader.git#egg=randomAccessReader``

Usage
=====

| Usage is very straightforward, and standard csv line endings (newline character), value delimiter (comma), and
  quotation character (double quote) are the defaults.  These can be changed in the constructor.
|
| Plain text file example:

::
        reader = RandomAccessReader('~/myfile.txt')
        line = reader.get_line(2)
        print line

| Csv example:

::
        reader = CsvRandomAccessReader('~/myfile.csv')
        line = reader.get_line_dict(5)
        for x in line:
            print x + " = " line[x]