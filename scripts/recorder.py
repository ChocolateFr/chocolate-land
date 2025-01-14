import os
import subprocess
import signal
import time

# Automatically detect the home directory
home_dir = os.path.expanduser("~")
videos_dir = os.path.join(home_dir, "Video")
scripts_dir = os.path.join(home_dir, ".config", "scripts")
os.chdir(scripts_dir)

def menu(*args):
    args = "\n".join(args)
    out = subprocess.run(
        ['rofi', '-dmenu'], input=args.encode(), capture_output=True
    )
    return out.stdout.strip().decode()

select = menu("󰻃 Record", " Stop last one", "x Cancel")
select = select[2:]
if select == 'Record':
    # Generate a unique file name for the recording
    b = f"{time.time()}.mp4"
    s = subprocess.Popen([
        'wf-recorder',
        '--audio=alsa_output.pci-0000_03_00.6.analog-stereo.monitor',
        '-f',
        os.path.join(videos_dir, b)
    ])
    subprocess.run(['notify-send', '-a', 'Recorder', b])
    # Save the process ID for later reference
    with open("lastrec", "w") as f:
        f.write(str(s.pid))

elif select == 'Stop last one':
    # Read the process ID and send the SIGINT signal
    with open("lastrec", "r") as f:
        pid = int(f.read().strip())
    os.kill(pid, signal.SIGINT)
    subprocess.run(['notify-send', '-a', 'Recorder', 'Signal sent.'])
