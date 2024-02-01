# MultiSync

## Summary

Multithreaded rsync script, written in Python. Script provides a more efficient utilization of modern CPUs by spawning concurrent processes of rsync for faster file sync and backups. Includes logging.

## Usage

Script uses standard rsync flags eg. -azhp and source/destination directory format. Source folder and Destination folders must exist

`./multisync.py -azhp /source/folder/ /destination/folder`
