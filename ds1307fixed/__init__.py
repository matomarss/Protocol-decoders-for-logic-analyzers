##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2013 Matt Ranostay <mranostay@gmail.com>
## Copyright (C) 2022 Martinček Matej <matomarss@gmail.com>
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
This decoder stacks on top of the 'i2c' PD and decodes the Dallas DS1307
real-time clock (RTC) specific registers and commands. This is a fixed version of this decoder capable of decoding
communication that starts with reading from registers without needing to specify the address of the register where the
reading starts. In this version, the decoder is also capable of visualizing that only some registers
were read from/written to.
'''

from .pd import Decoder
