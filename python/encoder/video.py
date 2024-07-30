
from os import path, remove
# import re
from subprocess import run, CalledProcessError
from sys import exit
from shutil import which

from utils import get_resolution, rename_video, sort_files


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
        "-stats_period",
        "5",
        "-n",
        output_file
    ]

    # Run ffmpeg encode as Subprocess
    run(ffmpeg_cmd, check=True)


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
            if (path.exists(path.join(out_folder, new_filename))):
                logger.info(f"{file} already encoded. Skipping")
                continue
            # Encode video
            encode_video_roku(path.join(in_folder, file),
                              path.join(out_folder, new_filename))
            # Cleanup
            remove(path.join(in_folder, file))
            logger.info(
                f"Successfully encoded video {new_filename}.\nOriginal file {file} deleted.")

    except CalledProcessError as e:
        logger.error(f"Error Details: {e.output}")
        exit(e.returncode)
