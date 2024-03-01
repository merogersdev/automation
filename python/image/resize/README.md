# Batch Image Resize

## Summary

Batch image processing script, useful for a wide variety of tasks including web design, efficient storage of very large images...etc.

## Setup

1. Navigate to this directiory in your terminal eg. `cd /home/user/code/automation/python/image/resize/` and create python virtual environment with `python3 -m venv .venv`
2. Install additonal packages with `python3 -m pip install -r requirements.txt`

## Flags

- (-w) Set max width of image (Default: 1024)
- (-l) Set max length/height of image (Default: 768)
- (-i) Set input directory (Default: "./in/")
- (-o) Set output directory (Default: "./out/")

## Example Usage

1. (Linux/Mac) Make sure the script is executable eg. `chmod +x image_resize.py`
2. Run script without flags eg. `./image_resize.py` for default options or run with flags `./image_resize.py -i /path/to/in/folder/ -o /path/to/out/folder/ -l 1080 -w 1920`
