#! /usr/bin/bash

# Version 1.0
# Usage: ./sync.sh -flags /src/folder/ /dest/folder/

line="----------------------------------"

# Check for invalid number of arguments, and print usage instructions
check_params() {
  if (( $# < 2 || $# > 3 )); then
    echo $line
    echo
    echo "Error: Invalid usage of sync.sh"
    echo
    echo "Usage Example: ./sync.sh -azh /source/folder/ /destination/folder"
    echo
    echo $line
    exit 1
  fi
}

# Makes sure rsync is installed
check_rsync_installed() {
  rsync --version &> /dev/null
  if [ $? -ne 0 ]; then
      echo "Error: Rsync not installed. Exiting"
      exit 2
  fi
}

check_log_folder() {
  if [ ! -d ./log ]; then
    mkdir log
  fi
}

sync_folders() {
  # Param 1: flags eg. -azh
  # Param 2: Source Directory
  # Param 3: Destination Directory

  short_date=$(date '+%Y-%m')
  long_date=$(date '+%Y-%m-%d %I:%M %p')
  
  log_filename=./log/sync-$short_date.log
  exclude_filename=exclude.txt

  # Start log file
  echo $line >> $log_filename
  echo 'Sync Started:' $long_date >> $log_filename
  echo $line >> $log_filename

  # If exclude file is provided and exists, use it
  if [[ -f ./$exclude_filename ]]; then
    rsync $1 $2 $3 --stats --exclude-from=$exclude_filename 2>> $log_filename >> $log_filename
  else
    rsync $1 $2 $3 --stats 2>> $log_filename >> $log_filename
  fi

  echo >> $log_filename 
  echo $line >> $log_filename
  echo 'Sync Finished:' $long_date >> $log_filename
  echo $line >> $log_filename
  echo >> $log_filename
}

main() {
  check_params $@
  check_rsync_installed
  check_log_folder
  sync_folders $1 $2 $3
}

# Run Main Script
main $@