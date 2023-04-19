import digitalio
import busio
import adafruit_tca8418
import time
import board

### Expension Board ### À CHANGER LORSQUE NOUVEAU BOARD REÇU

i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA
tca = adafruit_tca8418.TCA8418(i2c)

### PWR Button ###
#tca.gpio_mode[TCA8418.R7] = True
#tca.gpio_direction[TCA8418.R7] = False
#tca.pullup[TCA8418.R7] = True

pwr = adafruit_tca8418.DigitalInOut(6, tca)
pwr.direction = digitalio.Direction.INPUT


while True:
    print(pwr.value)
    time.sleep(1)