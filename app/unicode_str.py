#!/usr/bin/env python2
#-*- coding: UTF-8 -*-
# For Python-2.6:
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *
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

def unicode_if_necessary(obj):
    try:
        if isinstance(obj, str):
            return obj.decode('UTF-8')
        elif isinstance(obj, unicode):
            return obj
        else:
            return unicode(obj)
    except ValueError:
        return unicode()

def str_if_necessary(obj):
    try:
        if isinstance(obj, unicode):
            return obj.encode('UTF-8')
        elif isinstance(obj, str):
            return obj
        else:
            return str(obj)
    except ValueError:
        return str()


