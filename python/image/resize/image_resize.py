#! /usr/bin/env python3
# Version 1.0

from PIL import Image
import os

supported_extensions = (".jpg", ".jpeg", ".png")


def resize_images(input_dir, output_dir, width, height):
    # Resize images in directory and output them to
    for file in os.listdir(input_dir):
        if file.endswith(supported_extensions):
            image = Image.open(os.path.join(input_dir, file))
            filename, _ = os.path.splitext(file)
            image.thumbnail((width, height))
            new_width, new_height = image.size
            new_filename = f"{filename}_{new_width}x{new_height}.png"
            image.save(os.path.join(output_dir, new_filename))


def main():
    resize_images("./in/", "./out/", 1024, 768)


if __name__ == "__main__":
    main()
