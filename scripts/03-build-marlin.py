import sys
import subprocess
import os 
from os.path import expanduser
import glob
import shutil
import configparser

configuration_paths = [
    "configuration/updated/Configuration.h",
    "configuration/updated/Configuration_adv.h"
]
home = expanduser("~")
pio_command = f"{home}/.platformio/penv/bin/pio"
marlin_dirs = glob.glob("build/Marlin-*")

if len(marlin_dirs) > 1:
    print("Too many Marlin folders in the build directory:\n\t{}".format("\n\t".join(marlin_dirs)))
    sys.exit()
elif len(marlin_dirs) == 0:
    print("Couldn't find Marlin in the build directory.")
    sys.exit()
else:
    marlin_dir = marlin_dirs[0]

print("Applying updated configuration to Marlin")
config_destination_path = os.path.join(marlin_dir, "Marlin")
for config_file in configuration_paths:
    print(f"Copying {config_file} to {config_destination_path}")
    shutil.copy(config_file, os.path.join(marlin_dir, "Marlin"))

pio_ino_path = os.path.join(marlin_dir, "platformio.ini")
print(f"Making {pio_ino_path} file build for Ruby board")
config= configparser.SafeConfigParser()
config.read(pio_ino_path)
config.set(r"platformio",r"default_envs",r"Artillery_Ruby")

with open(pio_ino_path, 'w') as configfile:
    config.write(configfile)

print(f"Building Marlin found in {marlin_dir}")
os.chdir(marlin_dir)
with subprocess.Popen([pio_command, "run"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
    for line in process.stdout:
        line = line.decode('utf8').strip()
        if(line != ""):
            print(line)

