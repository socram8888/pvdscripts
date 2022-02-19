#!/usr/bin/env python3

from PIL import Image
import sys
import os

FRAME_WIDTH = 216
FRAME_HEIGHT = 160
FRAME_SIZE = (FRAME_WIDTH * FRAME_HEIGHT) // 2

COLOR_MATRIX = [
	[
		(1, 0, 0),
		(0, 1, 0),
		(0, 0, 1),
	],
	[
		(0, 1, 0),
		(0, 0, 1),
		(1, 0, 0),
	]
]

assert(len(sys.argv) == 3)

video = open(sys.argv[1], 'rb')
if not os.path.exists(sys.argv[2]):
	os.makedirs(sys.argv[2])

image = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT))
framenum = 0

while True:
	rawframe = video.read(FRAME_SIZE)
	if len(rawframe) != FRAME_SIZE:
		break

	for y in range(FRAME_HEIGHT):
		for x in range(FRAME_WIDTH):
			nibblepos = y * FRAME_WIDTH + x
			value = rawframe[nibblepos >> 1]
			if nibblepos & 1:
				value >>= 4
			else:
				value &= 0xF

			value = round(value * 255 / 15)

			matrix = COLOR_MATRIX[y % 2][x % 3]
			rgb = (matrix[0] * value, matrix[1] * value, matrix[2] * value)
			image.putpixel((x, y), rgb)

	image.save(os.path.join(sys.argv[2], '%05d.bmp' % framenum))
	framenum += 1
