# Development Environment Automated Installer (Ubuntu)

## Summary

This bash script is meant to automate the setup and installation of various Web Developer programs. Script is last tested on Kubuntu 23.10, and doesn't depend on any particular Desktop Environment.

Dev Setup script is designed to be modular, so pick and choose what you wish to install before running script. Additional instructions below.

#NOTE: Script is intended for Ubuntu and Ubuntu-based linux distributions. Will not work on Fedora or Arch-based distributions without some modifications.

## Usage

1. Make the script executable eg. `chmod +x dev_setup.sh`
2. Uncomment the functions you wish to use in main() and save. Current Options:
   1. Download and install Google Chrome
   2. Download and install the Hack Nerd Font
   3. Download and install additional useful packages
   4. Download and install VS Code
   5. Download and install VS Code extensions typical for a full-stack developer
   6. Set VS Code User Settings from supplied settings.json file
   7. Download and install Node Version Manager
   8. Download, install and enable Docker Community Edition
   9. Download and configure bash to use a custom, minimal prompt with git branch detection
3. Run script eg. `./dev_setup.sh`
