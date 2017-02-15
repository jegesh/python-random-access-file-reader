"""
General random-access file reader with very small memory overhead
Inspired by: http://stackoverflow.com/a/35785248/1857802

@author: Yaakov Gesher
"""

# =============
# imports
# =============


# ==========
# classes
# ==========


class RandomAccessReader(object):

    def __init__(self, filepath, endline_character='\n'):
        """
        :param filepath:  Absolute path to file
        :param endline_character: Delimiter for lines. Defaults to newline character (\n)
        """
        self._filepath = filepath
        self._endline = endline_character
        self._lines = self._get_line_data()

    def _get_line_data(self):
        f = open(self._filepath)
        lines = []
        start_position = 0
        has_more = True
        current_line = 0
        while has_more:
            current = f.read(1)
            if current == '':
                has_more = False
                continue

            if current == self._endline:
                # we've reached the end of the current line
                lines.append({"position": start_position, "length": current_line})
                start_position += current_line + 1
                current_line = 0
                continue

            current_line += 1
        f.close()
        return lines

    def get_line(self, line_number):
        """
        get the contents of a given line in the file
        :param line_number: 0-indexed line number
        :return: str
        """
        with open(self._filepath) as f:
            line_data = self._lines[line_number]
            f.seek(line_data['position'])
            return f.read(line_data['length'])


class CsvRandomAccessReader(RandomAccessReader):

    def __init__(self, filepath, has_header=True, endline_character='\n', values_delimiter=','):
        super(CsvRandomAccessReader, self).__init__(filepath, endline_character)
        self.headers = None
        self._delimiter = values_delimiter
        if has_header:
            pass
            