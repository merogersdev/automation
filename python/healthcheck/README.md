# Health Check Script (Linux)

## Summary

Gets and logs system health issues for Linux systems including internet connectivity, cpu load average, cpu temperature, disk usage, reboot status, memory usage and swap usage.

## Usage

### Docker Service

For real-time stats on how your server is doing, a docker-based Flask application is also included. Refreshes automatically every 10 seconds.

1. Clone repo with `git clone https://github.com/merogersdev/automation.git` and navigate to ./python/healthcheck/.
2. Build docker image with `docker build --tag healthcheck .`
3. Run docker image with `docker run -d -p 5000:5000 --name healthcheck healthcheck`
4. View app in your browser `http://localhost:5000/`

### Standalone Script

Out of the box, script provides health checks for enough free space on root, cpu load average, cpu temperature, internet connectivity, memory usage and reboot status for most systems. Can be run standalone or as a cron job.

1. Clone repo or download individual script with `curl -O https://raw.githubusercontent.com/merogersdev/automation/main/python/healthcheck/healthcheck.py`
2. Make script executable
   `chmod +x ./healthcheck.py`
3. Run script to generate a log of potential system issues.
   `./healthcheck.py`
