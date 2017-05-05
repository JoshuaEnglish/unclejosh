"""XLReader

Utility for reading Excel spreadsheets and generating lists of
namedtuple objects.
"""

__author__ = __maintainer__ = "Josh English"
__date__ = "2017-05-05"
__email__ = "josh@joshuarenglish.com"
__status__ = "Release"
__version__ = "1.1"



from collections import namedtuple, Mapping
from operator import itemgetter

import logging
XLOGGER = logging.getLogger('XLREADER')

from xlutils.view import SheetView

import json

try:
    from pubsub import pub
except ImportError:
    class dummypub:
        def sendMessage(self, *args, **kwargs):
            pass
    pub = dummypub()


class XLReader(object):
    """Reader(column_map)
    Creates an object to read an xlrd.Book object and create a list of
    namedtuple objects representing the data in one sheet of the book.
    Column_map is a dictionary of "header item", "fieldname" pairs.
    Column_map can also be a list or tuple of ("header item", "fieldname") pairs
    If column_map has a key of "_name", the value will be the name of the
    namedtuple class.
    Use Reader.scan_book_for_data(book) to load items.
    Reader.objects is a list of namedtuple objects.
    """
    def __init__(self, column_map):
        XLOGGER.debug("Creating Excel Reader")
        self.cols = []
        self.fields = []
        self.objects = []

        self.book = None
        self.sheet = None
        self.row = None
        self.getter = None

        self.classname = 'Datum'

        if isinstance(column_map, Mapping):
            map_items = column_map.items()
        else:
            map_items = column_map # assume it's an iterable of tuples

        for key, val in map_items:
            if key == '_name':
                self.classname = val
            else:
                self.cols.append(key)
                self.fields.append(val)
        self.tuple_class = namedtuple(self.classname, self.fields)
        self.filter_fields = []

    def set_filter_fields(self, fields):
        """set_filter_fields(fields)
        Creates an object creation filter.
        Fields listed must be non-empty
        """
        self.filter_fields = fields

    def scan_book_for_data(self, book):
        """scan_book_for_data(book)
        :param (xlrd.Book) book:  The book to scan.

        The Reader will go through each sheet until it finds a sheet
        with the appropriate values given as "header items".

        Once the sheet has been determined, every row below the header row
        will be converted to a namedtuple object.

        Calling this function replaces the list of namedtuple objects.
        """
        pub.sendMessage('%s.start' % self.classname)
        self._find_sheet(book)
        if self.sheet is None:
            XLOGGER.error("Cannot find sheet with appropriate data")
            raise ValueError("Cannot find sheet with appropriate data")

        self._load_objects()
        pub.sendMessage('%s.done' % self.classname)

    def _find_sheet(self, book):
        """Finds the appropriate sheet and row of the headers"""
        self.book = book
        for sheet in book.sheets():
            for ridx in range(sheet.nrows):
                row_values = sheet.row_values(ridx)
                if all(col in row_values for col in self.cols):
                    self.sheet = sheet
                    self.row = ridx
                    self._make_getter()
                    break
            if self.sheet is not None:
                break

    def _make_getter(self):
        """Create the itemgetter instance"""
        XLOGGER.debug('Creating Getter')
        values = self.sheet.row_values(self.row)
        idxs = (values.index(col) for col in self.cols)
        self.getter = itemgetter(*idxs)

    def _load_objects(self):
        """Create a namedtuple object for each valid row in the sheet
        below the header."""
        XLOGGER.debug("Loading objects")
        self.objects = []
        view = SheetView(self.book, self.sheet, slice(self.row+1, None, None))
        pub.sendMessage('%s.range', value = view.rows.stop)
        for idx, row in enumerate(view):
            pub.sendMessage('%s.update', value=idx)
            items = self.getter(list(row))
            new_tuple = self.tuple_class._make(items)
            is_good = True
            if self.filter_fields:
                for field in self.filter_fields:
                    if getattr(new_tuple, field) == '':
                        is_good = False
            if is_good:
                self.objects.append(new_tuple)
        XLOGGER.info("%d objects loaded", len(self.objects))

def xlreader_to_json(reader):
    """Retun a json-encoded representation of the reader.
    Does not record read objects
    """
    res = {}
    res['_name'] = reader.classname
    res['cols'] = reader.cols
    res['fields'] = reader.fields
    res['filters'] = reader.filter_fields
    return json.dumps(res)

def xlreader_from_json(json_string, klass=XLReader):
    """Create a reader from a previously stored json string"""
    res = json.loads(json_string)
    column_map = zip(res['cols'], res['fields'])
    reader = klass(column_map)
    reader.set_filter_fields(res['filters'])
    reader.classname = res['_name']
    return reader


