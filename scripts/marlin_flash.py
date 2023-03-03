# Standard Includes
import sys
from time import sleep, strftime

# Library includes
import serial
import serial.tools.list_ports

# Local Includes
import settings
from common import Common


class MarlinFlash:
    timestr = strftime("%Y%m%d-%H%M%S")
    printer_settings_filename = f"{settings.printer_backup_folder}/{timestr}-printer-settings.gcode"
    binary_to_flash = "output/firmware.bin"
    install_pio_dfu_command = [Common.pio_command, "pkg", "install", "-g", "--tool", "platformio/tool-dfuutil@^1.11.0"]

    # dfuutil requires sudo on linux and mac
    if not sys.platform == "win32":
        sudo_or_not = "sudo"

    run_pio_dfu_command = [sudo_or_not] + [Common.pio_command, "pkg", "exec", "--package", "platformio/tool-dfuutil", "--", "dfu-util"]
    run_sys_dfu_command = [sudo_or_not] + ["dfu_util"]

    run_dfu_command = run_sys_dfu_command

    port_name = ""
    serial_port = serial.Serial(baudrate=115200, timeout=1)

    def __init__(self, port_name=None):
        self.port_name = port_name

    def install_pio_dfu_util(self):
        print("[Info] Need to install dfu-util")

        dfu_util_install_status = Common.run_process(self.install_pio_dfu_command)

        # Use platformio command for dfu-util
        if dfu_util_install_status:
            self.run_dfu_command = self.run_pio_dfu_command

        return dfu_util_install_status

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

        with open(self.printer_settings_filename, "r") as setting_file:
            for line in setting_file.readlines():
                if (
                    not line.startswith(";")
                    and not line.startswith("ok")
                    and not line.startswith("M149")
                    and not line.startswith("G29")
                    and not line.startswith("M420")
                    and not line.startswith("M206")
                ):
                    print(f'[Info] Sending: "{line.strip()}"')
                    self.serial_port.write(bytes(f"{line.strip()}\n".encode("ascii")))
                    received = self.serial_port.readline()
                    print(received)
                    if not b"ok" in received:
                        print(f"[ERROR] OK not received")
                        return False

        print(f"[Info] Written settings from {self.printer_settings_filename}")

    def flash_new_firmware(self):
        self.serial_port.write(b"M997\n")
        print(f"[Info] Sent M997, waiting for reboot into dfu mode")
        sleep(5)
        print(f"Flashing {self.binary_to_flash}")
        dfu_util_status = Common.run_process(
            self.run_dfu_command
            + [
                "-a",
                "0",
                "-s",
                "0x8000000:leave",
                "-D",
                self.binary_to_flash,
            ]
        )
        return dfu_util_status

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

    Common.work_top_level()

    pio_command = Common.find_pio_command()
    if pio_command == "":
        if Common.install_platformio():
            pio_command = Common.pio_command
        else:
            return

    if not Common.check_command_exists("dfu-util"):
        # Use pio dfu-util if no system version
        if not mf.install_pio_dfu_util():
            return

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
