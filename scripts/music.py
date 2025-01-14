import os
import subprocess

# Automatically detect the home directory
home_dir = os.path.expanduser("~")
music_dir = os.path.join(home_dir, "Music")
scripts_dir = os.path.join(home_dir, ".config", "scripts")
os.chdir(scripts_dir)

def menu(*args):
    args = "\n".join(args)
    out = subprocess.run(
            ['rofi','-theme-str','configuration { show-icons: false; } listview{columns:1;}', '-dmenu'], input=args.encode(), capture_output=True
    )
    return out.stdout.strip().decode()

# List music files in the Music directory
musics = os.listdir(music_dir)
musics = [' ' + i.replace('-', ' ').replace('_', ' ').split('.')[0] for i in musics]
musics = ['Exit', 'Stop'] + musics

# Display menu
select = menu(*musics)

# Exit if nothing is selected
if not select or select == 'Exit':
    quit()

try:
    # Kill the last playing process if any
    with open("lastpid", "r") as f:
        last_pid = int(f.read().strip())
        subprocess.run(['kill', '-9', str(last_pid)])
except FileNotFoundError:
    pass  # No previous process was running
except ValueError:
    pass  # File was empty or contained invalid data

if select == 'Stop':
    quit()

# Play the selected music file
selected_file = os.listdir(music_dir)[musics.index(select) - 2]
process = subprocess.Popen([
    'mpv',
    os.path.join(music_dir, selected_file),
    '--loop',
    '--no-video'
])

# Save the process ID of the player
with open("lastpid", "w") as f:
    f.write(str(process.pid))
subprocess.run([
    'notify-send',
    'Now playing:',
    select[2:]
])
