import os
import subprocess
import sys
import time
from datetime import datetime
from distutils.spawn import find_executable

import serial
import serial.tools.list_ports


class MarlinFlash:
    repository_root = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    binary_to_flash = "output/firmware.bin"
    home = os.path.expanduser("~")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    printer_settings_filename = f"{timestr}-printer-settings.gcode"
    port_name = ""
    serial_port = serial.Serial(baudrate=115200, timeout=1)

    def __init__(self, port_name=None):
        self.port_name = port_name

    def work_top_level(self):
        print(f"[Info] Setting working directory to {self.repository_root}")
        os.chdir(self.repository_root)

    def clean_up_files(self, files_to_remove):
        print("[Info] Cleaning up:")
        for file_path in files_to_remove:
            print(f"\t{file_path}")
            os.remove(file_path)

    def run_process(self, process_command):
        # TODO: have a return which can be checked by caller
        print("[Info] Running {}".format(" ".join(process_command)))

        with subprocess.Popen(process_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            for line in process.stdout:
                line = line.decode("utf8").strip()
                if line != "":
                    print(line)

    def check_command_exists(self, command):
        print(f"[Info] Checking for {command}")
        command_full_path = find_executable(command)

        if command_full_path is None:
            return False

        print(f"[Info] Found {command_full_path}")

        return True

    def inform_how_to_install_dfu_util(self):
        print("[Error] Need to install dfu-util. Use brew on mac, apt on linux or grab the exe on Windows")

    def get_printer_settings(self):
        if not self.serial_port.is_open:
            print("[Error] No serial port open to get printer settings from")
            return False

        self.serial_port.flush()
        print('[Info] Sending: "M503"')
        self.serial_port.write(b"M503\n")

        settings = self.serial_port.readlines()

        if len(settings) == 0:
            print(f"[Error] No response received from printer on port {self.port_name}")
            return False

        with open(self.printer_settings_filename, "w") as setting_file:
            for line in settings:
                line = line.decode("ascii").replace("echo:", "").strip()
                print(f"\t{line}")
                setting_file.write(f"{line}\n")

        print(f"[Info] Written settings to {self.printer_settings_filename}")

        return True

    def restore_printer_settings(self):
        if not self.serial_port.is_open:
            print("[Error] No serial port open to send printer settings to")
            return False

        self.serial_port.flush()

        with open(self.printer_settings_filename, "r") as setting_file:
            for line in setting_file.readlines():
                if not line.startswith(";") and not line.startswith("ok"):
                    print(f'[Info] Sending: "{line.strip()}"')
                    self.serial_port.write(f"{line.strip()}\n".encode("ascii"))
                    received = self.serial_port.readlines()
                    received = b" ".join([line.strip() for line in received])
                    print(received)
                    if not b"ok" in received:
                        print(f"[ERROR] OK not received")
                        return False

        print(f"[Info] Written settings from {self.printer_settings_filename}")

    def flash_new_firmware(self):
        self.serial_port.write(b"M997\n")
        print(f"[Info] Sent M997, waiting for reboot into dfu mode")
        time.sleep(5)
        print(f"Flashing {self.binary_to_flash}")
        self.run_process(
            [
                "sudo",
                "dfu-util",
                "-a",
                "0",
                "-s",
                "0x8000000:leave",
                "-D",
                self.binary_to_flash,
            ]
        )
        return True

    def open_port(self):
        if self.port_name is None:
            print("[Info] No com port provided, listing available ports")
            self.port_name = self.select_port()

            if self.port_name is None:
                print("[Error] No com ports available")
                return False

        self.serial_port.port = self.port_name
        print(f"[Info] Opening {self.port_name}")
        self.serial_port.open()
        return True

    def select_port(self):
        comlist = serial.tools.list_ports.comports()
        connected = []

        if len(comlist) == 0:
            return None

        for index, element in enumerate(comlist):
            connected.append("{}. {}".format(index, element.device))

        print("[Info] Connected COM ports:\n\t{}".format("\n\t".join(connected)))

        selected_port_index = int(input("[Prompt] Select which port [0-{}]: ".format(len(comlist) - 1)))
        selected_port = comlist[selected_port_index].device

        return selected_port

    def close_port(self):
        print(f"[Info] Closing {self.port_name}")
        self.serial_port.close()


def main():
    continue_script = input(
        "\n** WARNING **\n\nThis script is a work in progress with known bugs, it is very likely to leave your printer in an unknown state \n\nContinue? (y/n):"
    )
    if continue_script.lower() != "y":
        return

    mf = MarlinFlash()
    mf.work_top_level()

    if not mb.check_command_exists(mb.pio_command):
        mb.install_platformio()

    if not mf.open_port():
        return

    if not mf.get_printer_settings():
        mf.close_port()
        return

    if not mf.flash_new_firmware():
        mf.close_port()
        return

    if not mf.restore_printer_settings():
        mf.close_port()
        return

    mf.close_port()


if __name__ == "__main__":
    main()
