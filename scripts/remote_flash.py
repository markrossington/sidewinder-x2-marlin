# Standard Includes
import os
import subprocess

# Local Includes
import settings
from common import Common


def main():
    Common.work_top_level()

    print("[Info] Delete existing temporary folder for scripts and binary on remote host")
    Common.run_process(["ssh", settings.remote_address, f'if [ -d "{settings.remote_folder}" ]; then rm -r {settings.remote_folder}; fi'])

    print("[Info] Making temporary folder for scripts and binary on remote host")
    Common.run_process(["ssh", settings.remote_address, f"mkdir {settings.remote_folder}"])

    if os.path.isfile("output/firmware.bin"):
        print("[Info] Found firmware.bin, copying to remote host")
        Common.run_process(["scp", "-r", "output", f"{settings.remote_address}:{settings.remote_folder}/"])
    else:
        print("[Error] output/firmware.bin not found, check if it built correctly")
        return

    if os.path.isdir("scripts"):
        print("[Info] Found scripts directory, copying to remote host")
        Common.run_process(["scp", "-r", "scripts", f"{settings.remote_address}:{settings.remote_folder}/"])
    else:
        print("[Error] scripts directory not found")
        return

if __name__ == "__main__":
    main()
