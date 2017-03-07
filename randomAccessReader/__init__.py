"""
General random-access file reader with very small memory overhead
Inspired by: http://stackoverflow.com/a/35785248/1857802 and http://stackoverflow.com/a/14999585/1857802

@author: Yaakov Gesher
"""

# =============
# imports
# =============

import csv
import StringIO

# ==========
# classes
# ==========


class RandomAccessReader(object):

    def __init__(self, filepath, endline_character='\n', ignore_blank_lines=False):
        """
        :param filepath:  Absolute path to file
        :param endline_character: Delimiter for lines. Defaults to newline character (\n)
        """
        self._filepath = filepath
        self._endline = endline_character
        self._ignore_blanks = ignore_blank_lines
        self._lines = self._get_line_data()

    @property
    def number_of_lines(self):
        return len(self._lines)

    def get_line_indexes(self):
        return range(len(self._lines))

    def _get_line_data(self):
        f = open(self._filepath)
        lines = []
        start_position = 0
        has_more = True
        current_line = 0
        while has_more:
            current = f.read(1)

            if current == self._endline or current == '':
                # we've reached the end of the current line
                if not self._ignore_blanks or current_line > 0:
                    lines.append({"position": start_position, "length": current_line})
                start_position += current_line + 1
                current_line = 0
                if current == '':
                    has_more = False
                continue

            current_line += 1
        f.close()
        return lines

    def get_lines(self, line_number, amount=1):
        """
        get the contents of a given line in the file
        :param line_number: 0-indexed line number
        :param amount amount of lines to read
        :return: str
        """
        lines = []
        with open(self._filepath) as f:
            for x in xrange(amount):
                line_data = self._lines[line_number]
                f.seek(line_data['position'])
                lines.append(f.read(line_data['length']))
            return lines


class CsvRandomAccessReader(RandomAccessReader):

    def __init__(self, filepath, has_header=True, **kwargs):
        """

        :param filepath:
        :param has_header:
        :param kwargs: endline_character='\n', values_delimiter=',', quotechar='"', ignore_corrupt=False, ignore_blank_lines=True
        """
        super(CsvRandomAccessReader, self).__init__(filepath, kwargs.get('endline_character','\n'), kwargs.get('ignore_blank_lines', True))
        self._headers = None
        self._delimiter = kwargs.get('values_delimiter', ',')
        self._quotechar = kwargs.get('quotechar', '"')
        self._ignore_bad_lines = kwargs.get('ignore_corrupt', False)
        self.has_header = has_header
        if has_header:
            dialect = self.MyDialect(self._endline, self._quotechar, self._delimiter)
            b = StringIO.StringIO(self.get_lines(0)[0])
            r = csv.reader(b, dialect)
            values = tuple(r.next())
            self._headers = values

    @property
    def headers(self):
        return self._headers

    def set_headers(self, header_list):
        if not hasattr(header_list, '__iter__'):
            raise TypeError("Argument 'header_list' must contain an iterable")
        self._headers = tuple(header_list)

    def _get_line_values(self, line):
        """
        Splits the csv line into a list of individual values
        :param line: str
        :return: tuple of str
        """
        dialect = self.MyDialect(self._endline, self._quotechar, self._delimiter)
        b = StringIO.StringIO(line)
        r = csv.reader(b, dialect)
        values = tuple(r.next())
        if len(self._headers) != len(values):
            if not self._ignore_bad_lines:
                raise ValueError("Corrupt csv - header and row have different lengths")
            return None
        return values

    def get_line_dicts(self, line_number, amount=1):
        """
        gets the requested line as a dictionary (header values are the keys)
        :param line_number: requested line number, 0-indexed (disregards the header line if present)
        :param amount
        :return: dict
        """
        if not self._headers:
            raise ValueError("Headers must be set before requesting a line dictionary")
        if self.has_header:
            line_number += 1
        lines = []
        text_lines = self.get_lines(line_number, amount)
        for x in xrange(amount):
            vals = self._get_line_values(text_lines[x])
            if vals is None:
                lines.append(dict(zip(self._headers, range(len(self._headers)))))
            else:
                lines.append(dict(zip(self._headers, vals)))
        return lines

    class MyDialect(csv.Dialect):
        strict = True
        skipinitialspace = True
        quoting = csv.QUOTE_ALL
        delimiter = ','
        quotechar = '"'
        lineterminator = '\n'

        def __init__(self, terminator, quotechar, delimiter):
            csv.Dialect.__init__(self)
            self.delimiter = delimiter
            self.lineterminator = terminator
            self.quotechar = quotechar
