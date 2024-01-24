#! /usr/bin/env python3

# Version 1.1

import os
import re
import subprocess
from shutil import which
import sys

def main():
  episode_regex='\w{1}\d{2}\w{1}\d{2}'
  year_regex='\d{4}'
  allowed_extensions = {'mkv', 'mp4'}
  encoder_info = ".Roku.1080p.Surround.x264.mp4"

  def encode_video(input_file, output_file):
    ffmpeg_cmd = [
      "ffmpeg",
      "-i",
      input_file,
      "-map",
      "0:0",
      "-map",
      "0:1",
      "-map",
      "0:1",
      "-c:v",
      "libx264",
      "-preset",
      "medium",
      "-crf",
      "22",
      "-map",
      "0:a",
      "-c:a:0",
      "aac",
      "-b:a:0",
      "128k",
      "-ac:a:0",
      "2",
      "-c:a:1",
      "ac3",
      "-b:a:1",
      "256k",
      "-ac:a:1",
      "6",
      "-c:s",
      "mov_text",
      "-n",
      output_file
    ]

    try:
      subprocess.run(ffmpeg_cmd, check=True)
      print(f"Encoding success for {output_file}")
      #os.remove(f"./in/{file}")
    except subprocess.CalledProcessError as e:
      print(f"Encoding failed for {output_file}")
      print(f"Return Code: {e.returncode}")
      print(f"Output: {e.output}")
      os.remove(f"./out/{output_file}")
      sys.exit(1)

  # Make sure ffmpeg is installed
  if (which('ffmpeg') is None):
    print("Cannot find ffmpeg. Please install package.")
    sys.exit(2)

  # Check if input folder exists, else create and exit
  if not (os.path.exists('in')):
    os.mkdir('in')
    print("Input folder found. Creating folder. Please add media and run again.")
    sys.exit(3)

  # Make sure there are files to convert, else exit
  if(len(os.listdir('in')) == 0):
    print("No files found to encode. Exiting.")
    sys.exit(4)

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
      new_filename = f"{file_segments[0]}{episode.group()}{encoder_info}"
      if (os.path.isfile(f"./out/{new_filename}")):
        print(f"./out/{new_filename} already exists. Skipping...")
      else:
        encode_video(f"./in/{file}", f"./out/{new_filename}")

    elif(year != None and ext in allowed_extensions):
      file_segments = re.split(year_regex, file)
      new_filename = f"{file_segments[0]}{year.group()}{encoder_info}"
      if (os.path.isfile(f"./out/{new_filename}")):
        print(f"./out/{new_filename} already exists. Skipping...")
      else:
        encode_video(f"./in/{file}", f"./out/{new_filename}")
        
    else:
      print(file + " is not a valid video file. Skipping...")
  sys.exit(0)

# Allows importing as module without executing
if __name__ == "__main__":
  main()