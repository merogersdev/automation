#! /usr/bin/env python3

# Version 1.0

import os
import re
import subprocess
from shutil import which

def main():
  episode_regex='\w{1}\d{2}\w{1}\d{2}'
  year_regex='\d{4}'
  allowed_extensions = ['mkv', 'mp4']
  roku_info = ".Roku.1080p.Surround.x264.mp4"

  def encode_video(input_file, output_file):
    ffmpeg_cmd = [
      "ffmpeg",
      "-i",
      input_file,
      "-c:v",
      "libx264",
      "-preset",
      "medium",
      "-crf",
      "22",
      "-n",
      output_file
    ]

    try:
      subprocess.run(ffmpeg_cmd, check=True)
      print(f"Encoding success for {output_file}")
    except subprocess.CalledProcessError as e:
      print(f"Encoding failed for {output_file}")
      print(f"Return Code: {e.returncode}")
      print(f"Output: {e.output}")

  # Make sure ffmpeg is installed
  if (which('ffmpeg') is None):
    print("Cannot find ffmpeg. Please install package.")
    return

  # Check if input folder exists, else create and exit
  if not (os.path.exists('in')):
    os.mkdir('in')
    print("Input folder found. Creating folder. Please run again.")
    return

  # Make sure there are files to convert, else exit
  if(len(os.listdir('in')) == 0):
    print("No files found to encode. Exiting.")
    return

  # Create output folder if not found
  if not (os.path.exists('out')):
    os.mkdir('out')

  # File List
  for file in os.listdir('in'):
    episode = re.search(episode_regex, file)
    year = re.search(year_regex, file)
    ext = file[-3:]

    if(episode != None and ext in allowed_extensions):
      file_segments = re.split(episode_regex, file)
      new_filename = f"{file_segments[0]}{episode.group()}{roku_info}"
      if (os.path.isfile(f"./out/{new_filename}")):
        print(f"./out/{new_filename} already exists. Skipping...")
        return
      encode_video(f"./in/{file}", f"./out/{new_filename}")
    elif(year != None and ext in allowed_extensions):
      file_segments = re.split(year_regex, file)
      new_filename = f"{file_segments[0]}{year.group()}{roku_info}"
      if (os.path.isfile(f"./out/{new_filename}")):
        print(f"./out/{new_filename} already exists. Skipping...")
        return
      encode_video(f"./in/{file}", f"./out/{new_filename}")
    else:
      print(file + " is not a valid video file. Skipping...")

# Allows importing as module without executing
if __name__ == "__main__":
  main()