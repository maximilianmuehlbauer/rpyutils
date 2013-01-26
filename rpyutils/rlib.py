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

import serial
import time
import os
from rpyutils.flashlib import FlashLib
from rpyutils.translation import _

class Robby(object):
    def __init__(self, port="/dev/ttyUSB0", debuglevel=0):
        self.port = port
        self.debuglevel = debuglevel
    def write(self, data):
        self.connection.write(data)
        if self.debuglevel >= 3:
            outstr = _("OUT: ")
            for char in data:
                outstr += str(char) + " "
            print(outstr)
    def read(self, length):
        data = self.connection.read(length)
        if self.debuglevel >= 3:
            instr = _("IN: ")
            for char in data:
                instr += str(char) + " "
            print(instr)
        return data
    def connect(self):
        if self.debuglevel >= 1:
            print(_("Connecting to %s") % self.port)
        self.connection = serial.Serial(
            port=self.port,
            baudrate=38400,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
    def reset(self):
        if self.debuglevel >= 1:
            print(_("Resetting Robot"))
        # set RTS on & off, to reset the robot
        self.connection.setRTS(1)
        time.sleep(1)
        self.connection.setRTS(0)
        # read a newline character
        self.read(1)
        # read the boot message
        rp6boot = self.read(9)
        if rp6boot == b"[RP6BOOT]":
            # read another newline character
            self.read(1)
            return True
        else:
            raise RP6ConnectionError(_('Could not reset Robot %s') % str(rp6boot))

    def getType(self, getVoltage=False):
        # send ASCII character with value of 072
        self.write(b"H")
        # read first part of next boot message
        rp6boot = self.read(4)
        if rp6boot == b"RP6:":
            # read second part of boot message, to get the type
            rp6read = self.read(5)
            if rp6read == b"\x01\x01\x04\x05\x00":
                self.type = "rp6"
                if self.debuglevel >= 1:
                    print(_("RP6-Board connected"))
                if getVoltage:
                    self.getBatteryVoltage()
            elif rp6read == b"\x02\x01\x04\x03\x00":
                self.type = "m32"
                if self.debuglevel >= 1:
                    print(_("M32-Board connected"))
            return self.type
        else:
            raise RP6ConnectionError(_("Could not determinate the type of the Robot"))
        
    def getBatteryVoltage(self):
        self.write(b"\x95")
        value1 = ord(self.read(1))
        value2 = ord(self.read(1))
        # TODO check this
        print(_("Voltage: %s V") % str((((value1 & 255) << 0) + ((value2 & 255) << 8)) / 102.4))
        
    def setHighSpeed(self):
        self.write(b"5")
        highspeed = self.read(1)
        if(highspeed == b"F"):  # highspeed !!!
            time.sleep(1)
            self.connection.baudrate = 500000
            self.write(b"\xAA\xAA\xAA\xAA\xAA\x99")
            highspeed = self.read(2)
            if highspeed == b"\xaaV":
                if self.debuglevel >= 1:
                    print(_("Highspeed enabled"))
                return True
            else:
                raise RP6ConnectionError(_("Could not setup high speed connection"))
    def flash(self, bindata):
        if self.debuglevel >= 1:
            print(_("Initializing flash"))
        # init flashing
        self.write(b"I")
        confirm = self.read(1)
        if confirm != b"g":
            return False
        self.write(b"K")
        confirm = self.read(1)
        if confirm != b"[":
            return False
        flashlib = FlashLib(bindata)
        blocknr = 0
        if self.debuglevel >= 1:
            print(_("Flashing"))
        while flashlib.getblock(blocknr):
            if self.debuglevel >= 2:
                print(_("Flashing block: %i") % blocknr)
            self.write(bytes([170]))
            self.write(b"\x80")
            self.write(b"\x00")
            self.write(bytes([blocknr]))
            
            flashdata = flashlib.getblock(blocknr)
            self.write(flashdata[1])
            
            self.write(bytes([(flashdata[0] & 255)]))
            self.write(bytes([(flashdata[0] >> 8) & 255]))
            self.write(b"\xAA")
            confirm = self.read(3)
            if confirm != b"B][":
                raise FlashError(_("Error flashing Block %i") % blocknr)
            blocknr += 1
        if self.debuglevel >= 1:
            print(_("Flashing finished"))
        self.connection.baudrate = 38400
        self.write(bytes([0]))
            
    @staticmethod
    def getFileClass(file):
            filename, fileextension = os.path.splitext(file)
            cfile = filename + ".c"
            if "RP6RobotBaseLib.h" in open(cfile).read():
                progtype = "rp6"
            elif "RP6ControlLib.h" in open(cfile).read():
                progtype = "m32"
            return progtype

class RP6ConnectionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class FlashError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
