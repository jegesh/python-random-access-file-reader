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
| The ``get_line()`` and ``get_line_dicts()`` methods return a list of rows.
| Plain text file example:

::

    reader = RandomAccessReader('~/myfile.txt')

    # single line
    line = reader.get_lines(2)[0]
    print line

    # multiple lines
    lines = reader.get_lines(3, 3)
    for l in lines:
        print l

| Csv example:

::

    reader = CsvRandomAccessReader('~/myfile.csv')

    # single line
    line = reader.get_line_dicts(5)[0]
    for x in line:
        print x + " = " line[x]

    # multiple lines
    lines = reader.get_line_dicts(6, 6)
    for l in lines:
        for x in l:
            print x + " = " l[x]
