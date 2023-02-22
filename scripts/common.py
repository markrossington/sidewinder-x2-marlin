# Standard Includes
import os
import shutil
import subprocess
import sys
import urllib.request
from distutils.spawn import find_executable
from os.path import expanduser
from sys import platform
from typing import List

# Local Includes
import settings


class Common:
    local_pio_script_path = "tmp/get-platformio.py"
    home = expanduser("~")
    if platform == "win32":
        pio_command = f"{home}/.platformio/penv/Scripts/pio.exe"
    else:
        pio_command = f"{home}/.platformio/penv/bin/pio"

    @staticmethod
    def work_top_level() -> None:
        repository_root: str = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
        print(f"[Info] Setting working directory to {repository_root}")
        os.chdir(repository_root)

    @staticmethod
    def clean_up_files(files_to_remove: List[str]) -> None:
        print("[Info] Cleaning up:")
        for file_path in files_to_remove:
            print(f"\t{file_path}")
            os.remove(file_path)

    @staticmethod
    def clean_up_folder(folder_to_remove: str) -> None:
        print(f"[Info] Cleaning up {folder_to_remove} directory")
        shutil.rmtree(folder_to_remove)
        os.makedirs(folder_to_remove, exist_ok=True)

    @staticmethod
    def run_process(process_command: str) -> bool:
        print("[Info] Running {}".format(" ".join(process_command)))

        with subprocess.Popen(process_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            for line in process.stdout:
                line = line.decode("utf8").strip()
                if line != "":
                    print(line)
            process.communicate()
            if process.returncode != 0:
                print(f'[Error] Process "{process_command}" failed, return code was {process.returncode}')
                return False
            else:
                return True

    @staticmethod
    def check_command_exists(command: str) -> bool:
        print(f"[Info] Checking for {command}")
        command_full_path = find_executable(command)

        if command_full_path is None:
            return False

        print(f"[Info] Found {command_full_path}")

        return True

    @staticmethod
    def download_file(remote_url: str, local_path: str) -> bool:
        print(f"[Info] Downloading {remote_url} to {local_path}...")
        urllib.request.urlretrieve(remote_url, local_path)

        file_downloaded = os.path.isfile(local_path)

        return file_downloaded

    @staticmethod
    def install_platformio() -> bool:
        Common.download_file(settings.pio_download_url, settings.local_pio_script_path)
        pio_install_success = Common.run_process([sys.executable, settings.local_pio_script_path])

        if not pio_install_success:
            return False

        Common.clean_up_files([settings.local_pio_script_path])
        return True
