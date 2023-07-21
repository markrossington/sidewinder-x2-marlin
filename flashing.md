# Flashing firmware onto your printer

There are multiple reasons you may want to do this manually: it could be to learn or because the automatic method doesn't work for you.

Here is artillery's guide: <https://bit.ly/3BLAcBn> and here's Freakydude's guide: <https://blog.freakydu.de/posts/2022-09-30-flash_marlin_sidewinderx2/> The following is mine.

# Put into reprogram mode
The first step is to put your printer into a mode where it can be downloaded to. This is also called DFU (Device Firmware Update) mode.

## DFU mode from Marlin
If your printer runs Marlin you can put the printer into reprogram mode by sending [`M997`](https://marlinfw.org/docs/gcode/M997.html) to the printer over the serial interface.

 1. Install a serial terminal app such as [Coolterm](https://freeware.the-meiers.org)
 2. Open the terminal tool
 3. Connect [USB-B to USB-A cable](https://www.amazon.com/AmazonBasics-USB-2-0-Cable-Male/dp/B00NH11KIK/) between your PC and your computer and turn the printer on
 4. A new serial port should appear to connect to in your serial terminal. e.g. `COM5`
 5. Connect to this with a baud rate of `115200`
 6. Type `M997` and press send
 7. If you see the serial port disconnect and the printer lights go off then it has rebooted in reprogram mode.

If this fails then see the next section.

## DFU Mode from Klipper or if M997 fails

It's been reported that to get into DFU mode if you have Klipper installed then you need to use the jumper method.

I will repeat what's written here: <https://3dprintbeginner.com/how-to-install-klipper-on-sidewinder-x2/>

>To do this, you need to remove the bottom cover of the printer in order to gain physical access to the Artillery Ruby board. Then, you need to install a jumper to connect the BOOT and the +3.3V pin. This connection will put the Ruby board in DFU mode and will allow you to flash the printer.

![jumper](https://3dprintbeginner.com/wp-content/uploads/2022/01/Artillery-Ruby-DFU-mode-jumper-scaled.jpg)

> When the flashing process is complete, the jumper can be removed.

# Reprogramming

 1. Get the `firmware.bin` you want to download to your printer
 2. Ensure `dfu-util` installed:
    * Windows: Download latest from [here](https://dfu-util.sourceforge.net/releases/dfu-util-0.9-win64.zip) 
    * Linux: In a terminal type: `sudo apt install dfu-util`
    * Mac: In a terminal type: `brew install dfu-util`
 3. Open a command prompt in the directory of your `firmware.bin`
 4. Run the following command:
    * Windows: `dfu-util -a 0 -s 0x8000000:leave -D firmware.bin`
    * Linux/Mac: `sudo dfu-util -a 0 -s 0x8000000:leave -D firmware.bin`
 5. Restart your printer
