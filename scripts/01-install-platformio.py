import urllib.request
import sys
import subprocess
import os

local_pio_script_path = "tmp/get-platformio.py"
pio_download_url = "https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py"

os.makedirs("tmp")

print(f"Downloading get_platformio.py from {pio_download_url} to {local_pio_script_path}...")
urllib.request.urlretrieve(pio_download_url, local_pio_script_path)

subprocess.run([sys.executable, local_pio_script_path])

print(f"Cleaning up {local_pio_script_path}")
os.remove(local_pio_script_path)
