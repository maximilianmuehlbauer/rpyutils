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

def _(text):
    if fallback:
        return text
    else:
        return gettext_translate(text)

fallback = False
gettext_translate = None

try:
    import gettext
    gettext.textdomain("rpyutils")
    gettext_translate = gettext.gettext
except:
    fallback = True