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

def pixelval(image, x, y):
	rgb = image.getpixel((x, y))
	matrix = COLOR_MATRIX[y % 2][x % 3]
	encoded = rgb[0] * matrix[0] + rgb[1] * matrix[1] + rgb[2] * matrix[2]
	return round(encoded * 15 / 255)

assert(len(sys.argv) == 3)

video = open(sys.argv[2], 'wb')
framenum = 1

while True:
	if framenum % 10 == 0:
		print(framenum)

	try:
		image = Image.open(os.path.join(sys.argv[1], '%05d.bmp' % framenum))
	except:
		break

	assert(image.mode == 'RGB')
	assert(image.size == (FRAME_WIDTH, FRAME_HEIGHT))

	buf = bytearray()
	for y in range(FRAME_HEIGHT):
		for x in range(0, FRAME_WIDTH, 2):
			buf.append(pixelval(image, x + 1, y) << 4 | pixelval(image, x + 0, y))

	video.write(buf)
	framenum += 1
