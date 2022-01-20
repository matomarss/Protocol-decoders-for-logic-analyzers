##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2022 Matej Martinček <matomarss@gmail.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

'''
OUTPUT_PYTHON format:

Packet:
[<ptype>, <pdata>]

<ptype>:
 - 'DATA'
 - 'PACKET END' (<pdata>: 0)

<pdata> is the data byte associated with the 'DATA'
command.
'''

import re
import sigrokdecode as srd
from common.srdhelper import bcd2int, SrdIntEnum

class Decoder(srd.Decoder):
    api_version = 3
    id = 'spi_extractor'
    name = 'SPI bytes extractor'
    longname = 'The SPI bytes extractor'
    desc = 'Extracts MOSI/MISO data values from SPI communication and potentially sends them to other stack-decoders'
    license = 'gplv2+'
    inputs = ['spi']
    outputs = ['dataBytes']
    tags = ['Embedded/industrial']
    annotations = ()
    annotation_rows = ()

    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 'INACTIVE'

    def start(self):
        self.out_python = self.register(srd.OUTPUT_PYTHON)

    def putp(self, data):
        self.put(self.ss, self.es, self.out_python, data)

    def send_data(self, b):
        # Send received data packet of type DATA
        self.putp(['DATA', b])

    def decode(self, ss, es, data):
        cmd, mosi, miso = data

        self.ss, self.es = ss, es

        if cmd == 'DATA':
            # If MOSI is sending a packet, pass it on as a single packet
            if mosi is not None:
                self.send_data(mosi)
            # If MISO is sending a packet, pass it on as a single packet
            if miso is not None:
                self.send_data(miso)
