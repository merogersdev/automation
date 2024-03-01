#! /usr/bin/env python3
# Version 1.0

import os
import sys
import argparse
from PIL import Image
import logging

parser = argparse.ArgumentParser(
    description="Resizes all image files in given directory")

parser.add_argument("-i",
                    "--input",
                    nargs="?",
                    type=str,
                    action="store",
                    default="./in/",
                    help='Enter input folder path')

parser.add_argument("-o",
                    "--output",
                    nargs="?",
                    type=str,
                    action="store",
                    default="./out/",
                    help="Enter output folder path")

parser.add_argument("-w",
                    "--width",
                    nargs="?",
                    type=int,
                    action="store",
                    default=1024,
                    help="Enter output image width")

parser.add_argument("-l",
                    "--length",
                    nargs="?",
                    type=int,
                    action="store",
                    default=768,
                    help="Enter output image /width")

args = parser.parse_args()

supported_extensions = (".jpg", ".jpeg", ".png")


def setup_logging(filename):
    # Logger with custom formatting for both file and terminal logging. Filename indicates log file
    logger = logging.getLogger("Image Resize")

    log_format = "%(levelname)s | %(asctime)s | PID: %(process)d | %(filename)s:%(lineno)s\n%(message)s"
    date_format = "%Y-%m-%d %I:%M %p"

    formatter = logging.Formatter(log_format, date_format)

    log_file_handler = logging.FileHandler(filename)
    log_file_handler.setFormatter(formatter)

    logger.setLevel("INFO")
    logger.addHandler(log_file_handler)
    return logger


def resize_images(input_dir, output_dir, width, height):
    resized_images = 0
    for file in os.listdir(input_dir):
        if file.endswith(supported_extensions):
            image = Image.open(os.path.join(input_dir, file))
            filename, _ = os.path.splitext(file)
            image.thumbnail((width, height))
            new_width, new_height = image.size
            new_filename = f"{filename}_{new_width}x{new_height}.png"
            image.save(os.path.join(output_dir, new_filename))
            resized_images += 1
    return resized_images


def main(args):
    logger = setup_logging("image_resize.log")

    if not os.path.exists(args.input):
        logger.critical(f"Input folder {args.input} does not exist")
        return 1

    if not os.path.exists(args.output):
        logger.critical(f"Output Folder {args.output} does not exist")
        return 1

    try:
        total = resize_images(args.input, args.output, args.width, args.length)
        logger.info(f"Total Images successfully resized: {total}")
        return 0
    except Exception as e:
        logger.error(f"Error: {type(e).__name__} - {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(args))
