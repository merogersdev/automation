#! /usr/bin/env python3

# Version 1.0

import subprocess
import datetime
import sys
import os

def main():
  # Check to make sure we have all the arguments
  if (len(sys.argv) < 3):
    print(f"Error: Invalid arguments. Usage: ./backup-linux.py /source/folder /destination/folder logfilename.txt")
    return
  
  # Set Source, Destination and Log File Name
  source_dir = sys.argv[1]
  dest_dir = sys.argv[2]
  log_filename = sys.argv[3]

  def backup(source_dir, dest_dir):
    date = datetime.datetime.now().strftime("%b %d, %Y - %I:%M %p")

    rsync_cmd = [
      "rsync",
      "-azhP",
      "--delete",
      "--exclude='node_modules'",
      "--exclude='.cache'",
      source_dir,
      dest_dir
    ]

    if not (os.path.exists(source_dir)):
      print("Error: Source folder not found. Please check path.")
      return
    
    if not (os.path.exists(dest_dir)):
      print("Error: Destination folder not found. Please check path.")
      return

    try:
      subprocess.run(rsync_cmd, stderr=subprocess.PIPE, check=True)
      with open(log_filename, "a") as log_file:
        msg = f"{date} | Backup Success\nSource: {source_dir}\nDestination: {dest_dir}\n"
        print(f"{msg}")
        log_file.write(f"{msg}\n")
    except subprocess.CalledProcessError as e:
      with open(log_filename, "a") as log_file:
        msg = f"{date} | Backup Failed \nSource: {source_dir}\nDestination: {dest_dir}\n\nError Code: {e.returncode}\nError Message: {e.stderr.decode(sys.getfilesystemencoding())}"
        print(msg)
        log_file.write(f"{msg}\n")

  backup(source_dir, dest_dir)

if __name__ == "__main__":
  main()
