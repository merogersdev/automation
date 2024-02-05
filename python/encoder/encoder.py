#! /usr/bin/env python3

# Version 1.6

import os
import re
import subprocess
from shutil import which
import sys
import logging


def setup_logger(name):
    log_format = "%(levelname)s | %(asctime)s | %(message)s"
    date_format = "%Y-%m-%d %I:%M %p"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    filehandler = logging.FileHandler("encoder.log")
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(log_format, date_format)
    handler.setFormatter(formatter)
    filehandler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(filehandler)


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
    # Renames video based on type of file - eg. tv episode or video
    episode_regex = r"\w{1}\d{2}\w{1}\d{2}"
    episode = re.search(episode_regex, file)
    year_regex = r"\d{4}"
    year = re.search(year_regex, file)
    special_regex = r"[^\w\d\.]*"

    replacements = [
        (" ", "."),
        (special_regex, "")
    ]

    if episode != None:
        file_segments = re.split(episode_regex, file)
        new_title = file_segments[0]
        for old, new in replacements:
            new_title = re.sub(old, new, new_title)
        return f"{new_title}{episode.group()}{encoder_info}"
    file_segments = re.split(year_regex, file)
    new_title = file_segments[0]
    for old, new in replacements:
        new_title = re.sub(old, new, new_title)
    return f"{new_title}{year.group()}{encoder_info}"


def get_resolution(filename):
    # Looks for HD formats in file or returns a . for standard/unknown definition so filename can be structured correctly
    hd_regex = r"\.?(1080p|720p|2160p|4[kK])\.?"
    has_resolution = re.search(hd_regex, filename)

    if has_resolution != None:
        resolution = has_resolution.group()
        resolution = re.sub(r"\.", "", resolution)
        return f".{resolution}."
    return "."


def sort_files(directory):
    # Sorts files alphabetically
    with os.scandir(directory) as entries:
        sorted_entries = sorted(entries, key=lambda entry: entry.name)
        sorted_items = [entry.name for entry in sorted_entries]
    return sorted_items


def encode_all_videos_for_roku(in_folder, out_folder, logger):
    try:
        for file in sort_files(in_folder):
            # Skip if it isn't a video file
            if not file.endswith(('mkv', 'mp4', 'm4v')):
                logger.info(
                    f"{file} is not a recognised video file. Skipping.")
                continue

            resolution = get_resolution(file)
            new_filename = rename_video(
                file, f".Roku{resolution}Surround.x264.mp4")
            # Check if file is already encoded
            if (os.path.exists(os.path.join(out_folder, new_filename))):
                logger.info(f"{file} already encoded. Skipping")
                continue
            # Encode video
            encode_video_roku(os.path.join(in_folder, file),
                              os.path.join(out_folder, new_filename))
            # Cleanup
            os.remove(os.path.join(in_folder, file))
            logger.info(
                f"Successfully encoded video {new_filename}.\nOriginal file {file} deleted.")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error Details: {e.output}")
        sys.exit(e.returncode)


def main():
    # Setup logging
    setup_logger('Encoder')
    logger = logging.getLogger('Encoder')

    # Check for correct number of arguments
    if len(sys.argv) != 3:
        logger.critical(
            "Invalid arguments specified.\nUsage: ./encoder.py /in/folder/ /out/folder")
        sys.exit(1)

    in_folder = sys.argv[1]
    out_folder = sys.argv[2]

    # check ffmpeg
    if which("ffmpeg") is None:
        logger.critical("Cannot find ffmpeg. Please install package.")
        sys.exit(1)

    # check if in exists and there are files in it
    if not os.path.exists(in_folder):
        logger.critical("Cannot read from input folder. Please recheck path.")
        sys.exit(1)

    # check for out folder
    if not os.path.exists(out_folder):
        logger.critical("Cannot read from output folder. Please recheck path.")
        sys.exit(1)

    # loop through only video files and encode/rename/output to out dir
    encode_all_videos_for_roku(in_folder, out_folder, logger)

    sys.exit(0)


# Allows importing as module without executing
if __name__ == "__main__":
    main()
