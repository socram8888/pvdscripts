
VideoNow Python codec
=====================

This is a quick and dirty, awful Python 3 set of scripts that are designed to encode, mux, decode
and demux videos for Hasbro's VideoNow Color player.

Usage
-----

### Encoding

```
# Create a virtual environment
virtualenv -p python3 venv

# Enable the virtual environment
source venv/bin/activate

# Install the Pillow image library
python3 install pillow

# Create folder to store video frames
mkdir -p camel_frames

# Extract frames, cropped to the appropiate resolution and frames per second
ffmpeg -i camel_original.webm -filter:v scale=w=216:h=160:force_original_aspect_ratio=increase,crop=216:160,fps=18 camel_frames/%05d.bmp

# Convert into the proprietary bitstream. This is painfully slow.
python encodeframes.py camel_frames camel_video.bin

# Extract audio in the appropiate format
ffmpeg -i camel_original.webm -f u8 -ac 2 -ar 17640 -acodec pcm_u8 camel_audio.bin

# Mux video and audio
python mux.py --video camel_video.bin --audio camel_audio.bin --output camel_muxed.wav
```

You'd be left with a WAVE audio file, containing the video and audio.

Recording onto real media
-------------------------

The VideoNow uses proprietary media and has some requirements:

 - The video length must be at least 1240 seconds (or about 21 minutes).
 - The discs can be no larger than 112mm (vs the 120mm of a standard, off-the-shelf CD-R).
 - First and last tracks are checked and may not be replaced or removed.

These 21 minutes of video translate to 42 minutes of audio. If the length is shorter, you'll
need to add some padding in the form of a silent audio track. This data goes __after__ the end
of disc marker track.

You can generate this padding easily using FFmpeg:
```
ffmpeg -f s16le -ac 2 -ar 44100 -i /dev/zero -ss 0 -t ${TIME} padding.wav
```

Since the recordable discs are nowadays pretty much unobtainable, you can use a standard CD-R
and _cut_ it to 108mm.

I used a commercial VideoNow disc, put on top of a normal CD-R, drew with some sharpie the outline
and then just cut it using some scissors. This leaves the disc in a structurally weak status, with
the outermost part of the reflective aluminium layer peeling off just by looking at it funny,
but since this is just an experiment for the lulz I can live with that.

A 80mm mini-disc would not work, as the do not contain enough physical space to hold the required
minimum video length. The player _seems_ to actively check the existance of this area by moving
the play head to the last track and attempting to read from it. I should check if it's possible to
fool the drive by messing with the disc's TOC.

Example layout:
  1. Fixed track with VideoNow logo (file `logo.wav` in this repository).
  2. First custom video track
  3. Second custom video track
  4. Third custom video track
  5. Fixed trailer track (file `trailer.wav` in this repository).
  6. Silent track for padding.

Bitstream format
----------------

