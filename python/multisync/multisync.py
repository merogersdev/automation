#! /usr/bin/env python3

# Version 1.0

import os
from multiprocessing import Pool, cpu_count
import subprocess
import sys
import re
import logging


def multisync(processes, flags, src, dest, logger):
    try:
        rsync_cmd = subprocess.call(
            ["rsync", flags, src, dest])
        with Pool(processes=processes) as pool:
            pool.map(rsync_cmd, get_filelist(src))
        pool.join()
        logger.info(
            "Rsync from {} to {} completed successfully".format(src, dest))
    except subprocess.CalledProcessError as e:
        logger.error("Error Code: {}\n Details: {}".format(
            e.returncode, e.output))
        return 1


def get_filelist(src):
    directories = next(os.walk(src))[1]
    directory_paths = [os.path.join(src, directory)
                       for directory in directories]
    return directory_paths


def get_available_processors():
    return cpu_count()


def check_rsync_flags(flags):
    flag_regex = r"^[-ahprqvz]*$"
    return re.search(flag_regex, flags)


def setup_logging(filename):
    logger = logging.getLogger("Logger")

    log_format = "%(levelname)s | %(asctime)s | PID: %(process)d | %(filename)s:%(lineno)s\n%(message)s"
    date_format = "%Y-%m-%d %I:%M %p"

    formatter = logging.Formatter(log_format, date_format)

    log_file_handler = logging.FileHandler(filename)
    log_file_handler.setFormatter(formatter)

    logger.setLevel("INFO")
    logger.addHandler(log_file_handler)
    return logger


def main():
    # Setup logging for script
    logger = setup_logging("multisync.log")

    # Make sure I have the right number of arguments
    if len(sys.argv) != 4:
        print("Invalid number of arguments. Usage eg. ./multisync.sh -arq /src/folder/ /dest/folder/")
        return 1

    # Assign arguments to variables so calling them is easier
    flags = sys.argv[1]
    source = sys.argv[2]
    destination = sys.argv[3]

    # Quick check for common rsync flags
    if check_rsync_flags == None:
        print(
            "Flags are not recognized. Please use common flags eg: -a -h -p -r -q -v or -z")
        return 1

    # Call Rsync with multithread support
    multisync(
        get_available_processors(),
        flags,
        source,
        destination,
        logger)

    return 0


if __name__ == "__main__":
    sys.exit(main())
