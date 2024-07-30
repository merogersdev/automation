#! /usr/bin/env python3

# Version 1.7

import logging
from sys import argv, exit, stdout
import os
from shutil import which

from video import encode_all_videos_for_roku


def main():
    def setup_logger(name):
        log_format = "%(levelname)s | %(asctime)s | %(message)s"
        date_format = "%Y-%m-%d %I:%M %p"
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        filehandler = logging.FileHandler("encoder.log")
        handler = logging.StreamHandler(stdout)
        formatter = logging.Formatter(log_format, date_format)
        handler.setFormatter(formatter)
        filehandler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(filehandler)

        setup_logger('Encoder')

    logger = logging.getLogger('Encoder')

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
