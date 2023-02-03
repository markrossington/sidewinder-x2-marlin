# Marlin for Artillery Sidewinder X2

The stock firmware on the Artillery Sidewinder X2 is [Marlin](https://github.com/MarlinFirmware/Marlin), however [Artillery's version](https://github.com/artillery3d/sidewinder-x2-firmware) is out of date (2.0.9.1) and missing some fairly basic features.

Marlin is an open source project in active development and so with a little configuration this can be made to run on any supported printer. 

In this repository you will find 2 files: [`Configuration.h`](configs/updated/Configuration.h) and [`Configuration_adv.h`](configs/updated/Configuration_adv.h) which are exactly that.

Scripts to download the latest supported Marlin, apply the configuration and build the firmware to flash onto your printer are a WIP.

# Lets just do this

 1. Ensure you have python
 2. If you don't have PlatformIO installed, then run: `01-install-platformio.py`
 3. Run: `02-get-marlin.py` and select which version you want
 4. Run: `03-build-marlin.py` and compiled firmware should be in `output/firmware.bin`
 5. Ensure `dfu-util` installed, turn printer on and plug a USB cable into it. Run `04-flash-marlin.py`.

# Summary of Differences from Stock

| Feature/Difference           | Stock              | This                      | Reference Variable                               | Rationale/Notes                                                                                          |
|------------------------------|--------------------|---------------------------|--------------------------------------------------|----------------------------------------------------------------------------------------------------------|
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
| Advanced OK Command          | Off                | On                        | ADVANCED_OK                                      | Allow Marlin to respond with additional info when returning OK                                            |
| M600 Filament change feature | Off                | On                        | NOZZLE_PARK_FEATURE, ADVANCED_PAUSE_FEATURE      |                                                                                                          |
| Auto report position         | Off                | On                        | AUTO_REPORT_POSITION, M114_DETAIL, M114_REALTIME | some clients may use this                                                                                |
| Lower Case G-Code            | Off                | On                        | GCODE_CASE_INSENSITIVE                           | Why not                                                                                                  |
| Host Action Commands         | Off                | On                        | HOST_ACTION_COMMANDS                             | Allow more advanced features of octoprint at negligible cost to performance                              |
| Cancel Objects               | Off                | On                        | CANCEL_OBJECTS                                   | Useful mid print to continue with other projects if one may have lifted or otherwise failed              |

# Notable omitted features

 - **Any UI or Display options** - The Sidewinder X2 has a display with it's own controller which communicates via UART to the Ruby Mainboard. So Marlin doesn't drive this.
 - **Any USB or SD card option** - The display controller also handles the SD card and USB slots so no need to configure here.

# Folder Structure

* configs
  * updated - The configuration to use on a new Sidewinder X2
  * stock_artillery - For reference only, to see which options are enabled on the stock firmware
* scripts
  * `01-install-platformio.py`
  * `02-get-marlin.py`
  * `03-build-marlin.py`
  * `04-flash-marlin.py`

# TODO:

 - [ ] Add a nice way to input which marlin to download and which config to apply (ini file, command line args, command line UI)
 - [ ] Combine scripts
 - [ ] Neaten up and document scripts
 - [ ] Add a way to point at a repo of custom config

# Sources/Links

 - The amazing Marlin project: https://github.com/MarlinFirmware/Marlin
 - Stock Binaries, if you wish to go back: https://www.artillery3d.com/pages/downloads
 - Stock source code: https://github.com/artillery3d/sidewinder-x2-firmware
 - Freakydude's Build: https://github.com/freakydude/Marlin
