import configparser
import glob
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
from distutils.spawn import find_executable


class MarlinBuilder:
    repository_root = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    marlin_version = "bugfix-2.1.x"
    local_pio_script_path = "tmp/get-platformio.py"
    pio_download_url = "https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py"
    marlin_download_url = f"https://github.com/MarlinFirmware/Marlin/archive/{marlin_version}.zip"
    download_zip_filepath = f"tmp/marlin_{marlin_version}.zip"
    config_paths = [
        "config/Configuration.h",
        "config/Configuration_adv.h",
    ]
    dont_run_processes = False  # TODO: This is only useful for dev, remove
    home = os.path.expanduser("~")
    pio_command = f"{home}/.platformio/penv/Scripts/pio"

    def __init__(self, dont_run_processes):
        self.dont_run_processes = dont_run_processes

    def work_top_level(self):
        print(f"[Info] Setting working directory to {self.repository_root}")
        os.chdir(self.repository_root)

    def clean_up_files(self, files_to_remove):
        print("[Info] Cleaning up:")
        for file_path in files_to_remove:
            print(f"\t{file_path}")
            os.remove(file_path)

    def clean_up_build_directory(self):
        print("[Info] Cleaning up build directory")
        shutil.rmtree("build")
        os.makedirs("build", exist_ok=True)

    def make_folder_structure(self):
        directories_to_make = ["tmp", "build", "output"]
        print("[Info] Creating directories:")
        for curr_dir in directories_to_make:
            os.makedirs(curr_dir, exist_ok=True)
            print(f"\t{curr_dir}")

    def download_file(self, remote_url, local_path):
        print(f"[Info] Downloading {remote_url} to {local_path}...")
        urllib.request.urlretrieve(remote_url, local_path)

    def run_process(self, process_command):
        print("[Info] Running {}".format(" ".join(process_command)))

        if not self.dont_run_processes:
            with subprocess.Popen(process_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
                for line in process.stdout:
                    line = line.decode("utf8").strip()
                    if line != "":
                        print(line)

    def install_platformio(self):
        self.download_file(self.pio_download_url, self.local_pio_script_path)
        self.run_process([sys.executable, self.local_pio_script_path])
        self.clean_up_files([self.local_pio_script_path])

    def check_command_exists(self, command):
        print(f"[Info] Checking for {command}")
        command_full_path = find_executable(command)

        if command_full_path is None:
            return False

        print(f"[Info] Found {command_full_path}")

        return True

    def get_marlin(self):
        self.download_file(self.marlin_download_url, self.download_zip_filepath)
        self.clean_up_build_directory()

        print(f"[Info] Extracting {self.download_zip_filepath} to build folder...")
        with zipfile.ZipFile(self.download_zip_filepath, "r") as zip_ref:
            zip_ref.extractall("build")

        self.clean_up_files([self.download_zip_filepath])

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
        self.run_process([self.pio_command, "run"])
        os.chdir(self.repository_root)

        print(f"[Info] Moving compiled firmware into output folder")
        shutil.copy(built_binary_path, "output")

        return True


def main():
    mb = MarlinBuilder(dont_run_processes=False)
    mb.work_top_level()
    mb.make_folder_structure()

    if not mb.check_command_exists(mb.pio_command):
        mb.install_platformio()

    mb.get_marlin()

    if not mb.build_marlin():
        print("[Error] Marlin build failed")
        return


if __name__ == "__main__":
    main()
