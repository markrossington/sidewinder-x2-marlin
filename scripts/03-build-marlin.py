import configparser
import glob
import os
import shutil
import subprocess
import sys
from os.path import expanduser

repository_root = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

marlin_dirs = glob.glob("build/Marlin-*")
if len(marlin_dirs) > 1:
    print(
        "Too many Marlin folders in the build directory:\n\t{}".format(
            "\n\t".join(marlin_dirs)
        )
    )
    sys.exit()
elif len(marlin_dirs) == 0:
    print("Couldn't find Marlin in the build directory.")
    sys.exit()
else:
    marlin_dir = marlin_dirs[0]
config_paths = [
    "configs/updated/Configuration.h",
    "configs/updated/Configuration_adv.h",
]
home = expanduser("~")
pio_command = f"{home}/.platformio/penv/bin/pio"
config_destination_path = os.path.join(marlin_dir, "Marlin")
output_binary_path = os.path.join(marlin_dir, ".pio/build/Artillery_Ruby/firmware.bin")


os.chdir(repository_root)

print("Applying updated configuration to Marlin")
for config_file in config_paths:
    print(f"Copying {config_file} to {config_destination_path}")
    shutil.copy(config_file, os.path.join(marlin_dir, "Marlin"))

pio_ino_path = os.path.join(marlin_dir, "platformio.ini")
print(f"Making {pio_ino_path} file build for Ruby board")
config = configparser.SafeConfigParser()
config.read(pio_ino_path)
config.set(r"platformio", r"default_envs", r"Artillery_Ruby")

with open(pio_ino_path, "w") as configfile:
    config.write(configfile)

print(f"Building Marlin found in {marlin_dir}")
os.chdir(marlin_dir)
with subprocess.Popen(
    [pio_command, "run"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
) as process:
    for line in process.stdout:
        line = line.decode("utf8").strip()
        if line != "":
            print(line)
os.chdir(repository_root)

print(f"Moving compiled firmware into output folder")
os.makedirs("output", exist_ok=True)
shutil.copy(output_binary_path, "output")
