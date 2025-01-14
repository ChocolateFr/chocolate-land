import subprocess
import json
import os
import sys
from time import sleep
from base64 import b64encode, b64decode

# Automatically detect the home directory
home_dir = os.path.expanduser("~")
config_dir = os.path.join(home_dir, ".config", "scripts")
os.chdir(config_dir)

base = config_dir
path = lambda x: os.path.join(base, x)
db_file = path("db.json")

# Ensure the database file exists
if not os.path.exists(db_file):
    with open(db_file, "w") as f:
        json.dump([], f)

db = json.load(open(db_file, "r"))
save = lambda: json.dump(db, open(db_file, "w"), indent=2)

def menu(*args):
    args = "\n".join(args)
    out = subprocess.run(
            ['rofi', '-dmenu', '-theme-str', 'configuration{show-icons:false;} listview{columns:1;}'], input=args.encode(), capture_output=True
    )
    return out

if sys.argv[1] == '--show':
    shows = [f"󰆏 {i[:30].replace('\n', ' ')}" for i in db]
    shows.reverse()
    select = menu(*shows).stdout
    shows.reverse()
    what = db[shows.index(select.strip().decode())]
    if what.startswith('󰆏 ||IMG||'):
        what = b64decode(what.replace('󰆏 ||IMG||', ''))
    else:
        what = what.encode()
    subprocess.run(['wl-copy'], input=what)

else:
    print('started')
    while True:
        copy = subprocess.run(['wl-paste'], capture_output=True).stdout.strip()
        try:
            copy = copy.decode()
        except UnicodeDecodeError:
            copy = b64encode(copy).decode()
            copy = "||IMG||" + copy
        except Exception as err:
            print(err)
        finally:
            if copy not in db:
                db.append(copy)
                db = db[-100:]  # Keep only the last 100 entries
                save()
            sleep(0.5)
