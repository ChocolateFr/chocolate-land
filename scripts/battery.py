import psutil
import subprocess
from time import sleep


def alert(msg):
    subprocess.run([
        'notify-send',
        '-a',
        'Power Manager',
        msg
    ])

alert("Battery health system started.")

plugged_said = False
said = 0
op_said = 0
while True:    
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    if not plugged and plugged_said:
        alert('Battery is plugged out.')
        plugged_said = False
    elif plugged and not plugged_said:
        plugged_said = True
        alert('Battery is plugged in.')
    elif percent < 30 and said == 0:
        alert('Battery is low.')
        said += 1
    elif percent < 5 and said == 1:
        said += 1
        alert('Critical Battery Level.')
    elif percent >= 80 and op_said == 0 and plugged:
        op_said = 1
        alert('Battery is full, plug out the charger.')
    if percent < 80:
        op_said = 0

    sleep(0.35)
