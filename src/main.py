import machine
import sys
import time
import dht
import framebuf
import ssd1306

# SETTINGS - data pin for the DHT-22 sensor
gpio_dht22 = 6

# SETTINGS - I2C pins for the SSD-1306 OLED display
i2c_peripheral = 1 # depending on what pins you use for I2C, will be 0 or 1
i2c_sda = 14
i2c_scl = 15

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
def display_reading(temp:int) -> None:

    # load in the bufs
    to_display:list[framebuf.FrameBuffer] = []
    for c in str(temp):
        if c == "0":
            to_display.append(buf0)
        elif c == "1":
            to_display.append(buf1)
        elif c == "2":
            to_display.append(buf2)
        elif c == "3":
            to_display.append(buf3)
        elif c == "4":
            to_display.append(buf4)
        elif c == "5":
            to_display.append(buf5)
        elif c == "6":
            to_display.append(buf6)
        elif c == "7":
            to_display.append(buf7)
        elif c == "8":
            to_display.append(buf8)
        elif c == "9":
            to_display.append(buf9)

    # display
    on_x = int(round((128 - (len(to_display) * 32)) / 2, 0))
    for fb in to_display:
        oled.blit(fb, on_x, 16)
        on_x = on_x + 32
    oled.show()

## function for bottom loading bar
def loading_bar(percent:float, height:int = 3) -> None:
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
        temperature_f:int = None
        while temperature_f == None:
            try:
                print("Measuring from DHT-22 on attempt # " + str(dht22_attempts + 1) + "...")
                dht22.measure()
                temperature_c = dht22.temperature()
                temperature_f = int(round((temperature_c * (9/5)) + 32, 0))
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
        start_sleep_ticks_ms = time.ticks_ms()
        while (time.ticks_ms() - start_sleep_ticks_ms) < 60000:
            elapsed_ms:int = time.ticks_ms() - start_sleep_ticks_ms
            duration_percent:float = elapsed_ms / 60000
            loading_bar(duration_percent)
            time.sleep(0.1)