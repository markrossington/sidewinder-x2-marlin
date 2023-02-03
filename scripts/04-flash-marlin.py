import os
import subprocess
import sys
import time
from distutils.spawn import find_executable
from sys import platform

import serial
import serial.tools.list_ports

binary_to_flash = "output/firmware.bin"
repository_root = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

os.chdir(repository_root)


# Check dfu-util
print(f"INFO: Checking for dfu-util")
dfu_exist = find_executable("dfu-util")

if dfu_exist is None:
    print(
        "ERROR: Need to install dfu-util. Use brew on mac, apt on linux or grab the exe on Windows"
    )
    sys.exit()

print(f'INFO: dfu-util found at "{dfu_exist}"')

print(f"Putting printer into dfu mode by sending M997 command")
comlist = serial.tools.list_ports.comports()
connected = []
for index, element in enumerate(comlist):
    connected.append("{}. {}".format(index, element.device))

print("Connected COM ports:\n\t{}".format("\n\t".join(connected)))

selected_port_index = int(input("Select which port [0-{}]: ".format(len(comlist) - 1)))
selected_port = comlist[selected_port_index].device
print(f"Selected {selected_port}")

ser = serial.Serial(selected_port, "115200")

ser.write(b"M997\n")

ser.close()


print(f"Waiting for reboot into dfu mode")
time.sleep(5)

print(f"Flashing {binary_to_flash}")
with subprocess.Popen(
    [
        "dfu-util",
        "-a",
        "0",
        "-s",
        "0x8000000:leave",
        "-D",
        binary_to_flash,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
) as process:
    for line in process.stdout:
        line = line.decode("utf8").strip()
        if line != "":
            print(line)


if platform == "linux" or platform == "linux2":
    # maybe apt get
    pass
elif platform == "darwin":
    # brew install
    pass
elif platform == "win32":
    # use exe
    pass
