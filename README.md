# datamoshing

a collection of datamoshing scripts i use in my art. although there are
most likely infinite ways to achieve the datamoshing effect, i have found that
random byte corruption in jpeg and mp4 formats produce an easy-to-produce effect
that is visually meaningful. this is due to the fact that these file formats
are compressed; randomly corrupting bytes in a compressed file can have complex,
chaotic (in the mathematical sense) effects on the output.

## corrupt_png.py

*requirements: jpeginfo, python (+ python dependencies)*

a tool to create a "glitched" effect on JPG images by randomly corrupting bytes
and using jpeginfo to ensure the result is still viewable.

## corrupt_mp4.py

*requirements: ffmpeg, python (+ python dependencies)*

a tool to create a "glitched" effect on MP4 video files by randomly corrupting
bytes and using ffmpeg to ensure the result is still playable.
