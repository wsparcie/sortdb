print('please wait...')

import subprocess
import sys
from os import system
from time import sleep

from database import Database

try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
    import matplotlib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'colorama'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'matplotlib'])
    print('installing modules')
finally:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
    import matplotlib
    print('importing modules')

sys.setrecursionlimit(10**9)

class Main(Database):
    def __init__(self):
        self.base = Database()

    def main(self):
        sleep(2)
        system('cls||clear')
        self.base.menu()

if __name__ == '__main__':
    Main().main()