# Pico Thermometer
A simple and fun Raspberry Pi project! Turn an inexpensive [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/), a [DHT-22 sensor](https://www.adafruit.com/product/385), an [SSD-1306 OLED display](https://www.adafruit.com/product/326), and [a few 3D-printed parts](https://www.thingiverse.com/thing:6691193) into a temperature monitor for any room in your home!

![img2](https://i.imgur.com/fLneAjs.png)

## How to Setup
1. 3D-print the STL files found [here on Thingiverse](https://www.thingiverse.com/thing:6691193).
2. Mount your SSD-1306 OLED display to the **top.stl** you printed (the lid of the box) with four M2 screws.
3. If you printed the bottom with the hole (recommended), slip your wires through the hole, connected to the DHT-22 sensor externally, and the Raspberry Pi Pico internally (soldered).
4. Using [Thonny](https://thonny.org/) deploy the [source code](./src/) to the Pico. If you're not using the exact wiring I am using (same GPIOs), be sure to modify the source code according to your wiring!
5. Place the Raspberry Pi Pico at the bottom of the box, but ensure the USB port is positioned so it can be accessed by the semi-circle hole in the box (this will be how your supply power).
5. Screw on the lid with four M2 screws.
6. Mount to a wall with some simple double sided tape, and plug it in!

After deploying, you will see the Pico poll the ambient temperature and update the display once per minute. There is a "loading bar" at the bottom of the display that slowly grows to the full width of the display, indicating how long it is to its next read and print cycle.

## Image Gallery
![Cover](https://i.imgur.com/0bu5Jq6.jpeg)

![cover](https://i.imgur.com/fR1BD5F.jpeg)

![wired](https://i.imgur.com/DYd0QDj.jpeg)

![in box](https://i.imgur.com/8QaKE0T.jpeg)