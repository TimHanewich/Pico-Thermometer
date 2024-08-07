print("Pico Thermometer, created by Tim Hanewich")
print("For more information, visit https://github.com/TimHanewich/Pico-Thermometer")
print("")
print("Copyright (c) 2024 Tim Hanewich")
print("Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:")
print("The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.")
print("THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")

import machine
import sys
import time
import dht
import framebuf
import ssd1306



########## SETTINGS ##########

# sample rate
sample_rate_seconds:int = 60

# data pin for the DHT-22 sensor
gpio_dht22 = 28

# I2C pins for the SSD-1306 OLED display
i2c_peripheral = 1 # depending on what pins you use for I2C, will be 0 or 1
i2c_sda = 14
i2c_scl = 15

##############################



# create I2C interface
print("Creating I2C interface...")
i2c = machine.I2C(i2c_peripheral, sda=machine.Pin(i2c_sda), scl=machine.Pin(i2c_scl))
if 60 not in i2c.scan():
    print("SSD-1306 OLED display not detected on I2C! Program cancelling.")
    sys.exit()
else:
    print("SSD-1306 I2C presence confirmed!")

# set up DHT-22 sensor
print("Setting up DHT22 sensor...")
dht22 = dht.DHT22(machine.Pin(gpio_dht22, machine.Pin.IN))

# set up SSD-1306 OLED display
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# load number bufs (32x32) into memory
def load(path:str) -> framebuf.FrameBuffer:
    f = open(path, "rb")
    data = f.read()
    f.close()
    return framebuf.FrameBuffer(bytearray(data), 32, 32, framebuf.MONO_HLSB)

buf0 = load("graphics/0")
buf1 = load("graphics/1")
buf2 = load("graphics/2")
buf3 = load("graphics/3")
buf4 = load("graphics/4")
buf5 = load("graphics/5")
buf6 = load("graphics/6")
buf7 = load("graphics/7")
buf8 = load("graphics/8")
buf9 = load("graphics/9")

# function we can call on to display
def display_reading(temp:float) -> None:

    # configurable settings
    period_radius_x:int = 3 # period X radius (width radius)
    period_radius_y:int = 3 # period Y radius (height radius)
    char_buffer:int = 0 # buffer in between characters (0 default)

    # calculate total width
    width:int = 0
    for c in str(temp):

        # add raw width
        if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            width = width + 32
        elif c == ".":
            width = width + period_radius_x + period_radius_x # radius x twice because the DIAMETER is the width (twice radius)
        else:
            raise Exception("Unable to display reading with character '" + c + "'")
        
        # add buffer
        width = width + char_buffer

    # now that we have the width of the entire structure, position begin x accordingly
    on_x:int = int(round((128 - width) / 2, 0))

    # display each, taking note of the location of a period
    period_location:tuple[int, int] = None
    for c in str(temp):
        if c == "0":
            oled.blit(buf0, on_x, 16)
            on_x = on_x + 32
        elif c == "1":
            oled.blit(buf1, on_x, 16)
            on_x = on_x + 32
        elif c == "2":
            oled.blit(buf2, on_x, 16)
            on_x = on_x + 32
        elif c == "3":
            oled.blit(buf3, on_x, 16)
            on_x = on_x + 32
        elif c == "4":
            oled.blit(buf4, on_x, 16)
            on_x = on_x + 32
        elif c == "5":
            oled.blit(buf5, on_x, 16)
            on_x = on_x + 32
        elif c == "6":
            oled.blit(buf6, on_x, 16)
            on_x = on_x + 32
        elif c == "7":
            oled.blit(buf7, on_x, 16)
            on_x = on_x + 32
        elif c == "8":
            oled.blit(buf8, on_x, 16)
            on_x = on_x + 32
        elif c == "9":
            oled.blit(buf9, on_x, 16)
            on_x = on_x + 32
        elif c == ".":
            period_location = (on_x + period_radius_x, 16 + 32 - period_radius_y - period_radius_y)
            on_x = on_x + period_radius_x + period_radius_x

        # opportunity here to add in buffer width between characters
        on_x = on_x + char_buffer

    # add the period if there is one
    # the reason we have to add the period AFTER every other number is added is because if a number graphic has a pixel turned off at the very edge, it will "overwrite" part of the period, truncating a portion of it.
    if period_location != None:
        oled.ellipse(period_location[0], period_location[1], period_radius_x, period_radius_y, 1, True)

    # show!
    oled.show()

## function for bottom loading bar
def loading_bar(percent:float, height:int = 6) -> None:
    oled.rect(0, 64-height, 128, height, 0, True) # clear any old progress bar that was previously there
    rwidth:int = int(round(128 * percent, 0)) # calculate rectangle width
    oled.rect(0, 64-height, rwidth, height, 1, True) # display as filled in rectangle at bottom
    oled.show()

# infinite reading loop
def loop():
    print("Beginning thermometer loop!")
    while True:

        # measure temperature
        print("Reading temperature from DHT-22...")
        dht22_attempts:int = 0
        temperature_f:float = None
        while temperature_f == None:
            try:
                print("Measuring from DHT-22 on attempt # " + str(dht22_attempts + 1) + "...")
                dht22.measure()
                temperature_c = dht22.temperature()
                temperature_f = round((temperature_c * (9/5)) + 32, 1)
            except Exception as e:
                print("Reading attempt failed! Exception msg: " + str(e))
            dht22_attempts = dht22_attempts + 1
            time.sleep(0.25)

        # before displaying anything, clear all
        oled.fill(0)

        # display temp
        print("Displaying temperature reading of '" + str(temperature_f) + "'...")
        display_reading(temperature_f)

        # do it again in one minute
        print("Sleeping for 60 seconds...")
        wait_ms:int = sample_rate_seconds * 1000
        start_sleep_ticks_ms = time.ticks_ms()
        while (time.ticks_ms() - start_sleep_ticks_ms) < wait_ms:
            elapsed_ms:int = time.ticks_ms() - start_sleep_ticks_ms
            duration_percent:float = elapsed_ms / wait_ms
            loading_bar(duration_percent)
            time.sleep(0.1)

loop()