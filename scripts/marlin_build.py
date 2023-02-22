import configparser
import glob
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile

# Local Includes
from common import Common


class MarlinBuild:
    marlin_version = "bugfix-2.1.x"
    local_pio_script_path = "tmp/get-platformio.py"
    pio_download_url = "https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py"
    marlin_download_url = f"https://github.com/MarlinFirmware/Marlin/archive/{marlin_version}.zip"
    download_zip_filepath = f"tmp/marlin_{marlin_version}.zip"
    config_paths = [
        "config/Configuration.h",
        "config/Configuration_adv.h",
    ]
    home = os.path.expanduser("~")
    if sys.platform == "win32":
        pio_command = f"{home}/.platformio/penv/Scripts/pio.exe"
    else:
        pio_command = f"{home}/.platformio/penv/bin/pio"

    def __init__(self):
        pass

    def make_folder_structure(self):
        directories_to_make = ["tmp", "build", "output"]
        print("[Info] Creating directories:")
        for curr_dir in directories_to_make:
            os.makedirs(curr_dir, exist_ok=True)
            print(f"\t{curr_dir}")

    def install_platformio(self):
        Common.download_file(self.pio_download_url, self.local_pio_script_path)
        pio_install_success = Common.run_process([sys.executable, self.local_pio_script_path])

        if not pio_install_success:
            return False

        Common.clean_up_files([self.local_pio_script_path])
        return True

    def get_marlin(self):
        Common.download_file(self.marlin_download_url, self.download_zip_filepath)
        Common.clean_up_folder("build")

        print(f"[Info] Extracting {self.download_zip_filepath} to build folder...")
        with zipfile.ZipFile(self.download_zip_filepath, "r") as zip_ref:
            zip_ref.extractall("build")

        Common.clean_up_files([self.download_zip_filepath])

    def build_marlin(self) -> bool:
        marlin_dirs = glob.glob("build/Marlin-*")
        marlin_dir = ""
        if len(marlin_dirs) > 1:
            print("[Error] Too many Marlin folders in the build directory:\n\t{}".format("\n\t".join(marlin_dirs)))
            return False
        elif len(marlin_dirs) == 0:
            print("[Error] Couldn't find Marlin in the build directory")
            return False
        else:
            marlin_dir = marlin_dirs[0]

        config_destination_path = os.path.join(marlin_dir, "Marlin")
        built_binary_path = os.path.join(marlin_dir, ".pio/build/Artillery_Ruby/firmware.bin")

        for config_file in self.config_paths:
            print(f"[Info] Copying {config_file} to {config_destination_path}")
            shutil.copy(config_file, os.path.join(marlin_dir, "Marlin"))

        pio_ino_path = os.path.join(marlin_dir, "platformio.ini")
        print(f"[Info] Making {pio_ino_path} file build for Ruby board")
        config = configparser.ConfigParser()
        config.read(pio_ino_path)
        config.set(r"platformio", r"default_envs", r"Artillery_Ruby")
        with open(pio_ino_path, "w") as configfile:
            config.write(configfile)

        print(f"[Info] Building Marlin found in {marlin_dir}")
        os.chdir(marlin_dir)

        build_success = Common.run_process([self.pio_command, "run"])
        if not build_success:
            return False

        Common.work_top_level()

        print(f"[Info] Moving compiled firmware into output folder")
        shutil.copy(built_binary_path, "output")

        return True


def main():
    mb = MarlinBuild()
    Common.work_top_level()
    mb.make_folder_structure()

    if not Common.check_command_exists(mb.pio_command):
        mb.install_platformio()

    mb.get_marlin()

    if not mb.build_marlin():
        print("[Error] Marlin build failed")
        return


if __name__ == "__main__":
    main()
