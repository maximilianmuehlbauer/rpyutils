#!/usr/bin/env python
# coding=UTF-8

'''
rpyutils - Lib for the RP6 robot
Copyright (C) 2011 Scirocco <rpyutils@t-online.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

"""rpyutils by Maximilian Mühlbauer <rpyutils@t-online.de>"""

from distutils.core import setup

setup(name="rpyutils",
      version="0.1",
      description='rpyutils, flash your rp6 and use the terminal',
      author='Maximilian Mühlbauer',
      author_email='rpyutils@t-online.de',
      url='http://launchpad',
      license='GNU GPL v3',
      scripts=['rpyloader', 'rpyterm'],
      packages=['rpyutils'],
     )