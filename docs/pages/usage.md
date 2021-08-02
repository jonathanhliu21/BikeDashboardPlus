# How to use your Bike Dashboard

There are 2 modes to the Bike Dashboard: Bike mode, and server mode. Bike mode is the mode that you set when you are actually riding your bike. The OLED display will display time, speed, etc., and you are able to track your route. Server Mode sets up a server where you can configure your Bike Dashboard and where you can view the maps of your tracked routes.

## Bike Mode
The Bike Dashboard automatically goes into Bike Mode when it boots up. 

After displaying some setup text, the OLED will display the things you will see in Bike Mode. This diagram will show what each thing displayed on the OLED represents:

![Bike_mode_OLED_tutorial]()

This is how the LED panel works and how the LEDs are numbered:  
![LED_panel_tutorial]()  
If you are going *x* mph, or *x* km/h, or *x* m/s, depending on your configuration which we will get to later, then LED *x* will light up.

To start tracking, press the button wired to pin D4 on the Arduino Nano. The green LED on the Arduino will light up and a "T" will show up on the bottom right of the OLED display to indicate that you are currently tracking. **Note that tracking is not possible if you are disconnected** i.e. the red LED is on or it says "M:D" on the OLED.

Once you have started tracking, it will immediately write to a new track file. If you have started this by accident, don't worry, you can delete this later. 

To pause tracking, press the button wired to pin D5 on the Arduino. Indicators that you have paused are the green LED blinking instead of staying constatly on and the OLED display a "P" on the bottom right corner. To resume, press the same button. 

To end tracking, press the same button as the one you pressed when you started tracking. The green LED will turn off and there should be nothing displayed on the bottom right corner of the OLED. 

## Server Mode
