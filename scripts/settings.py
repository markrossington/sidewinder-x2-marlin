# ==== PlatformIO Settings ====
pio_download_url = "https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py"

# ==== Building Marlin ====
marlin_version = "80f0d4ed7c7e6487ffcc9a2f4b8ea32f78192446"  # latest commit tested on bugfix-2.1.x
marlin_download_url = f"https://github.com/MarlinFirmware/Marlin/archive/{marlin_version}.zip"

# This is the PlatformIO target (i.e. which board to build for)
# Artillery_Ruby is the name of the Artillery 3D 32bit printer mainboard
# This is good for: Artillery X1, X2, Genius, Genius Pro and Hornet printers
platformio_target = "Artillery_Ruby"

# Set to True if you want to use Configuration files from somewhere else, 
# you will need to specify marlin_configuration_h and marlin_configuration_adv_h below
# Set to False to use the default configuration found in the config/ folder
use_custom_config = False

# URL of Configuration.h file, only used if use_custom_config is True. This is the Marlin projects example.
marlin_configuration_h = "https://github.com/MarlinFirmware/Configurations/raw/bugfix-2.1.x/config/examples/Artillery/Sidewinder%20X2/Configuration.h"

# URL of Configuration_adv.h file, only used it use_custom_config is True. This is the Marlin projects example.
marlin_configuration_adv_h = "https://github.com/MarlinFirmware/Configurations/raw/bugfix-2.1.x/config/examples/Artillery/Sidewinder%20X2/Configuration_adv.h"

# If the configurations live in a private github repo, add your PAT here
personal_access_token = "" # Leave blank for public repos

# ==== Flashing ====

dfu_util_path = ""  # Leave blank to use platformio's version
printer_backup_folder = "eeprom_settings"

# Can override the platformio command if required here
pio_path_override = ""  # leave blank to override

# ==== Remote Flashing ====
# Only need to use these settings for remote_flash.py

# The SSH username and IP address of remote host connected to 3d printer
remote_address = "pi@192.168.0.1" 

# Temp folder on remote host to put the scripts and firmware binary
remote_folder = "/home/pi/marlin_flashing"

