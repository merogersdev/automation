# PowerShell Backup (Windows)

## Summary

Simple PowerShell script to backup files from one directory to another. Script runs multithreaded, depending on how many virtual processors are available. Errors are logged when they happen.

## Flags

- (-src) Source Directory (Eg: C:\Users\User)
- (-dest) Destination Directory

## Usage

### Manual

1. In Terminal or Powershell, run the script and bypass restrictions `powershell -ExecutionPolicy Bypass -File .\backup.ps1 -src C:\Users\User -dest C:\Backup\User`

### User Scheduled Task (Weekly Backup/Sync)

1. Open Task Scheduler and Create Basic Task
2. Set name and description for task
3. Select Weekly for when you want the task to start
4. Select Sunday, and set time to when you will likely not be using your PC - eg. 1:00:00 AM
5. Select Start a program
6. Setup Script Parameters
7. In Program/script: type `powershell`
8. In Add arguments (optional): type `-ExecutionPolicy Bypass -File .\backup.ps1 -src C:\Users\User -dest C:\Backup\User`, substituting source and destination directory for ones of your choosing.
9. In Start in (optional): type the location of the script eg. `C:\Users\User\automation\powershell\backup\`
