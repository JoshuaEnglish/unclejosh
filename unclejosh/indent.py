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
__author__ = "Joshua R English"
__version__ = "1.0"

from itertools import islice, cycle

_dot = ":"
_pad = 1
_width = 4

def dot():
    return _dot

def set_dot(dot):
    """set_dot(dot)
    Sets the single-character for the dot
    """
    global _dot
    if len(dot) != 1:
        raise ValueError("dot must be a single character")
    _dot = dot
    _build_dots()

def set_width(width):
    """set_width(width)
    Sets the total width of the repeated indentation string.
    """
    global _width
    if _width < 2:
        raise ValueError("width must be at least 2")
    _width = int(width)
    _build_dots()

def set_left_pad(width):
    """set_left_pad(width)
    Sets the number of spaces to the left of the dot character.
    """
    global _pad
    _pad = int(max(width, 0))
    _build_dots()

def _build_dots():
    """Rebuild the indentation string"""
    global _dots
    if _pad + 1 > _width:
        raise ValueError("Pad and Dot are bigger than the total width")
    _dots = "{0}{1}{2}".format(" "*_pad, _dot, " "*(_width-_pad-1))

_build_dots()

def set_dots(dots):
    """set_dots(dots)
    Sets the string for indetation
    """
    global _dots
    _dots = dots

def indent(x):
    """indent(x)
    Return a string of length x with dot characters spaced into columns
    """
    return ''.join(islice(cycle(_dots), x))

if __name__ == '__main__':
    for x in range(7): print(indent(x),"line")