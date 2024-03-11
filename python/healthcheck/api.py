from flask import Blueprint, jsonify
from healthcheck import check_reboot_status, check_cpu_loadavg, check_cpu_threshold, check_internet_connectivity, check_memory_usage, check_swap_usage, check_disk_usage

api = Blueprint(__name__, "api")


@api.route('/')
def home():
    # Set status code for response
    status_code = 200

    # Disk
    disk_over, percent_free, percent_used, gb_free, gb_total = check_disk_usage(
        "/", 50)
    swap_over, swap_usage = check_swap_usage(70)

    # CPU
    cpu_usage_over, cpu_usage = check_cpu_threshold(70)
    cpu_avg_over, cpu_avgs = check_cpu_loadavg(90)

    # Memory
    memory_over, memory_usage = check_memory_usage(70)

    # System
    requires_reboot = check_reboot_status()
    internet = check_internet_connectivity(
        "8.8.8.8", 443, 1)

    # Response
    response = {
        "disk": {
            "disk_over": disk_over,
            "percent_free": percent_free,
            "percent_used": percent_used,
            "gb_free": gb_free,
            "gb_total": gb_total,
            "swap_over": swap_over,
            "swap_usage": swap_usage
        },
        "cpu": {
            "usage": cpu_usage,
            "over": cpu_usage_over,
            "load_avg": {
                "one_min": cpu_avgs[0],
                "five_min": cpu_avgs[1],
                "fifteen_min": cpu_avgs[2],
            },
            "load_avg_over": cpu_avg_over
        },
        "memory": {
            "over": memory_over,
            "usage": memory_usage
        },
        "system": {
            "reboot": requires_reboot,
            "internet": internet
        }
    }

    return jsonify(response), status_code
