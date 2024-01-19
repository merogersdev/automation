#! /usr/bin/bash

# Check for invalid number of arguments, and print usage instructions
check_params() {
  if (( $# < 2 || $# > 3 )); then
    line="--------------------------------"
    echo $line
    echo
    echo "Error: Invalid usage of sync.sh"
    echo
    echo "Usage Example 1: without exclude folders file:"
    echo "./sync.sh /source/folder/ /destination/folder"
    echo
    echo "Usage Example 2: with exclude folders file:"
    echo "./sync.sh /source/folder/ /destination/folder ./exclude.sh"
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

sync_folders() {
  # Param 1: flags eg. -azhP
  # Param 2: Source Directory
  # Param 3: Destination Directory

  log_filename=sync-$(date +%m-%Y).log
  exclude_filename=exclude.txt

  # If exclude file is provided and exists, use it
  if [[ -f ./$exclude_filename ]]; then
    rsync $1 $2 $3 --exclude-from={$exclude_filename} --log-file=$log_filename
  else
    rsync $1 $2 $3 --log-file=$log_filename --log-file-format="%t %f %b"
  fi
}

generate_log() {
  echo $1
}

main() {
  check_params $@
  check_rsync_installed


  sync_folders -azhP ./src/ ./dest/


  # if [[ ! -f $3 || $3 != "*.txt" ]]; then
  #   echo "Error: Cannot find exclude file or it is not a .txt file. Exiting."
  #   exit 3
  # elif [[ $# == 3 ]]; then
  #   echo "Exclude create file"
  #   touch $3
  # else
  #   echo "No exclude"
  # fi

}







# Run Main Script
main $@