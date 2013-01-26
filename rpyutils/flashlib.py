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

class FlashLib(object):
    def __init__(self, bindata):
        self.bindata = bindata
        counter = len(self.bindata) % 256
        while counter < 256:
            self.bindata += bytes([255])
            counter += 1
        
    def checksum(self, checksum, databyte):
        tmp = (databyte & 255) ^ (checksum & 255)
        databyte = tmp ^ (tmp << 4)
        tmp1 = ((databyte & 255) << 8 | checksum >> 8 & 255)
        tmp2 = (databyte & 255) >> 4
        tmp3 = (databyte & 255) << 3
        return tmp1 ^ tmp2 ^ tmp3
        
    def getblock(self, blocknr):
        offset = blocknr * 256
        
        if offset == len(self.bindata):
            return False
        
        checksum = 65535
        checksum = self.checksum(checksum, 170)
        checksum = self.checksum(checksum, 128)
        checksum = self.checksum(checksum, 0)
        checksum = self.checksum(checksum, blocknr)
        
        counter = offset
        while counter < offset + 256:
            checksum = self.checksum(checksum, self.bindata[counter])
            counter += 1
            
        # return checksum + block
        return checksum, self.bindata[offset:offset + 256]
