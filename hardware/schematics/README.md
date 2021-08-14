# Wiring

![wiring diagram](/docs/img/bd_schematic_clear.png)
This is the wiring diagram. Go [here](/docs/img/bd_schematic_clear.png) for a clearer image.

## Raspberry Pi
The left side of the arrow is the pin on the component and the right side is the pin on the Raspberry Pi. For example, `VCC -> 5V` on the GPS would mean to wire `VCC` on the GPS to `5V` on the Raspberry Pi.

1. The GPS
    - `VCC -> 5V`
    - `GND -> GND`
    - `TX -> RX` or `GPIO 15`
    - `RX -> TX` or `GPIO 14`
2. The OLED
    - `VCC -> 5V`
    - `GND -> GND`
    - `SCL -> SCL` or `GPIO 3`
    - `SDA -> SDA` or `GPIO 2`
3. Button 1:
    - Wire one pin to `GPIO 17`
    - Wire the pin across from it to `GND`
4. Button 2:
    - Do the same with button 1 but to `GPIO 18` instead of `17`

## Arduino
1. Error LED: Wire the positive side to `D3` on the Arduino and the negative side to a 220 ohm resistor to ground.
2. Tracking LED: Wire the positive side to `D2` on the Arduino and the negative side to a 220 ohm resistor to ground.
3. Start/stop tracking button: Wire one pin to 5V. Wire the pin across from it to `D4`, and wire the same pin to a 10k ohm resistor to ground.
4. Pause/resume tracking button: Do the same as above but wire it to `D5` instead of `D4`.
5. LED Panel: See picture above. The negative pins of the LEDs get wired to the pins below (pins 8-A5). That is, the wire coming out from the bottom side of an LED in the diagram gets wired to the negative pin of that LED.

Lastly, connect the Raspberry Pi and the Arduino using a USB cable.

