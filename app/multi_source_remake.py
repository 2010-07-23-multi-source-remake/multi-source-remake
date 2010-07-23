#!/usr/bin/env python2
#-*- coding: UTF-8 -*-
# For Python-2.6:
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *
# multi_source_remake.py
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

import sys, os, os.path, contextlib
from .unicode_str import unicode_if_necessary, str_if_necessary

class UserError(Exception):
    pass

class Conf:
    def __init__(self):
        self.verbose = False
        self.bufsize = None
        self.src_paths = []
        self.out_path = None

def copy_mtime(source, target):
    stat = os.stat(source)
    atime = stat.st_atime
    mtime = stat.st_mtime
    
    os.utime(target, (atime, mtime))

def equal_bufs(bufs):
    for buf in bufs:
        if bufs[0] != buf:
            return False
    else:
        return True

def suggest_correct(bufs, rating):
    sorted_rating = sorted(
        [(i, score) for i, score in enumerate(rating)],
        key=lambda x: x[1],
        reverse=True
    )
    
    suggest = None
    sugg_score = None
    
    for candidate, cand_rating_score in sorted_rating:
        cand_buf = bufs[candidate]
        cand_score = len([1 for buf in bufs if cand_buf == buf])
        
        if suggest is None or cand_score > sugg_score:
            suggest = candidate
            sugg_score = cand_score
    
    return suggest

def remake(conf):
    srcs_rating = [0] * len(conf.src_paths)
    
    with contextlib.nested(
                *(open(x, 'rb') for x in conf.src_paths)
            ) as srcs:
        with open(conf.out_path, 'wb') as out:
            while True:
                try:
                    bufs = [x.read(conf.bufsize) for x in srcs]
                    
                    if not bufs[0]:
                        raise EOFError()
                    
                    for i, buf in enumerate(bufs):
                        if not buf:
                            raise IOError(
                                'Unexpected end of file \'%s\'' %
                                conf.src_paths[i]
                            )
                except EOFError:
                    break
                
                if equal_bufs(bufs):
                    out.write(bufs[0])
                else:
                    correct = suggest_correct(bufs, srcs_rating)
                    incorrects = [i for i, buf in enumerate(bufs) if buf != bufs[correct]]
                    
                    for i in incorrects:
                        srcs_rating[i] -= 1
                    
                    if conf.verbose:
                        print(
                            'Detected incorrectness:\n\tIncorrect data in:\n%s\n%s' % (
                                '\n'.join(
                                    '\t\t%s (%s score)' % (conf.src_paths[i], srcs_rating[i])
                                    for i in incorrects
                                ),
                                '\tUsed: %s (%s score)' % (conf.src_paths[correct], srcs_rating[correct])
                            )
                        )
                    
                    out.write(bufs[correct])
    try:
        copy_mtime(conf.src_paths[0], conf.out_path)
    except OSError as e:
        print('Warning: %s: %s' % (type(e), e), file=sys.stderr)
    
    if conf.verbose:
        print('Remaked \'%s\'' % conf.out_path)
        print(
            'Total data correctness:\n%s' %
            '\n'.join(
                '\t%s: %s score' % (src_path, srcs_rating[i])
                for i, src_path in enumerate(conf.src_paths)
            )
        )

def print_help(app_name):
    print(
        'Usage %(app_name)s: \n'
        '%(app_name)s [-verbose] [-bufsize=<size>] [-out=<output-file>] '
            '<main-source> <addition-source> <addition-source> ...' %
        {'app_name': app_name}
    )

def main():
    app_name = unicode_if_necessary(sys.argv[0])
    
    try:
        args = list(map(unicode_if_necessary, sys.argv[1:]))
        conf = Conf()
        
        if args:
            for arg in args:
                if arg.startswith('-'):
                    opt = arg[len('-'):].split('=', 1)
                    opt_nam = opt[0]
                    opt_val = opt[1] if len(opt) > 1 else None
                    
                    if opt_nam == 'verbose':
                        if not conf.verbose:
                            conf.verbose = True
                        else:
                            raise UserError('Reused option \'verbose\'')
                    elif opt_nam == 'bufsize':
                        opt_val_int = int(opt_val)
                        
                        if conf.bufsize is None:
                            opt_val_int = int(opt_val)
                            if opt_val_int > 0:
                                conf.bufsize = opt_val_int
                            else:
                                raise UserError(
                                    'Invalid value \'%s\' of option \'bufsize\'' %
                                    opt_val_int
                                )
                        else:
                            raise UserError('Reused option \'bufsize\'')
                    elif opt_nam == 'out':
                        if conf.out_path is None:
                            conf.out_path = opt_val
                        else:
                            raise UserError('Reused option \'out\'')
                    elif opt_nam == 'help' or \
                            opt_nam == 'h' or opt_nam == '-help':
                        print_help(app_name)
                        
                        return
                    else:
                        raise UserError('Unrecognised option \'%s\'' % opt_nam)
                else:
                    conf.src_paths.append(arg)
        else:
            raise UserError('Too few arguments')
        
        if len(conf.src_paths) < 3:
            raise UserError('Too few source files')
        
        if conf.bufsize is None:
            conf.bufsize = 512
        
        if conf.out_path is None:
            conf.out_path = os.path.join(
                os.path.dirname(conf.src_paths[0]),
                'remaked.%s' % os.path.basename(conf.src_paths[0]),
            )
        
        remake(conf)
    except UserError as e:
        print('%s' % e, file=sys.stderr)
        print_help(app_name)
        
        return 2


