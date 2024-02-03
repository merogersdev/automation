# Arch Linux Install Script

## Summary

Arch Linux automated installation script, written in Bash. Select from Gnome OR KDE OR no desktop environment. Multiple desktop environments is discouraged. For security purposes, script will prompt at the end for user and root passwords. NOTE: Script will only run in EFI Mode.

## Usage

1. Boot VM or bare metal machine with the latest Arch Linux ISO in EFI mode.
2. Download individual script to arch install environment with `curl -O https://raw.githubusercontent.com/merogersdev/automation/main/bash/arch_install/arch_install.sh`
3. Determine disk you wish to install on by running `lsblk` in terminal. Eg. sda.
4. Modify the function arguments in main to reflect disk to install to, username, hostname, package mirror countries, locale, keymap, CPU microcode, and desktop environment.
5. Make script executable `chmod +x ./arch_install.sh`
6. Run script to install arch. Will prompt at the end for passwords. `./arch_install.py`
