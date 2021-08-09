# MIT License

# Copyright (c) 2021 jonyboi396825

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import subprocess
import threading
import time

import Adafruit_SSD1306
import requests
import serial
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

BUTTON_PIN = 17
BUTTON_SH_PIN = 18
CMD_BIKE_MODE = "python3 raspberrypi/bike_mode.py 2>> errors.txt && printf \"Happened at $(date)\\n\\n\" >> errors.txt;"
CMD_SERVER_MODE = "python3 raspberrypi/server_mode.py 2>> errors.txt && printf \"Happened at $(date)\\n\\n\" >> errors.txt;"

class InitiationError(Exception):
    """
    This error is raised if could not initialize OLED or Arduino.
    """
    def __init__(self, code, *args, **kwargs):
        self.code = code
        self.which = kwargs["which"]
        self.msg = f"{self.which} could not be initialized."

        super().__init__(self.msg)

    def __repr__(self):
        return f"{self.msg} Exiting with code {self.code}."

def handle_bike_mode() -> None:
    global display, img, draw, font, b

    draw.rectangle((0, 0, 128, 128), fill=0)
    draw.text((0, 0), "Restart to switch mode ", fill=255, font=font)
    draw.text((0, 16), "No press detected \nEntering bike mode", fill=255, font=font)
    display.image(img)
    display.display()
    time.sleep(2)

    while True:
        # using subprocess instead of import so an error would not exit out of the whole program and the process would be easier to kill
        subprocess.call(CMD_BIKE_MODE.split())

        # if exits out here, means that OS error happened/Arduino disc or OLED disc
        try:
            # put in try because OLED may be disconnected
            draw.rectangle((0, 0, 128, 128), fill=0)
            draw.text((0, 0), "Oh no!", fill=255, font=font)
            draw.text((0, 16), "OLED or Arduino \ndisconnected. Reconn., \npress B1 try again.", fill=255, font=font)
            display.image(img)
            display.display()
            time.sleep(1)

        except:
            pass

        # let user press button after reconnected and then try again
        b.wait_for_press()
        time.sleep(2) # wait 2 seconds just in case of conflict with writing to OLED

def handle_server_mode() -> None:
    global display, img, draw, font

    # checks for internet connection in order to enter server mode
    try:
        requests.get("https://google.com")

        # display the pi IP as website
        website_name = _get_pi_ip()

        draw.rectangle((0, 0, 128, 128), fill=0)
        draw.text((0, 0), "Restart to switch mode ", fill=255, font=font)
        draw.text((0, 16), f"In server mode \nVisit website: \n{website_name}:7123", fill=255, font=font)
        display.image(img)
        display.display()
        time.sleep(1)

        # using subprocess instead of import so an error would not exit out of the whole program and the process would be easier to kill
        subprocess.call(CMD_SERVER_MODE.split())
    except requests.exceptions.ConnectionError:
        # enter bike mode if no internet connection

        draw.rectangle((0, 0, 128, 128), fill=0)
        draw.text((0, 0), "No connection", fill=255, font=font)
        draw.text((0, 16), "Going into \nbike mode", fill=255, font=font)
        display.image(img)
        display.display()
        time.sleep(1)

        handle_bike_mode()
        return

def shutdown_button() -> None:
    global display, img, draw, font

    # wait 30 seconds so the button wouldn't interfere with any of the setup stuff
    time.sleep(30)

    # shuts down pi when this is pressed

    sh_b = Button(BUTTON_SH_PIN)
    sh_b.wait_for_press()

    # stop all sub programs
    STOP_CMD_BK = "pkill -f raspberrypi/bike_mode.py"
    STOP_CMD_SV = "pkill -f raspberrypi/server_mode.py"
    subprocess.call(STOP_CMD_BK.split())
    subprocess.call(STOP_CMD_SV.split())

    time.sleep(1)

    draw.rectangle((0, 0, 128, 128), fill=0)
    draw.text((0, 0), "Powering off", fill=255, font=font)
    draw.text((0, 16), "Wait for green LED \non RPi to turn off \nbefore switching off.", fill=255, font=font)
    display.image(img)
    display.display()
    time.sleep(1)

    # power off
    POWER_OFF_CMD = "sudo shutdown -h now"
    subprocess.call(POWER_OFF_CMD.split())

def _check_components() -> bool:
    """
    Checks that all components are connected properly before starting the program.
    """

    try:
        # check display
        display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        display.begin()

        # check serial port
        pt_f = open("raspberrypi/port", 'r')
        pt = pt_f.read().strip()
        ser = serial.Serial(pt, 115200)
        ser.flush()
        pt_f.close()

    except OSError as e:
        if (e.errno == 2):
            print("Serial port could not be opened.")
            return "Serial port"
        elif (e.errno == 121):
            print("OLED could not be initialized.")
            return "OLED"
        return "Something"

    return ""

def _get_pi_ip() -> str:
    s_p = subprocess.Popen("hostname -I".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = s_p.communicate()
    return output.decode("utf-8").rstrip()

def main() -> None:
    global display, img, draw, font, b

    print(f"Started program at {datetime.datetime.now()}")

    try:
        try:
            _s = _check_components()
            if (_s != ""):
                raise InitiationError(1, which=_s)
        except InitiationError as e:
            with open("errors.txt", 'a') as f:
                f.write(f"{e}\nHappened at {datetime.datetime.now()} \n\n")

            quit(e.code)

        th1 = threading.Thread(target=shutdown_button)
        th1.start()

        mode = None

        # init display
        display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        display.begin()
        time.sleep(2)

        display.clear()
        display.display()
        time.sleep(1)

        # init python PIL
        img = Image.new('1', (display.width, display.height))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("raspberrypi/fonts/Gidole-Regular.ttf", 12)

        # draw setup text
        draw.text((0, 0), "Setup", font=font, fill=255)
        draw.multiline_text((0, 16), "Press button 1 on RPi \nto enter server mode. \nOtherwise, do nothing.", font=font, fill=255)

        display.image(img)
        display.display()
        time.sleep(1)

        # wait for button press to go into server mode
        b = Button(BUTTON_PIN)

        # wait 5 seconds for user to press button, otherwise enter bike mode
        b.wait_for_press(timeout=5)

        # display if button pressed/button not pressed
        if (b.is_pressed):
            mode = "server"
        else:
            mode = "bike"
    except KeyboardInterrupt:
        display.clear()
        display.display()

        quit()

    try:
        # run respective programs
        if (mode == "bike"):
            handle_bike_mode()
        elif (mode == "server"):
            handle_server_mode()
    except (KeyboardInterrupt):
        # clear display if keyboard interrupt
        display.clear()
        display.display()

    display.clear()
    display.display()

    quit()


if (__name__ == "__main__"):
    main()
