# Marlin for Artillery Sidewinder X2

The stock firmware on the Artillery Sidewinder X2 is [Marlin](https://github.com/MarlinFirmware/Marlin), however [Artillery's version](https://github.com/artillery3d/sidewinder-x2-firmware) is out of date (2.0.9.1) and missing some fairly basic features.

Marlin is an open source project in active development and so with a little configuration this can be made to run on any supported printer.

In this repository you will find 2 files: [`Configuration.h`](configuration/updated/Configuration.h) and [`Configuration_adv.h`](configuration/updated/Configuration_adv.h) which are exactly that.

You should also find scripts to download the latest supported Marlin, apply the configuration and build the firmware to flash onto your printer.

**NOTE: At the moment this is the configuration for _my_ printer. I have changed a few things from stock and so these defaults may not work for you. E.g. the thermistor type. I hope one day to make a stock configuration**

# Sources/Links

 - Stock Binaries, if you wish to go back: https://www.artillery3d.com/pages/downloads
 - Stock source code: https://github.com/artillery3d/sidewinder-x2-firmware
 - Freakydude's Build: https://github.com/freakydude/Marlin
