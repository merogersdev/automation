#! /usr/bin/env python3

# Version 1.7.1

from sys import argv, exit
import os
from shutil import which

from video import encode_all_videos_for_roku
from log import logger


def main():
    print(argv)

    # Check for correct number of arguments
    if len(argv) != 3:
        logger.critical(
            "Invalid arguments specified.\nUsage: ./encoder.py /in/folder/ /out/folder")
        exit(1)

    in_folder = argv[1]
    out_folder = argv[2]

    # check ffmpeg
    if which("ffmpeg") is None:
        logger.critical("Cannot find ffmpeg. Please install package.")
        exit(1)

    # check if in exists and there are files in it
    if not os.path.exists(in_folder):
        logger.critical("Cannot read from input folder. Please recheck path.")
        exit(1)

    # check for out folder
    if not os.path.exists(out_folder):
        logger.critical("Cannot read from output folder. Please recheck path.")
        exit(1)

    # loop through only video files and encode/rename/output to out dir
    encode_all_videos_for_roku(in_folder, out_folder, logger)

    exit(0)


if __name__ == "__main__":
    main()
