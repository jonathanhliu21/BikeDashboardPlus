import time
import subprocess

import Adafruit_SSD1306
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

BUTTON_PIN = 17
CMD_BIKE_MODE = "python3 raspberrypi/bike_mode.py"
CMD_SERVER_MODE = "python3 raspberrypi/server_mode.py"

def handle_bike_mode() -> None: 
    global display, img, draw, font

    while True:
        subprocess.call(CMD_BIKE_MODE.split())
        
        # if exits out here, means that OS error happened/Arduino disc or OLED disc

        display.clear()
        display.display()

        draw.text((0, 0), "Oh no!", fill=255, font=font)
        draw.text((0, 16), "OLED or Arduino \ndisconnected. Check \nconnections, try again.", fill=255, font=font)


def main() -> None:
    global display, img, draw, font

    mode = None

    # init display
    display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
    display.begin()

    display.clear()
    display.display()

    # init python PIL
    img = Image.new('1', (display.width, display.height))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("raspberrypi/fonts/arial.ttf", 12)

    # draw setup text
    draw.text((0, 0), "Setup", font=font, fill=255)
    draw.multiline_text((0, 16), "Press button on RPi \nto enter server mode. \nOtherwise, do nothing.", font=font, fill=255)

    display.image(img)
    display.display()

    # wait for button press to go into server mode
    b = Button(BUTTON_PIN)

    try:
        b.wait_for_press(timeout=5)
    except KeyboardInterrupt:
        display.clear()
        display.display()
        quit()

    # display if button pressed/button not pressed
    if (b.is_pressed):
        draw.rectangle((0, 0, 128, 128), fill=0)
        draw.text((0, 0), "Restart to switch mode ", fill=255, font=font)
        draw.text((0, 16), "In server mode \nVisit website: \nraspberrypi.local:5000", fill=255, font=font)
        display.image(img)
        display.display()

        mode = "server"
    else:
        draw.rectangle((0, 0, 128, 128), fill=0)
        draw.text((0, 0), "Restart to switch mode ", fill=255, font=font)
        draw.text((0, 16), "No press detected \nEntering bike mode", fill=255, font=font)
        display.image(img)
        display.display()

        try:
            time.sleep(1)
        except KeyboardInterrupt:
            display.clear()
            display.display()
            quit()

        mode = "bike"
    
    try:
        # run respective programs
        if (mode == "bike"):
            handle_bike_mode()
        elif (mode == "server"):
            subprocess.call(CMD_SERVER_MODE.split())
    except KeyboardInterrupt:
        # clear display if keyboard interrupt
        display.clear()
        display.display()
    except OSError as e:
        print(e)
        pass
    
    display.clear()
    display.display()
    quit()
    

if (__name__ == "__main__"):
    main()