This information has been obtained by three different sources:
  1. [A post by a man called VideoNowDude on the VideoHelp forum](https://forum.videohelp.com/threads/123262-converting-video-formats-(For-Hasbro-s-VideoNow)-I-know-the/page17#post1149694)
  2. Decompiling the official VideoNow Media Wizard application (which crashes on Windows 10, so
     don't bother trying to run it)
  3. Analyzing the bitstream of some commercial discs I have.

This device uses video with the following characteristics:
 - Video: 216x160, 4bpp, 18fps
 - Audio: stereo, PCM 8-bit unsigned at 17640Hz

First weird this about this device, which you might have noticed in the previous sections is that
the CDs are __not__ standard data discs created in ISO 9660 mode - instead, the CDs contain audio
tracks, whose samples represent the data values of the bitstream.

These tracks are read at double speed, so considering tracks are 44100Hz, stereo and contain
16-bit samples, this gives us a total of 352800 bytes per second.

This byte stream is formed of small, 10-byte chunks. Out of these chunks, 9 bytes are dedicated to
video, and the 10th byte is dedicated to audio.

```
+-------------------+---+
| V V V V V V V V V | A |
+-------------------+---+
```

These 10-byte chunks are then grouped into larger, 19600-byte frames.

Inside these frames, the audio byte of the chunks __always__ contains audio. However, in the video
part, the first 360 bytes house a fixed preamble for synchronization, rather than video data.

This header is:

```
00000000: 81E3 E3C7 C781 81E3 C7  .........
00000009: 81E3 E3C7 C781 81E3 C7  .........
00000012: 81E3 E3C7 C781 81E3 C7  .........
0000001b: 81E3 E3C7 C781 81E3 C7  .........
00000024: 81E3 E3C7 C781 81E3 C7  .........
0000002d: 81E3 E3C7 C781 81E3 C7  .........
00000036: 81E3 E3C7 C781 81E3 C7  .........
0000003f: 81E3 E3C7 C781 81E3 C7  .........
00000048: 81E3 E3C7 C781 81E3 C7  .........
00000051: 81E3 E3C7 C781 81E3 C7  .........
0000005a: 81E3 E3C7 C781 81E3 C7  .........
00000063: 81E3 E3C7 C781 81E3 C7  .........
0000006c: 81E3 E3C7 C781 81E3 C7  .........
00000075: 81E3 E3C7 C781 81E3 C7  .........
0000007e: 81E3 E3C7 C781 81E3 C7  .........
00000087: 81E3 E3C7 C781 81E3 C7  .........
00000090: 81E3 E3C7 C781 81E3 C7  .........
00000099: 81E3 E3C7 C781 81E3 C7  .........
000000a2: 81E3 E3C7 C781 81E3 C7  .........
000000ab: 81E3 E3C7 C781 81E3 C7  .........
000000b4: 81E3 E3C7 C781 81E3 C7  .........
000000bd: 81E3 E3C7 C781 81E3 C7  .........
000000c6: 81E3 E3C7 C781 81E3 C7  .........
000000cf: 81E3 E3C7 C781 81E3 C7  .........
000000d8: 0000 0201 0402 0603 FF  .........
000000e1: 0804 0A05 0C06 0E07 FF  .........
000000ea: 1108 1309 150A 170B FF  .........
000000f3: 190C 1B0D 1D0E 1F0F FF  .........
000000fc: 0028 0229 042A 062B FF  .(.).*.+.
00000105: 082C 0A2D 0C2E 0E2F FF  .,.-.../.
0000010e: 1130 1331 1532 1733 FF  .0.1.2.3.
00000117: 1934 1B35 1D36 1F37 FF  .4.5.6.7.
00000120: 0038 0239 043A 063B FF  .8.9.:.;.
00000129: 083C 0A3D 0C3E 0E3F FF  .<.=.>.?.
00000132: 1140 1341 1542 1743 FF  .@.A.B.C.
0000013b: 1944 1B45 1D46 1F47 FF  .D.E.F.G.
00000144: FFFF FFFF FFFF FFFF FF  .........
0000014d: FFFF FFFF FFFF FFFF FF  .........
00000156: FFFF FFFF FFFF FFFF FF  .........
0000015f: FFFF FFFF FFFF FFFF FF  .........
```

The MediaWizard software has this header hardcoded, so it's unlikely it contains any meaningful
data that the player extracts from it.

After this header comes the data for a singular 216x160 image, stored top to bottom, left to right,
with 4 bits per pixel, for a total of 17280 bytes.

Each byte represents the value for two pixels, with the value of even columns stored in the low
nibble, and odd pixels in the high nibble.

You might be thinking that 4 bits per pixel isn't enough to store RGB information for a pixel, and
you are right: the bitstream contains the intensity for only one of the color channels.

The reason for this is that the LCD in this device is rather primitive and uses a crude Bayer
filter on top of an already low-resolution LCD, meaning so each pixel has a fixed color, and the
bitstream just controls how bright that color is in that position of the grid.

In order to make this less noticeable, the Bayer filter uses the following pattern:

 - Even rows have pixels in a R-G-B pattern.
 - Odd rows have pixels in a G-B-R pattern.

Regarding audio, it is stored at 17640Hz stereo in PCM unsigned with 8-bits per value:
 - A zero volt signal (complete silence) is represented by 0x80.
 - A positive volt signal is represented by 0x80 + value.
 - A negative volt signal is represented by 0x80 - value.

The stream interleaves left and right channel data, with the first byte in each frame containing
the volume of the left channel, the second byte for the right, and so on.

Lastly, each track seems to have some safeguard empty space at the beginning with no video
information. The VideoHelp forum post calls for a multiple of 10, but the commercial discs I have
use only 392 bytes.
