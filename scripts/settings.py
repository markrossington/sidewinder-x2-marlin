### PlatformIO Settings
pio_download_url = "https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py"

### Building Marlin
marlin_version = "80f0d4ed7c7e6487ffcc9a2f4b8ea32f78192446"  # latest commit tested on bugfix-2.1.x
marlin_download_url = f"https://github.com/MarlinFirmware/Marlin/archive/{marlin_version}.zip"


# Set to True if you want to use Configuration files from somewhere else, 
# you will need to specify marlin_configuration_h and marlin_configuration_adv_h below
# Set to False to use the default configuration found in the config/ folder
use_custom_config = False

# URL of Configuration.h file, only used if use_custom_config is True. This is the Marlin projects example.
marlin_configuration_h = "https://github.com/MarlinFirmware/Configurations/raw/bugfix-2.1.x/config/examples/Artillery/Sidewinder%20X2/Configuration.h"

# URL of Configuration_adv.h file, only used it use_custom_config is True. This is the Marlin projects example.
marlin_configuration_adv_h = "https://github.com/MarlinFirmware/Configurations/raw/bugfix-2.1.x/config/examples/Artillery/Sidewinder%20X2/Configuration_adv.h"


### Flashing

dfu_util_path = ""  # Leave blank to use platformio's version
printer_backup_folder = "eeprom_settings"

# Can override the platformio command if required here
pio_path_override = ""  # leave blank to override
