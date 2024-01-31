#! /usr/bin/env python3

import os
import psutil
import shutil
import socket
import math
import sys
import datetime 

def convert_bytes_to_gigabytes(bytes):
   return math.floor(bytes / 2**30)

def check_reboot_status():
  return os.path.exists("/run/reboot-required")

def check_cpu_threshold(max_usage):
   return psutil.cpu_percent(1) > max_usage

def check_internet_connectivity(url):
  try:
    socket.gethostbyname(url)
    return False    
  except:
    return True

def get_disk_usage(disk):
  usage = shutil.disk_usage(disk)
  gb_free = convert_bytes_to_gigabytes(usage.free)
  gb_total = convert_bytes_to_gigabytes(usage.total)
  percent_free = math.floor(100 * usage.free / usage.total)
  return gb_free, gb_total, percent_free

def generate_logfile(filename):


  date = datetime.datetime.now().strftime("%b %d, %Y - %I:%M %p")


def main():

  gb_free, gb_total, percent_free = get_disk_usage("/")
  print("Free: {}GB".format(gb_free))
  print("Total: {}GB".format(gb_total))
  print("Free Space: {}%".format(percent_free))

  sys.exit(0)

if __name__ == "__main__":
  main()