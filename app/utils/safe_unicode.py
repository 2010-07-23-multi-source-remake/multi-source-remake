#!/usr/bin/env python
#-*- coding: utf-8 -*-
# for Python-2.6:
from __future__ import absolute_import, division, print_function, unicode_literals

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without_path even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys

DEFAULT_ENCODING = 'utf-8'
DEFAULT_ENCODING_ERRORS = 'replace'

def safe_unicode(
            obj,
            encoding=DEFAULT_ENCODING,
            errors=DEFAULT_ENCODING_ERRORS,
        ):
    if not encoding:
        encoding = DEFAULT_ENCODING
    
    try:
        if isinstance(obj, unicode):
            return obj
        elif isinstance(obj, bytes):
            return unicode(obj, encoding, errors)
        else:
            return unicode(obj)
    except ValueError:
        return u'<VALUE_ERROR>'

def safe_bytes(
            obj,
            encoding=DEFAULT_ENCODING,
            errors=DEFAULT_ENCODING_ERRORS,
        ):
    if not encoding:
        encoding = DEFAULT_ENCODING
    
    try:
        if isinstance(obj, bytes):
            return obj
        elif isinstance(obj, unicode):
            return obj.encode(encoding, errors)
        else:
            return bytes(obj)
    except ValueError:
        return b'<VALUE_ERROR>'

def safe_print(*args, **kwargs):
    fd = kwargs.get('file', sys.stdout)
    encoding = getattr(fd, 'encoding', None)
    
    args_b = [
        safe_bytes(arg, encoding=encoding)
        for arg in args
    ]
    
    print(*args_b, **kwargs)


