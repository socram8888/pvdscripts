#!/usr/bin/env python3

import wave
import sys
import re

FRAME_SIZE = 19600

assert(len(sys.argv) == 2)

f = wave.open(sys.argv[1], 'rb')

audio = open(f'{sys.argv[1]}.a.raw', 'wb')
video = open(f'{sys.argv[1]}.v.raw', 'wb')

frames = bytearray()
while True:
	buf = f.readframes(1024)

	if len(buf) == 0:
		break
	frames.extend(buf)

preamble_pattern = (
	b'\x81\xE3\xE3\xC7\xC7\x81\x81\xE3\xC7.' * 24 +
	b'\x00\x00\x02\x01\x04\x02\x06\x03\xFF.' +
	b'\x08\x04\x0A\x05\x0C\x06\x0E\x07\xFF.' +
	b'\x11\x08\x13\x09\x15\x0A\x17\x0B\xFF.' +
	b'\x19\x0C\x1B\x0D\x1D\x0E\x1F\x0F\xFF.' +
	b'\x00\\x28\x02\\x29\x04\\x2A\x06\\x2B\xFF.' +
	b'\x08\x2C\x0A\x2D\x0C\x2E\x0E\x2F\xFF.' +
	b'\x11\x30\x13\x31\x15\x32\x17\x33\xFF.' +
	b'\x19\x34\x1B\x35\x1D\x36\x1F\x37\xFF.' +
	b'\x00\x38\x02\x39\x04\x3A\x06\x3B\xFF.' +
	b'\x08\x3C\x0A\x3D\x0C\x3E\x0E\\x3F\xFF.' +
	b'\x11\x40\x13\x41\x15\x42\x17\x43\xFF.' +
	b'\x19\x44\x1B\x45\x1D\x46\x1F\x47\xFF.' +
	b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF.' +
	b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF.' * 3
)

match = re.search(preamble_pattern, frames)
assert(match)

frames = frames[match.start():]

off = 0
while True:
	line = frames[off : off + 10]
	if len(line) != 10:
		break

	if off % FRAME_SIZE >= 400:
		video.write(line[0:9])
	audio.write(line[9:10])

	off += 10
