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


import re
import sigrokdecode as srd
from common.srdhelper import bcd2int, SrdIntEnum
import math

a = ['ADDRESS', 'DATA', 'ADDRESS2', 'DATA2', ]

Ann = SrdIntEnum.from_list('Ann', a)

class Decoder(srd.Decoder):
    api_version = 3
    id = 'packeter'
    name = 'Packeter'
    longname = 'The Packeter'
    desc = 'Alters input according to options.'
    license = 'gplv2+'
    inputs = ['dataBytes']
    options = (
        {'id': 'output-format', 'desc': 'Format for displaying packets values',
         'default': 'dec', 'values': ('dec', 'ASCII', 'bin', 'hex')},
        {'id': 'input-binary-format', 'desc': 'Binary format in which the input is encoded',
         'default': 'bin', 'values': ('bin', 'BCD')},
        {'id': 'max-packet-length', 'desc': 'Maximal length of a packet',
         'default': 4},
        {'id': 'packet-separator-sequence',
         'desc': 'Sequence of characters to separate packets on (hexadecimal values without 0x separated by ,)',
         'default': 'none'},
        {'id': 'use-separator-sequence', 'desc': 'Separate packets on sequence of characters',
         'default': 'no', 'values': ('yes', 'no')},
        {'id': 'display-separator-sequence', 'desc': 'Display separation sequence characters',
         'default': 'yes', 'values': ('yes', 'no')},
    )
    outputs = []
    tags = ['Embedded/industrial']
    annotations = (
        ('address', 'Address'),
        ('data', 'Data'),
        ('address2', 'Address2'),
        ('data2', 'Data2'),
    )
    annotation_rows = (
        ('first', 'First row', (Ann.ADDRESS, Ann.DATA,)),
        ('second', 'Second row', (Ann.ADDRESS2, Ann.DATA2,)),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        # Almost all global variables are remembered for each row separately
        self.ss = [0, 0]
        self.es = [0, 0]
        self.state = ['NEUTRAL', 'NEUTRAL']
        self.current_row = 0
        self.stored_values = [[], []]
        self.separation_sequence_pointer = [0, 0]

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)
        # Split the separation sequence string at commas to create a list
        if self.options['use-separator-sequence'] == 'yes':
            self.separation_sequence = str(self.options['packet-separator-sequence']).split(',')
        else:
            self.separation_sequence = []

    def manage_stored_values(self, t):
        if self.have_to_output():
            self.output_stored_values(t)

    def output_stored_values(self, t):
        # Outputs all values stored until now at the current row with the correct annotation type and at the correct row
        if len(self.stored_values[self.current_row]) == 0:
            return
        if t == 'DATA':
            if self.current_row == 0:
                self.put(self.ss[0], self.es[0], self.out_ann, [Ann.DATA, ['Data: ' + self.get_output(), 'Da', 'D']])
            elif self.current_row == 1:
                self.put(self.ss[1], self.es[1], self.out_ann, [Ann.DATA2, ['Data: ' + self.get_output(), 'Da', 'D']])
        elif t == 'ADDR':
            if self.current_row == 0:
                self.put(self.ss[0], self.es[0], self.out_ann, [Ann.ADDRESS, ['Address: ' + self.get_output(), 'Add', 'A']])
            elif self.current_row == 1:
                self.put(self.ss[1], self.es[1], self.out_ann, [Ann.ADDRESS2, ['Address: ' + self.get_output(), 'Add', 'A']])

        # Resets the current state, stored values and separation sequence pointer for the current row
        self.state[self.current_row] = 'NEUTRAL'
        self.stored_values[self.current_row] = []
        self.separation_sequence_pointer[self.current_row] = 0

    def have_to_output(self):
        # Returns True if the options indicate that a new packet should be started and the previous one finished
        return self.options['max-packet-length'] == len(self.stored_values[self.current_row]) or self.is_separated_by_sequence()

    def is_separated_by_sequence(self):
        # Returns True if the sequence separation is active and the pointer indicates the need of separation
        return (self.options['use-separator-sequence'] == 'yes' and
                0 < len(self.separation_sequence) <= self.separation_sequence_pointer[self.current_row])

    def move_separation_sequence_pointer(self, value):
        # If the sequence separation is active
        if len(self.separation_sequence) == 0 or self.options['use-separator-sequence'] == 'no':
            return
        if self.options['input-binary-format'] == 'BCD':
            value = bcd2int(value)

        # ...and this value is starting a separation sequence or following an already
        # started separation sequence, move the separation sequence pointer potentially causing separation
        if str(hex(value).replace("0x", "")) == self.separation_sequence[self.separation_sequence_pointer[self.current_row]]:
            self.separation_sequence_pointer[self.current_row] += 1
        # ...otherwise reset separation sequence pointer
        else:
            self.separation_sequence_pointer[self.current_row] = 0

    def get_output(self):
        # If the options say so, the separation sequence characters should be excluded from the output
        if self.is_separated_by_sequence() and self.options['display-separator-sequence'] == 'no':
            for _ in self.separation_sequence:
                self.stored_values[self.current_row].pop()

        # Get the output from the values stored in the current row according to output and input binary format options
        output = ''
        if self.options['output-format'] == 'dec':
            for b in self.stored_values[self.current_row]:
                if self.options['input-binary-format'] == 'BCD':
                    b = bcd2int(b)
                output = output + ' ' + str(b)
        elif self.options['output-format'] == 'bin':
            for b in self.stored_values[self.current_row]:
                if self.options['input-binary-format'] == 'BCD':
                    b = bcd2int(b)
                output = output + ' ' + str(bin(b).replace("0b", ""))
        elif self.options['output-format'] == 'ASCII':
            for b in self.stored_values[self.current_row]:
                if self.options['input-binary-format'] == 'BCD':
                    b = bcd2int(b)

                # If the output format is ASCII, visualize only characters with codes from 32 up to 126
                # and use special symbols for the other codes
                if b == 10:
                    b = "\u240a"
                elif b == 13:
                    b = "\u240d"
                elif b == 32:
                    b = "\u2423"
                elif b == 9:
                    b = "\u21e5"
                elif 126 >= b >= 32:
                    b = chr(b)
                else:
                    b = "\ufffd"
                output = output + b
        elif self.options['output-format'] == 'hex':
            for b in self.stored_values[self.current_row]:
                if self.options['input-binary-format'] == 'BCD':
                    b = bcd2int(b)
                output = output + ' ' + hex(b)
        return output

    # Any addition to stored values should be done via this method
    def add_to_stored_values(self, value):
        self.stored_values[self.current_row].append(value)
        self.move_separation_sequence_pointer(value)

    def decode(self, ss, es, data):
        cmd, data_value, row = data

        # Data values are stored for each row separately and separation conditions are checked for each row separately
        # Therefore, current_row has to be set before the processing of the next data value can start
        self.current_row = row

        # State machine.
        if self.state[self.current_row] == 'NEUTRAL':
            self.ss[self.current_row] = ss

        if cmd == 'DATA':
            # If has not finished collecting an ADDRESS packet yet, finish it now
            if self.state[self.current_row] == 'RECEIVING ADDRESS':
                self.output_stored_values('ADDR')
                self.ss[self.current_row] = ss

            # On this row we are receiving DATA packets now
            self.state[self.current_row] = 'RECEIVING DATA'
            # Set the end of the current packet on this row for now
            self.es[self.current_row] = es

            self.add_to_stored_values(data_value)

            # Send all data values stored in this row until now if it is necessary and clear the buffer
            self.manage_stored_values('DATA')
        elif cmd == 'ADDRESS':
            # If has not finished collecting a DATA packet yet, finish it now
            if self.state[self.current_row] == 'RECEIVING DATA':
                self.output_stored_values('DATA')
                self.ss[self.current_row] = ss

            # On this row we are receiving ADDRESS packets now
            self.state[self.current_row] = 'RECEIVING ADDRESS'
            # Set the end of the current packet on this row for now
            self.es[self.current_row] = es

            self.add_to_stored_values(data_value)

            # Send all address values stored in this row until now if it is necessary and clear the buffer
            self.manage_stored_values('ADDR')
