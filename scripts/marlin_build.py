# Standard Includes
import configparser
import glob
import os
import shutil
import sys
import zipfile

# Local Includes
import settings
from common import Common


class MarlinBuild:
    default_config_paths = ["config/Configuration.h", "config/Configuration_adv.h"]
    config_paths = ["", ""]

    def __init__(self):

        Common.clean_up_folder("tmp/custom_config")

        if settings.use_custom_config == False or settings.marlin_configuration_h == "" or settings.marlin_configuration_adv_h == "":
            self.config_paths = self.default_config_paths
        else:
            os.makedirs("tmp/custom_config", exist_ok=True)
            self.config_paths = ["tmp/custom_config/Configuration.h", "tmp/custom_config/Configuration_adv.h"]

            Common.download_file(settings.marlin_configuration_h , self.config_paths[0])
            Common.download_file(settings.marlin_configuration_adv_h, self.config_paths[1])

            for file_check in self.config_paths:
                if not os.path.isfile(file_check):
                    print(f"[Error] Cannot find {file_check}")
                    sys.exit()

    def make_folder_structure(self):
        directories_to_make = ["tmp", "build", "output"]
        print("[Info] Creating directories:")
        for curr_dir in directories_to_make:
            os.makedirs(curr_dir, exist_ok=True)
            print(f"\t{curr_dir}")

    def get_marlin(self):
        download_zip_filepath: str = f"tmp/marlin_{settings.marlin_version}.zip"
        Common.download_file(settings.marlin_download_url, download_zip_filepath)
        Common.clean_up_folder("build")

        print(f"[Info] Extracting {download_zip_filepath} to build folder...")
        with zipfile.ZipFile(download_zip_filepath, "r") as zip_ref:
            zip_ref.extractall("build")

        Common.clean_up_files([download_zip_filepath])

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

        build_success = Common.run_process([Common.pio_command, "run"])
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

    if not Common.check_command_exists(Common.pio_command):
        Common.install_platformio()

    mb.get_marlin()

    if not mb.build_marlin():
        print("[Error] Marlin build failed")
        return


if __name__ == "__main__":
    main()
