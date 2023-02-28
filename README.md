# Marlin for Artillery Sidewinder X2
[![Artillery3d Repo](https://img.shields.io/badge/Artillery%20Version-v2.0.9.1-blue)](https://github.com/artillery3d/sidewinder-x2-firmware)
[![Marlin Repo](https://img.shields.io/github/v/release/MarlinFirmware/Marlin?label=%20Marlin%20Version)](https://github.com/MarlinFirmware/Marlin)
[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/pp8mnskrg2f)



The stock firmware on the Artillery Sidewinder X2 is [Marlin](https://github.com/MarlinFirmware/Marlin), however [Artillery's version](https://github.com/artillery3d/sidewinder-x2-firmware) is out of date and missing some useful features.

Marlin is an open source project in active development and so with a little configuration the latest version can be made to run on any supported printer. 

In this repository you will find configuration for use with newer versions of Marlin on the Sidewinder X2 which consists of 2 files:
 - [`config/Configuration.h`](config/Configuration.h)
 - [`config/Configuration_adv.h`](config/Configuration_adv.h)

To save you having to manually figure out how to use these files I have written scripts to download the latest supported Marlin, apply the configuration and build the firmware to flash onto your printer.

Feel free to [open an issue](https://github.com/markrossington/sidewinder-x2-marlin/issues/new) if you think there are more sane defaults or find any bugs.

# Disclaimer
I offer no warranty, support or guarantees. Any changes to your 3D printer firmware and the consequences of these changes are your responsibility. If you do not understand what you are doing then I suggest you do not continue.

# Lets just do this

## Build the Firmware

 1. Clone or [download a zip](https://github.com/markrossington/sidewinder-x2-marlin/archive/refs/heads/main.zip) of this repository
 2. Unzip to a folder, for example: 
    * Windows: `C:/sidewinder-x2-marlin/` 
    * Linux/Mac: `~/sidewinder-x2-marlin/`
 3. Ensure you have Python 3.x installed. [Download here](https://www.python.org/downloads/).
 4. Open a command prompt on Windows or terminal on Linux/Mac
 5. Type (Note this is the same folder as in step 2): 
    * Windows: `cd C:/sidewinder-x2-marlin/` 
    * Linux/Mac: `cd ~/sidewinder-x2-marlin/` 
 6. Type:
    * Windows `python scripts/marlin_build.py`
    * Linux/Mac: `python3 scripts/marlin_build.py`
 7. There will be a lot of text flying past which is a good thing, once it's stopped firmware should be built and available in the `output` folder. Check for `firmware.bin`

## Program new firmware onto printer (aka flashing)
> **Warning**
> `scripts/marlin_flash.py` is a work in progress, please don't use yet. Follow the manual guide here: [flashing.md](flashing.md)

<details><summary>Expand to see how the script should work</summary>

 1. Ensure firmware has been built as in section above
 2. Ensure `dfu-util` installed:
    * Windows: Download latest from [here](https://dfu-util.sourceforge.net/releases/dfu-util-0.9-win64.zip) and unzip to the same folder you unzipped the files of the repository before in step 2, for example:`C:/sidewinder-x2-marlin/`
    * Linux: In a terminal type: `sudo apt install dfu-util`
    * Mac: In a terminal type: `brew install dfu-util`
 3. Turn printer on and plug a USB-B cable between the printer and your computer
 4. Open a command prompt on Windows or terminal on Linux/Mac
 5. Type:
    * Windows `python scripts/marlin_flash.py`
    * Linux/Mac: `python3 scripts/marlin_flash.py`
</details>

# New Features vs Stock
 * [Linear Advance](https://marlinfw.org/docs/features/lin_advance.html)
 * [Input Shaping](https://marlinfw.org/docs/gcode/M593.html)
 * Better support for [Octoprint](https://octoprint.org) by enabling [`HOST_ACTION_COMMANDS`](https://reprap.org/wiki/G-code#Action_commands)
 * [Cancel Objects](https://marlinfw.org/docs/gcode/M486.html)
 * Other minor improvements..

<details><summary><strong>Click to show full detailed comparison</strong></summary>

| Feature/Difference           | Stock              | This                      | Reference Variable                               | Rationale/Notes                                                                                          |
| ---------------------------- | ------------------ | ------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Marlin Version               | 2.0.9.1            | 2.1.2 Bugfix              | N/A                                              | Less bugs, newer features, see [Marlin Releases](https://github.com/MarlinFirmware/Marlin/releases) page |
| Heater Minimum Temperature   | 5 C                | -5 C                      | HEATER_0_MINTEMP etc                             | 5 C is a bad default because it is a reasonable ambient temperature in a garage                          |
| Restore level after home     | Off                | On                        | ENABLE_LEVELING_AFTER_G28                        | Save having to enter `M420` to restore the mesh after home in slicer settings                            |
| Possible to detach servo     | Off                | On                        | SERVO_DETACH_GCODE                               | Add ability to send `M282` for lower power idle state                                                    |
| Kickstarting fans            | Off                | 100ms                     | FAN_KICKSTART_TIME                               | Allows the fan to spin up reliably                                                                       |
| Auto Aligning Steppers       | Off                | On                        | Z_STEPPER_AUTO_ALIGN                             | There are 2 Z axis steppers TBD check if this is needed                                                  |
| Input Shaping                | Off                | On                        | INPUT_SHAPING_X, INPUT_SHAPING_Y                 | Allows reduction in ringing and ghosting artifacts on prints induced by vibrations of the printer        |
| Adaptive Step Smoothing      | Off                | On                        | ADAPTIVE_STEP_SMOOTHING                          | Increases resolution of stepping for better print quality                                                |
| Linear Advance               | Off                | On                        | LIN_ADVANCE                                      | Maintains consistent pressure in the nozzle for cleaner corners/ other features which change speed       |
| Increased Arc support        | Low Res No Circles | Higher Res, allow circles | MIN_ARC_SEGMENT_MM, ARC_P_CIRCLES                |                                                                                                          |
| Internal Move Buffer         | 16                 | 64                        | BLOCK_BUFFER_SIZE                                | Increase buffer size providing there is SRAM available is a good thing                                   |
| Serial ASCII Buffer          | 4 bytes            | 32 bytes                  | BUFSIZE                                          |                                                                                                          |
| Serial Receive Buffer        | 128 bytes          | 2048 bytes                | RX_BUFFER_SIZE                                   | This makes printing with something like octoprint much smoother and less likely to stutter               |
| Advanced OK Command          | Off                | On                        | ADVANCED_OK                                      | Allow Marlin to respond with additional info when returning OK                                           |
| M600 Filament change feature | Off                | On                        | NOZZLE_PARK_FEATURE, ADVANCED_PAUSE_FEATURE      |                                                                                                          |
| Auto report position         | Off                | On                        | AUTO_REPORT_POSITION, M114_DETAIL, M114_REALTIME | some clients may use this                                                                                |
| Lower Case G-Code            | Off                | On                        | GCODE_CASE_INSENSITIVE                           | Why not                                                                                                  |
| Host Action Commands         | Off                | On                        | HOST_ACTION_COMMANDS                             | Allow more advanced features of octoprint at negligible cost to performance                              |
| Cancel Objects               | Off                | On                        | CANCEL_OBJECTS                                   | Useful mid print to continue with other projects if one may have lifted or otherwise failed              |
</details>


# Folder Structure

* `configs` - Updated Marlin configuration for Sidewinder X2
* `scripts`
  * `settings.py` - Edit this file to change settings such as which version of marlin you want, which config to use etc.
  * `marlin_build.py` - Build Marlin
  * `marlin_flash.py` - Flash Marlin to printer
  * `common.py` - Common functions used by both scripts. Save me writing them twice. You shouldn't need to edit or use this file.

# FAQ

  1. If you're going to flash a new firmware, why not just use [Klipper](https://www.klipper3d.org)?
     * Klipper will mean learning a whole new software ecosystem. This is a valuable learning project and **one I suggest to those who seek it**. However if you just want your printer to operate in the same way, but with better features: Marlin is the way to go. 
     * Feature wise Klipper used to be king, however the Marlin team are catching up with features such as linear advance and input shaping which are now both available. 
     * You absolutely need an additional computer (usually a Rapsberry Pi) constantly plugged into your printer. Not a problem for most of us who use Octoprint/OctoPi but still worth noting. Using Klipper your printer will not operate without this. 
     * The existing TFT screen will no longer work, there are great projects such as [Klipperscreen](https://klipperscreen.readthedocs.io) which will work with a screen plugged into your Raspberry Pi but this is extra hardware still. 
  2. How does this compare to the official Marlin Sidewinder X2 example configurations found [here](https://github.com/MarlinFirmware/Configurations/tree/import-2.1.x/config/examples/Artillery/Sidewinder%20X2)?
     * The Marlin example configurations were the starting point for the ones in this project. Using the example configs will give you a fairly stock experience on your printer. To enable newer features you would then need to turn certain settings on (e.g. Linear Advance) one by one. That is what this project does for you. Not only that, we offer build and flash scripts too.
  3. Is this the firmware for the TFT?
     * No, this is the firmware for the mainboard. If you wish to update the firmware for the TFT then look at [Arillery's Download Page](https://www.artillery3d.com/pages/downloads) or for something new try [BigTreeTech's firmware](https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware), though if you have a new style TFT then you might not be able to, see [the following issue](https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware/issues/2391).
  4. Why are the scripts in Python and not X, Y or Z?
      * I wanted this to work on as many platforms as possible. Python allows for this and is often installed on many peoples machines anyway. It's worth noting that building Marlin doesn't work on a Raspberry Pi at this point in time, this is a limitation of the toolchains and nothing I can control.
  5. Why are no UI or SD card options configured?
      * The circuit board connected to the TFT display manages the UI and SD card on this printer. Marlin runs on a different board, the mainboard. For TFT related firmware see question 2.
  6. Why don't you have this new amazing feature installed?
      * I might not know about it, [open an issue](https://github.com/markrossington/sidewinder-x2-marlin/issues/new).

# Sources/Links

 - The amazing Marlin project: https://github.com/MarlinFirmware/Marlin
 - Official Marlin config for Sidewinder X2: https://github.com/MarlinFirmware/Configurations/tree/import-2.1.x/config/examples/Artillery/Sidewinder%20X2
 - Stock Binaries, if you wish to go back: https://www.artillery3d.com/pages/downloads
 - Stock source code: https://github.com/artillery3d/sidewinder-x2-firmware
 - Freakydude's Build: https://github.com/freakydude/Marlin
