#! /usr/bin/env python3

import os
import psutil
import shutil
import socket
import math
import sys
import logging
import re


def setup_logging(filename):
    # Logger with custom formatting for both file and terminal logging. Filename indicates log file
    logger = logging.getLogger("HealthCheck")

    log_format = "%(levelname)s | %(asctime)s | PID: %(process)d | %(filename)s:%(lineno)s\n%(message)s"
    date_format = "%Y-%m-%d %I:%M %p"

    formatter = logging.Formatter(log_format, date_format)

    log_file_handler = logging.FileHandler(filename)
    log_file_handler.setFormatter(formatter)

    logger.setLevel("INFO")
    logger.addHandler(log_file_handler)
    return logger


def convert_bytes_to_gigabytes(bytes):
    # Converts bytes to GB
    return math.floor(bytes / 2**30)


def check_reboot_status():
    # Checks if system requires reboot
    return os.path.exists("/run/reboot-required")


def check_cpu_threshold(max_percent):
    # Checks to see if cpu is below threshold
    return psutil.cpu_percent(1) > max_percent


def check_cpu_loadavg(max_percent):
    # Checks cpu load average is below threshold for 1,5,15 Min intervals
    cpu_count = psutil.cpu_count()
    avgs = [percent / cpu_count * 100 for percent in psutil.getloadavg()]

    # Round
    roundavgs = [round(avg) for avg in avgs]

    # Returns True if any load threshold is reached
    for avg in roundavgs:
        if avg > max_percent:
            return roundavgs

    return False


def check_cpu_temp_acpi(max_temp):
    # Gets CPU Temp for ACPI Devices - Linux Only
    try:
        return psutil.sensors_temperatures()['acpitz'][0].current > max_temp
    except:
        return True


def check_cpu_temp_pi(max_temp):
    # Gets CPU Temp for Raspberry Pi - Linux Only
    try:
        return psutil.sensors_temperatures()['cpu_thermal'][0].current > max_temp
    except:
        return True


def check_cpu_temp_generic(max_temp):
    # Gets CPU Temp for any supported linux system. Relatively expensive function - Use if other cpu checks don't work.
    rootdir = "/sys/class/thermal/"
    regex = "thermal_zone\d{1}"

    zones = []
    temps = []

    try:
        # Get all thermal zones for system
        for _, dirs, _ in os.walk(rootdir):
            for dir in dirs:
                if re.match(regex, dir):
                    zones.append(dir)

        # Get all temperature values in each zone
        for zone in zones:
            filename = f"{rootdir}{zone}/temp"
            with open(filename, "r") as file:
                for line in file:
                    temps.append(int(line.strip()))

        # Make sure no temps succeed max temp
        for temp in temps:
            if temp > max_temp:
                return True
        return False
    except:
        return True


def check_memory_usage(max_percent):
    # Checks if system memory usage is below threshold
    return psutil.virtual_memory().percent > max_percent


def check_swap_usage(max_percent):
    # Checks swap area usage is below threshold
    return psutil.swap_memory().percent > max_percent


def check_internet_connectivity(url):
    # Checks for connectivity to given URL
    try:
        socket.gethostbyname(url)
        return False
    except:
        return True


def get_disk_usage(disk):
    # Gets disk usage for given disk/partition/mount point
    usage = shutil.disk_usage(disk)
    gb_free = convert_bytes_to_gigabytes(usage.free)
    gb_total = convert_bytes_to_gigabytes(usage.total)
    percent_free = math.floor(100 * usage.free / usage.total)
    return gb_free, gb_total, percent_free


def main():
    logger = setup_logging("healthcheck.log")

    # Gets usage for root disk
    _, _, percent_free = get_disk_usage("/")

    # Warning log if free space less than 25%
    if percent_free < 50:
        logger.warning(f"Free space on / is currently at {percent_free}%")

    # Critical log free space is less than 10%
    if percent_free < 25:
        logger.critical(
            f"Free space on / is currently at {percent_free}%".format(percent_free))

    # Warning log if system requires reboot
    requires_reboot = check_reboot_status()
    if requires_reboot == True:
        logger.warning("System requires reboot")

    # Checks CPU usage is below threshold, warning log if not
    high_cpu_usage = check_cpu_threshold(70)
    if high_cpu_usage == True:
        logger.warning(
            f"High CPU usage detected. Usage currently at {str(high_cpu_usage)}%")

    # Check if CPU temp (ACPI) is below threshold or can be read
    cpu_overheating = check_cpu_temp_acpi(80)

    if cpu_overheating == True:
        logger.critical("CPU is overheating or value cannot be read.")

    # Checks internet connectivity
    is_connected = check_internet_connectivity("https://google.ca")
    if not is_connected:
        logger.critical("No internet connectivity.")

    # Check overall system load
    avgs = check_cpu_loadavg(70)
    if avgs != False:
        logger.warning(
            f"High CPU Usage: 1 Min: {avgs[0]}%, 5 Min: {avgs[1]}%, 15 Min: {avgs[2]}%")

    # Checks overall memory usage
    memory_usage = check_memory_usage(70)
    if memory_usage == True:
        logger.warning("High memory usage detected.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
