### PlatformIO Settings
pio_download_url = "https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py"

### Building
marlin_version = "80f0d4ed7c7e6487ffcc9a2f4b8ea32f78192446" # latest commit tested on bugfix-2.1.x
marlin_download_url = f"https://github.com/MarlinFirmware/Marlin/archive/{marlin_version}.zip"

# Can be a URL of github repo with your "Configuration.h" and "Configuration_adv.h" files
marlin_config_to_use = ""  # Leave blank to use default

### Flashing
dfu_util_path = ""  # Leave blank to use platformio's version
printer_backup_folder = "eeprom_settings"

# Can override the platformio command if required here
pio_path_override = ""  # leave blank to override
