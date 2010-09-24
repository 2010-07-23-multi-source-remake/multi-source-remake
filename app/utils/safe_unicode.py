#!/usr/bin/env python2
#-*- coding: UTF-8 -*-
# For Python-2.6:
from __future__ import absolute_import, division, print_function, unicode_literals
# unicode_str.py
#
#
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
#
# 


import sys

ENCODING_DEF = 'utf-8'
ENCODING_ERRORS_DEF = 'replace'

def get_fd_encoding(fd, fd_encoding_def=None):
    try:
        fd_encoding = fd.encoding or fd_encoding_def
    except AttributeError:
        fd_encoding = fd_encoding_def
    
    return fd_encoding

def safe_unicode(
            obj,
            encoding=ENCODING_DEF,
            errors=ENCODING_ERRORS_DEF,
        ):
    if not encoding:
        encoding = ENCODING_DEF
    
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
            encoding=ENCODING_DEF,
            errors=ENCODING_ERRORS_DEF,
        ):
    if not encoding:
        encoding = ENCODING_DEF
    
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
    encoding = get_fd_encoding(fd)
    
    args_b = [
        safe_bytes(arg, encoding=encoding)
        for arg in args
    ]
    
    print(*args_b, **kwargs)


