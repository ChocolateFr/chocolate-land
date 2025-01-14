import subprocess
import sys
import watchdict
import os

# Automatically detect the home directory
home_dir = os.path.expanduser("~")
config_dir = os.path.join(home_dir, ".config", "scripts")

# Change directory to the config scripts folder
os.makedirs(config_dir, exist_ok=True)
os.chdir(config_dir)

# Initialize WatchDict with save.json
db = watchdict.WatchDict('save.json')

def menu(*args):
    args = "\n".join(args)
    out = subprocess.run(
        ['rofi', '-dmenu',"-theme-str",'configuration{show-icons:false;} listview{columns:2;}'], input=args.encode(), capture_output=True
    )
    return out.stdout.strip().decode()

# Command-line argument handling
if len(sys.argv) < 2:
    print("Usage: script.py [save|delete|menu] [key] [value]")
    sys.exit(1)

if sys.argv[1] == 'save':
    if len(sys.argv) < 4:
        print("Usage: script.py save <key> <value>")
        sys.exit(1)
    db[sys.argv[2]] = sys.argv[3]
elif sys.argv[1] == 'delete':
    if len(sys.argv) < 3:
        print("Usage: script.py delete <key>")
        sys.exit(1)
    db.pop(sys.argv[2], None)
    db.commit()
else:
    selected_key = menu(*db.keys())
    if selected_key:
        subprocess.run(['wl-copy'], input=db[selected_key].encode())
