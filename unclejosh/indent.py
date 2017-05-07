# -*- coding: utf-8 -*-
"""
indent.py

Simple indentation guide for printed tree-like output.

Repeats a string for a certain number of characters. Default string is
" :  ".

>>> from indent import indent
>>> for x in range(7): print(indent(x),"line")
 line
  line
 : line
 :  line
 :   line
 :    line
 :   : line
>>>

"""

from itertools import islice, cycle

__author__ = "Joshua R English"
__version__ = "1.0.1"
__history__ = """
2016-11-13 -- 1.0.1 -- fixed typo in __author__ and __version__
                       code cleanup with pep8 and flake8
"""

DOT = ":"
PAD = 1
WIDTH = 4
DOTS = None


def dot():
    """Returns the current dot character.
    Use set_dot to change this character."""
    return DOT


def set_dot(dot):
    """set_dot(dot)
    Sets the single-character for the dot
    """
    global DOT
    if len(dot) != 1:
        raise ValueError("dot must be a single character")
    DOT = dot
    build_dot_string()


def set_width(width):
    """set_width(width)
    Sets the total width of the repeated indentation string.
    """
    global WIDTH
    if WIDTH < 2:
        raise ValueError("width must be at least 2")
    WIDTH = int(width)
    build_dot_string()


def set_left_pad(width):
    """set_left_PAD(width)
    Sets the number of spaces to the left of the dot character.
    """
    global PAD
    PAD = int(max(width, 0))
    build_dot_string()


def build_dot_string():
    """Rebuild the indentation string"""
    global DOTS
    if PAD + 1 > WIDTH:
        raise ValueError("Pad and Dot are bigger than the total width")
    DOTS = "{0}{1}{2}".format(" "*PAD, DOT, " "*(WIDTH-PAD-1))


build_dot_string()


def set_dots(dots):
    """set_dots(dots)
    Sets the string for indetation
    """
    global DOTS
    DOTS = dots


def indent(length):
    """indent(length)
    Return a string of length `length` with dot characters spaced into columns
    """
    return ''.join(islice(cycle(DOTS), length))


if __name__ == '__main__':
    for x in range(7):
        print(indent(x), "line")
