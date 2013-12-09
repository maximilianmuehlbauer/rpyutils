#!/usr/bin/env python3
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

import glob
from rpyutils.translation import _

class HexToBin(object):
    def __init__ (self, filename, debuglevel):
        self.debuglevel = debuglevel
        self.parseHex(filename)
        
    def parseHex(self, filename):
        self.bindata = b""
        if self.debuglevel >= 2:
            print(_("Parsing Hexfile: %s") % filename)
        file = open(filename, "rb")
        for linenr, line in enumerate(file):
            line = line[1:]
            
            position = 0
            checksum = 0;
            while position < len(line) - 2:
                checksum = checksum + int(line[position:position + 2], 16)
                position += 2
            if checksum % 256 != 0:
                raise HexError(_("Incorrect Checksum at line %i") % linenr)
            
            # cut line to data
            line = line[8:-4]
            position = 0
            while position < len(line):
                self.bindata += bytes([int(line[position:position + 2], 16)])
                position += 2
                
    def getBinData(self):
        return self.bindata
    
    @staticmethod
    def findHexFile():
        hexfiles = glob.glob("*.hex")
        if len(hexfiles) > 1 or len(hexfiles) == 0:
            return False
        else:
            return hexfiles[0]
            
class HexError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
