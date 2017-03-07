Random Access File Reader
-------------------------

| This is a small library that allows for reading any given line in a file without having to read all the lines before it
  or load the entire file into memory.  Only the line indexes and lengths are held in memory, which enables random
  access even on very large files for a very minuscule memory cost.

Installation
============
``pip install random-access-file-reader``

Usage
=====

| Usage is very straightforward, and standard csv line endings (newline character), value delimiter (comma), and
  quotation character (double quote) are the defaults.  These can be changed in the constructor.
|
| The ``get_line()`` and ``get_line_dicts()`` methods return a list of rows.
|
| **Plain text file example:**

::

    from randomAccessReader import RandomAccessReader

    reader = RandomAccessReader('~/myfile.txt')

    # single line
    line = reader.get_lines(2)[0]
    print line

    # multiple lines
    lines = reader.get_lines(3, 3)
    for l in lines:
        print l

| Optional arguments in the constructor:

- ``endline_character`` - self-explanatory (default is endline character ``\n``)
- ``ignore_blank_lines`` - if set to ``True``, blank lines in the file will not be read or indexed (default is ``False``)

|
| **Csv example:**

::

    from randomAccessReader import CsvRandomAccessReader
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

| Optional arguments in the constructor:

- ``endline_character`` - self-explanatory (default is endline character ``\n``)
- ``ignore_blank_lines`` - if set to ``True``, blank lines in the file will not be read or indexed (default is ``True``)
- ``values_delimiter`` - character used by the csv to separate values within a line (default is ``,``)
- ``quotechar`` - character used by the csv to surround values that contain the value delimiting character (default is ``"``)
- ``ignore_corrupt`` - if set to ``True``, lines with an invalid length will return blank instead of raising an exception (default is ``False``)
