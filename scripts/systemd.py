import psutil
import subprocess
import platform


def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    return f"CPU Usage: {cpu_usage}%\n" \
           f"CPU Frequency: {cpu_freq.current:.2f} MHz\n" \
           f"Logical Cores: {psutil.cpu_count(logical=True)}\n" \
           f"Physical Cores: {psutil.cpu_count(logical=False)}\n"


def get_memory_info():
    mem = psutil.virtual_memory()
    return f"Memory Usage: {mem.percent}%\n" \
           f"Total: {mem.total / (1024 ** 3):.2f} GB\n" \
           f"Available: {mem.available / (1024 ** 3):.2f} GB\n" \
           f"Used: {mem.used / (1024 ** 3):.2f} GB\n"


def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = ""
    for part in partitions:
        usage = psutil.disk_usage(part.mountpoint)
        disk_info += f"{part.device} ({part.mountpoint}):\n" \
                     f"  Usage: {usage.percent}%\n" \
                     f"  Total: {usage.total / (1024 ** 3):.2f} GB\n" \
                     f"  Used: {usage.used / (1024 ** 3):.2f} GB\n" \
                     f"  Free: {usage.free / (1024 ** 3):.2f} GB\n"
    return disk_info


def get_network_info():
    net_io = psutil.net_io_counters()
    return f"Network:\n" \
           f"  Bytes Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB\n" \
           f"  Bytes Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB\n"


def get_system_info():
    uname = platform.uname()
    return f"System: {uname.system}\n" \
           f"Node Name: {uname.node}\n" \
           f"Release: {uname.release}\n" \
           f"Version: {uname.version}\n" \
           f"Machine: {uname.machine}\n" \
           f"Processor: {uname.processor}\n"


def get_battery_info():
    if psutil.sensors_battery():
        battery = psutil.sensors_battery()
        return f"Battery Percentage: {battery.percent}%\n" \
               f"Power Plugged: {'Yes' if battery.power_plugged else 'No'}\n" \
               f"Time Left: {battery.secsleft // 3600}h {battery.secsleft % 3600 // 60}m\n"
    else:
        return "Battery information not available.\n"


def show_in_rofi(prompt, options):
    result = subprocess.run(
        ["rofi", "-dmenu", "-p", prompt],
        input="\n".join(options),
        text=True,
        capture_output=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


def main():
    menu_options = {
        "CPU Info": get_cpu_info,
        "Memory Info": get_memory_info,
        "Disk Info": get_disk_info,
        "Network Info": get_network_info,
        "System Info": get_system_info,
        "Battery Info": get_battery_info,
        "Exit": lambda: "Exiting..."
    }

    while True:
        choice = show_in_rofi("Select Info", list(menu_options.keys()))
        if choice in menu_options:
            if choice == "Exit":
                break
            details = menu_options[choice]()
            show_in_rofi(choice, details.splitlines())


if __name__ == "__main__":
    main()

