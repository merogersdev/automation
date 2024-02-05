#! /usr/bin/env python3

# Version 1.4

import os
import re
import subprocess
from shutil import which
import sys


def encode_video_roku(input_file, output_file):
    # Encode video for Roku Devices
    # Video: x264 8-bit crf 22
    # Audio Track 1: aac stereo 128k
    # Audio Track 2: aac 5.1 256k
    # Subtitle Track: Passthrough

    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-map",
        "0:0",
        "-map",
        "0:1",
        "-c:v",
        "libx264",
        "-crf",
        "22",
        "-vf",
        "format=yuv420p",
        "-map",
        "0:a",
        "-c:a:0",
        "aac",
        "-b:a:0",
        "128k",
        "-ac:a:0",
        "2",
        "-c:a:1",
        "aac",
        "-b:a:1",
        "256k",
        "-ac:a:1",
        "6",
        "-n",
        output_file
    ]

    # Run ffmpeg encode as Subprocess
    subprocess.run(ffmpeg_cmd, check=True)


def rename_video(file, encoder_info):
    episode_regex = '\w{1}\d{2}\w{1}\d{2}'
    episode = re.search(episode_regex, file)

    year_regex = '\d{4}'
    year = re.search(year_regex, file)

    if episode != None:
        file_segments = re.split(episode_regex, file)
        return f"{file_segments[0]}{episode.group()}{encoder_info}"
    file_segments = re.split(year_regex, file)
    return f"{file_segments[0]}{year.group()}{encoder_info}"


def get_resolution(filename):
    has_resolution = re.search(r"\.\d{3,4}p\.", filename)

    if has_resolution != None:
        return has_resolution.group()[1:-1]
    return "."


def sort_files(directory):
    with os.scandir(directory) as entries:
        sorted_entries = sorted(entries, key=lambda entry: entry.name)
        sorted_items = [entry.name for entry in sorted_entries]
    return sorted_items


def encode_all_videos_for_roku(in_folder, out_folder):
    try:
        for file in sort_files(in_folder):
            # Skip if it isn't a video file
            if not file.endswith(('mkv', 'mp4', 'm4v')):
                print("{} is not a recognised video file. Skipping.".format(file))
                continue

            resolution = get_resolution(file)
            new_filename = rename_video(
                file, ".Roku.{}.Surround.x264.mp4".format(resolution))
            # Check if file is already encoded
            if (os.path.exists(os.path.join(out_folder, new_filename))):
                print("{} already encoded. Skipping".format(file))
                continue
            # Encode video
            encode_video_roku(os.path.join(in_folder, file),
                              os.path.join(out_folder, new_filename))
            # Cleanup
            os.remove(os.path.join(in_folder, file))
            print("Successfully encoded video {}.\nOriginal file {} deleted.".format(
                new_filename, file))

    except subprocess.CalledProcessError as e:
        print("Error Code: ".format(e.returncode),
              "Details: ".format(e.output))
        sys.exit(e.returncode)


def main():
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Invalid arguments specified.\nUsage: ./encoder.py /in/folder/ /out/folder")
        sys.exit(1)

    in_folder = sys.argv[1]
    out_folder = sys.argv[2]

    # check ffmpeg
    if which("ffmpeg") is None:
        print("Cannot find ffmpeg. Please install package.")
        sys.exit(1)

    # check if in exists and there are files in it
    if not os.path.exists(in_folder):
        print("Cannot read from input folder. Please recheck path.")
        sys.exit(1)

    # check for out folder
    if not os.path.exists(out_folder):
        print("Cannot read from output folder. Please recheck path.")
        sys.exit(1)

    # loop through only video files and encode/rename/output to out dir
    encode_all_videos_for_roku(in_folder, out_folder)

    sys.exit(0)


# Allows importing as module without executing
if __name__ == "__main__":
    main()
