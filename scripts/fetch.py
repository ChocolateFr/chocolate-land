import psutil
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
import time

console = Console()
ART = "/home/chocolatefr/Templates/ascii_arts/boykisser/little.txt"
details = dict()

def prefixer(value, rounding=2):
    prefixs = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    for j in range(len(prefixs)):
        value = value / 1024**j
        if value < 1:
            return f'{round(value * 1024**j, rounding)}{prefixs[j]}'
    return f'{value}B'

# Read ASCII art
art = open(ART).read()
art = '[blue]' + art

# Gather system information
details['󰻠 CPU'] = f"{psutil.cpu_count()} (Total), {psutil.cpu_count(False)} (Logical)"
details['󰍛 RAM'] = f"{prefixer(psutil.virtual_memory().total)} ({round(psutil.virtual_memory().used/psutil.virtual_memory().total,2)*100}%)"
details['󰋊 SSD'] = f'Total: {prefixer(psutil.disk_usage("/").total)}, Used: {prefixer(psutil.disk_usage("/").used)}, Free: {prefixer(psutil.disk_usage("/").free)}'
details['󰍹  DE'] = f'Hyprland-Catppuccin'
details[' CAT'] = 'MEOW!'

# Adding more detailed information
details['󰝣 CPU Usage'] = f"{psutil.cpu_percent()}%"  # CPU usage percentage
details['󰝧 Disk I/O'] = f"Read: {prefixer(psutil.disk_io_counters().read_bytes)}, Write: {prefixer(psutil.disk_io_counters().write_bytes)}"
details['󰛀 Network'] = f"Sent: {prefixer(psutil.net_io_counters().bytes_sent)}, Received: {prefixer(psutil.net_io_counters().bytes_recv)}"
details['󰇰 Uptime'] = f"{str(time.strftime('%H:%M:%S', time.gmtime(psutil.boot_time())))}"

# Join the details with separator
joiner = ''
l_art = len(art.split('\n'))

txt = '\n'.join([f'[blue]{i} [purple]{joiner} [white]{details[i]}' for i in details])
l_txt = len(txt.split('\n'))

# Adjust length for formatting
if l_txt < l_art:
    txt = txt + '\n' * (l_art - l_txt)
elif l_art < l_txt:
    art = art + '\n' * (l_txt - l_art)

# Create final panel with ASCII art and system details
final = Align(
    Columns([
        Panel(art),
        Panel(txt)
    ]),
    align='center'
)

# Print final result to the console
console.print(final)

