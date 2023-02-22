import os
import shutil
import subprocess
import sys
from typing import List


class Common:
    @staticmethod
    def work_top_level():
        repository_root: str = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
        print(f"[Info] Setting working directory to {repository_root}")
        os.chdir(repository_root)

    @staticmethod
    def clean_up_files(files_to_remove: List[str]):
        print("[Info] Cleaning up:")
        for file_path in files_to_remove:
            print(f"\t{file_path}")
            os.remove(file_path)

    @staticmethod
    def clean_up_folder(folder_to_remove: str):
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
