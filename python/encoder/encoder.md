# Video Encoder Script

## Summary

This python script uses ffmpeg to automate the task of determining which files are video files in a particular directory, renaming them, re-encoding them and outputting the result into another folder. Currently has preset to work with Roku devices. Once the files are successfully transcoded, the originals are deleted.

## Usage

Pass both the folder with videos and the folder to store the transcoded files. Both folders need to exist before the script will transcode.

1. Make script executable - eg.
   `chmod +x ./encoder.py`
2. Run Script - eg.
   `./encoder.py /in/folder/ /out/folder/`
