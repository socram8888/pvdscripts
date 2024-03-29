
VideoNow Python codec
=====================

This is a quick and dirty, awful Python 3 set of scripts that are designed to encode, mux, decode
and demux videos for Hasbro's VideoNow Color player.

Modules
-------
- [FFmpeg](https://ffmpeg.org/)

- [pillow](https://python-pillow.org/)

Usage
-----

### Setup

```
# Install the Pillow image library.
python3 -m pip install pillow

# Create folder to store video frames.
mkdir frames
```

### Encoding

```
# Extract frames, cropped to the appropiate resolution and frames per second.
ffmpeg -i input.mp4 -filter:v scale=w=216:h=160:force_original_aspect_ratio=increase,crop=216:160,fps=18 frames/%05d.bmp

# Convert into the proprietary bitstream. This is painfully slow.
python encodeframes.py frames input_video.raw

# Extract audio in the appropiate format.
ffmpeg -i input.mp4 -f u8 -ac 2 -ar 17640 -acodec pcm_u8 input_audio.raw

# Mux the video and audio.
python3 mux.py --video input_video.raw --audio input_audio.raw --output input_muxed.wav

# Demux the video and audio.
python3 demux.py input_muxed.wav

You'd be left with a WAVE audio file, containing the video and audio.
```

### Decoding

```
# Extract video frames from raw video file.
python3 dumpframes.py input_video.raw frames

You'd left with the video frames in bitmap format, which can then be re-encoded into a readable video file.
```

Bitstream documentation
-----------------------

An up-to-date version can be found [in my website](https://orca.pet/videonow/).
