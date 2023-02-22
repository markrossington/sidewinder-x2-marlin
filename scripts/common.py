import os
import shutil
import subprocess
import sys
import urllib
from distutils.spawn import find_executable
from typing import List


class Common:
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
    def download_file(remote_url, local_path):
        print(f"[Info] Downloading {remote_url} to {local_path}...")
        urllib.request.urlretrieve(remote_url, local_path)
