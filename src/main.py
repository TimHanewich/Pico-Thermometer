import machine
import bitgraphics
import sys
import time
import dht

# SETTINGS - data pin for the DHT-22 sensor
gpio_dht22 = 6

# SETTINGS - I2C pins for the SSD-1306 OLED display
i2c_peripheral = 1 # depending on what pins you use for I2C, will be 0 or 1
i2c_sda = 14
i2c_scl = 15

# create I2C interface
i2c = machine.I2C(i2c_peripheral, sda=machine.Pin(i2c_sda), scl=machine.Pin(i2c_scl))
if 60 not in i2c.scan():
    print("SSD-1306 OLED display not detected on I2C! Program cancelling.")
    sys.exit()

# set up DHT-22 sensor
dht22 = dht.DHT22(machine.Pin(gpio_dht22, machine.Pin.IN))
    
# create display
bgd = bitgraphics.BitGraphicDisplay(i2c, 128, 64) # create BitGraphicDisplay with width 128, height 64

# create typewriter and load in 32x32 graphics
tr = bitgraphics.Typewriter()
tr.add_character("0", bitgraphics.BitGraphic(path="graphics/0.json"))
tr.add_character("1", bitgraphics.BitGraphic(path="graphics/1.json"))
tr.add_character("2", bitgraphics.BitGraphic(path="graphics/2.json"))
tr.add_character("3", bitgraphics.BitGraphic(path="graphics/3.json"))
tr.add_character("4", bitgraphics.BitGraphic(path="graphics/4.json"))
tr.add_character("5", bitgraphics.BitGraphic(path="graphics/5.json"))
tr.add_character("6", bitgraphics.BitGraphic(path="graphics/6.json"))
tr.add_character("7", bitgraphics.BitGraphic(path="graphics/7.json"))
tr.add_character("8", bitgraphics.BitGraphic(path="graphics/8.json"))
tr.add_character("9", bitgraphics.BitGraphic(path="graphics/9.json"))
tr.add_character("d", bitgraphics.BitGraphic(path="graphics/degree_fahrenheit.json"))

while True:

    # measure temperature
    print("Reading temperature from DHT-22...")
    dht22_attempts:int = 0
    temperature_f:int = None
    while temperature_f == None and dht22_attempts < 10:
        try:
            print("Measuring from DHT-22 on attempt # " + str(dht22_attempts + 1) + "...")
            dht22.measure()
            temperature_c = dht22.temperature()
            temperature_f = int(round((temperature_c * (9/5)) + 32, 0))
        except Exception as e:
            print("Reading attempt failed! Exception msg: " + str(e))
        dht22_attempts = dht22_attempts + 1
        time.sleep(0.25)

    # show it on the display
    print("Displaying temperature of " + str(temperature_f) + "...")
    bg = tr.write(str(temperature_f) + "d", 32, 32)
    bgd.clear()
    bgd.display(bg, center=(0.5, 0.5))
    bg.show()

    # do it again in one minute
    print("Sleeping for 60 seconds...")
    time.sleep(60)