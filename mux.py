#!/usr/bin/env python3

import wave
import sys
import argparse

FRAME_SIZE = 19600
IMAGE_PER_FRAME = 17280
AUDIO_PER_FRAME = 1960
PREAMBLE = (
	b'\x81\xE3\xE3\xC7\xC7\x81\x81\xE3\xC7' * 24 +
	b'\x00\x00\x02\x01\x04\x02\x06\x03\xFF' +
	b'\x08\x04\x0A\x05\x0C\x06\x0E\x07\xFF' +
	b'\x11\x08\x13\x09\x15\x0A\x17\x0B\xFF' +
	b'\x19\x0C\x1B\x0D\x1D\x0E\x1F\x0F\xFF' +
	b'\x00\x28\x02\x29\x04\x2A\x06\x2B\xFF' +
	b'\x08\x2C\x0A\x2D\x0C\x2E\x0E\x2F\xFF' +
	b'\x11\x30\x13\x31\x15\x32\x17\x33\xFF' +
	b'\x19\x34\x1B\x35\x1D\x36\x1F\x37\xFF' +
	b'\x00\x38\x02\x39\x04\x3A\x06\x3B\xFF' +
	b'\x08\x3C\x0A\x3D\x0C\x3E\x0E\x3F\xFF' +
	b'\x11\x40\x13\x41\x15\x42\x17\x43\xFF' +
	b'\x19\x44\x1B\x45\x1D\x46\x1F\x47\xFF' +
	b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF' +
	b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF' * 3
)

parser = argparse.ArgumentParser(description='Muxes VideoNow Color streams.')
parser.add_argument('-a', '--audio', type=argparse.FileType('rb'), help='Audio file, optional')
parser.add_argument('-v', '--video', type=argparse.FileType('rb'), help='Video file', required=True)
parser.add_argument('-o', '--output', type=lambda x: wave.open(x, 'wb'), help='Output file', required=True)
args = parser.parse_args()

args.output.setnchannels(2)
args.output.setsampwidth(2)
args.output.setframerate(44100)

# Write padding data
args.output.writeframes(b'\x00' * 392)

if not args.audio:
	frameaudio = b'\x80' * AUDIO_PER_FRAME

while True:
	frameimage = args.video.read(IMAGE_PER_FRAME)
	if len(frameimage) != IMAGE_PER_FRAME:
		break

	if args.audio:
		frameaudio = args.audio.read(AUDIO_PER_FRAME)
		if len(frameaudio) != AUDIO_PER_FRAME:
			break

	frameimage = PREAMBLE + frameimage
	muxedframe = bytearray()
	for line in range(FRAME_SIZE // 10):
		muxedframe.extend(frameimage[line * 9 : (line + 1) * 9])
		muxedframe.append(frameaudio[line])

	args.output.writeframes(muxedframe)
