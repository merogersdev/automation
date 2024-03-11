# Automation Scripts

This repository stores my automation scripts. Each script has its own dedicated README file for further instructions.

## Bash

### Arch Linux Installation Script

Automated installation script to install Arch Linux, with choice of Gnome or KDE desktop environments. Includes several QOL tweaks and will prompt for passwords at the end.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/bash/arch_install/arch_install.sh)
[README](https://github.com/merogersdev/automation/blob/main/bash/arch_install/README.md)

### Developer Environment Setup

Automated installer for NVM, Docker, custom Bash Prompt, VS Code, popular VS Code extensions, VS Code user settings, Google Chrome, and the Hack Nerd Font on Ubuntu-based linux systems.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/bash/dev_setup/dev_setup.sh)
[README](https://github.com/merogersdev/automation/blob/main/bash/dev_setup/dev_setup.md)

### Custom Bash Prompt

Custom bash prompt with git branch detection. Minimal and quick to load. Useful alternative to other more complex prompts.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/bash/prompt/prompt.sh)
[README](https://github.com/merogersdev/automation/blob/main/bash/prompt/prompt.md)

### File Sync Script

Based on rsync, this script features more robust log generation and can be easily called from CRON.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/bash/sync/sync.sh)
[README](https://github.com/merogersdev/automation/blob/main/bash/sync/sync.md)

## Python

### Backup Linux

Platform-agnostic backup utilty. Coming Soon!

### Video Encoder

Batch-processing video encoder. Can detect whether videos are a movie or tv episode, rename it with encoder data, and output to a separate directory.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/python/encoder/encoder.py)
[README](https://github.com/merogersdev/automation/blob/main/python/encoder/README.md)

### Image Resize

Batch image resizing script. Resizes images in a given folder, and outputs the resized file with dimensions eg. screenshot_1920x1080.png to a separate directory. Can be run with built-in defaults or with optional flags for input directory, output directory, image width and image length/height.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/python/image/resize/image_resize.py)
[README](https://github.com/merogersdev/automation/blob/main/python/image/resize/README.md)

### Health Check (Script and Docker Dashboard)

Gets and logs system health issues for Linux systems including internet connectivity, cpu load average, cpu temperature, disk usage, reboot status, memory usage and swap usage. Can be run as a standalone script, or as a service via included dockerfile.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/python/healthcheck/healthcheck.py)
[README](https://github.com/merogersdev/automation/blob/main/python/healthcheck/README.md)

### Multisync

Multithreaded rsync script, written in Python. Script provides a more efficient utilization of modern CPUs by spawning concurrent processes of rsync for faster file sync and backups. Includes logging.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/python/multisync/multisync.py)
[README](https://github.com/merogersdev/automation/blob/main/python/multisync/README.md)

## PowerShell

### Backup Script (Windows)

Simple PowerShell script to backup files from one directory to another. Script runs multithreaded, depending on how many virtual processors are available. Errors are logged when they happen.

[CODE](https://raw.githubusercontent.com/merogersdev/automation/main/powershell/backup/backup.ps1)
[README](https://github.com/merogersdev/automation/blob/main/powershell/backup/README.md)

## Tags

![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
