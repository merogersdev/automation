# Health Check Script (Linux)

# Summary

Gets and logs system health issues for Linux systems including internet connectivity, cpu load average, cpu temperature, disk usage, reboot status, memory usage and swap usage.

# Usage

Out of the box, script provides health checks for enough free space on root, cpu load average, cpu temperature, internet connectivity, memory usage and reboot status for most systems. Can be run standalone or as a cron job.

1. Make script executable
   `chmod +x ./healthcheck.py`
2. Run script to generate a log of potential system issues.
   `./healthcheck.py`
