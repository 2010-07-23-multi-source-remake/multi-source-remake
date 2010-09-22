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


ENCODING_DEF = 'UTF-8'
ENCODING_ERRORS_DEF = 'replace'

_unicode = __builtins__.get('unicode', str)
_bytes = __builtins__.get('bytes', str)

def safe_unicode(
            obj,
            encoding=ENCODING_DEF,
            errors=ENCODING_ERRORS_DEF,
        ):
    if not encoding:
        encoding = ENCODING_DEF
    
    try:
        if isinstance(obj, _unicode):
            return obj
        elif isinstance(obj, _bytes):
            return _unicode(obj, encoding, errors)
        else:
            return _unicode(obj)
    except ValueError:
        return _unicode()

def safe_bytes(
            obj,
            encoding=ENCODING_DEF,
            errors=ENCODING_ERRORS_DEF,
        ):
    if not encoding:
        encoding = ENCODING_DEF
    
    try:
        if isinstance(obj, _bytes):
            return obj
        elif isinstance(obj, _unicode):
            return obj.encode(encoding, errors)
        else:
            return _bytes(obj)
    except ValueError:
        return _bytes()


