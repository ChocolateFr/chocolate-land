import os
import subprocess
from log import logging
import os

class Home:
    def __init__(self) -> None:
        self.home = os.path.expanduser('~')
    
    def __getitem__(self, items):
        if not isinstance(items, tuple):
            return os.path.join(self.home, items)
        else:
            return os.path.join(self.home, *items)


    def ensure(self, path):
        abspath = os.path.join(self.home, path)
        if os.path.exists(abspath):
            if os.path.isfile(abspath):
                os.remove(abspath)
        else:
            os.makedirs(abspath, exist_ok=True)
        return True
    
    def write(self, filePath, buffer, mode='+w'):
        self.ensure(os.path.dirname(filePath))
        with open(self[filePath], mode) as fp:
            fp.write(buffer)

    def read(self, filePath):
        return open(filePath, '+r').read()


def cmd(command):
    logging.info(f'Running the command: {command}')
    subprocess.run(
        command.split(' '),
        text=True,
    )
    return 'ok'
