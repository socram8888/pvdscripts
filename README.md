
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

Bitstream documentation
-----------------------

An up-to-date version can be found [in my website](https://orca.pet/videonow/).
