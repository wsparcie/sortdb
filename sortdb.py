print("please wait...")

import importlib.util
import subprocess
import sys
from os import system, environ
from time import sleep

from flask import Flask, jsonify
import pyroscope
from database import Database

try:
    packages = ('colorama', 'matplotlib')
    for pack in packages:
        spec = importlib.util.find_spec(pack)
        if spec is None:
            print(pack, "is not installed...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pack])
except Exception as e:
    print(e)

from colorama import just_fix_windows_console
just_fix_windows_console()

environ["MPLCONFIGDIR"] = "/tmp"
environ["TERM"] = "xterm"

sys.setrecursionlimit(10**9)
app = Flask(__name__)

print('pyroscope configuration'.upper())
pyroscope.configure(
    app_name="sortdb",
    server_address="http://pyroscope:4040",
    detect_subprocesses=True,
    enable_logging=True,
)

@app.route("/")
@pyroscope.tag_wrapper({"function": "sortdb"})
def sortdb():
    with pyroscope.tag_wrapper({ "function": "sortdb"}):
        print("Handling request in sortdb...")
        with app.app_context():
            sleep(2)
            system('clear')
            Database().menu()
            return jsonify({"message": "Main function executed successfully"})

if __name__ == '__main__':
    print("Serving on port 8000...\nvisit http://127.0.0.1:8000")
    app.run(debug=False, host="0.0.0.0", port=8000)
