# PowerShell Backup Script with RoboCopy
# Version 1.0

# Command-Line Parameters
Param (
  [string]$src = $env:USERPROFILE,
  [string]$dest = "C:\Backup\$($env:UserName)"
)

$ScriptBlock = {
  # Log File
  $LogFile = "backup.log"

  # Main Function
  function Main {
    Write-Host "RoboCopy - Start"
    New-Item -ItemType Directory -Force -Path $dest
    ExecuteRoboCopy
    Write-Host "RoboCopy - End"
  }

  # Helpers
  function GetThreadCount {
    $processor = Get-ComputerInfo -Property CsProcessors
    $threads = $processor.CsProcessors.NumberOfLogicalProcessors
    return $threads
  }

  function ExecuteRoboCopy {
    robocopy $src $dest /E /R:0 /W:0 /COPY:DAT /DCOPY:DAT /MT:$(GetThreadCount) /NFL /NDL /NJH /NJS /NS /NC /NP /Log+:$LogFile
  }

  Main
}


# Run Script
Invoke-Command -ScriptBlock $ScriptBlock -ArgumentList $src,$dest,$cn -ErrorAction SilentlyContinue

