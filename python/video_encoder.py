#! /usr/bin/env python3

import os
import re
import subprocess

episode_regex='\d{4}'
movie_regex='\d{4}'
allowed_extensions = ['mkv', 'mp4']

def convert_video(input_file, output_file):
  ffmpeg_cmd = [
    "ffmpeg",
    "-i",
    input_file,
    "-vn",
    "-acodec",
    "libmp3lame",
    "-ab",
    "192k",
    "-ar",
    "44100",
    "-y",
    output_file
  ]

  try:
    subprocess.run(ffmpeg_cmd, check=True)
    print("Conversion success")
  except subprocess.CalledProcessError as e:
    print("Conversion failed")

for file in os.listdir('in'):
  regex = re.search(episode_regex, file)
  print(file, regex)

