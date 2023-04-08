import digitalio
import busio
import adafruit_aw9523
import time
import board

### Expension Board ### À CHANGER LORSQUE NOUVEAU BOARD REÇU

i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA
aw9523 = adafruit_aw9523.AW9523(i2c)

### PWR Button ###
pwrButton = aw9523.get_pin(0)
pwrButton.direction = digitalio.Direction.INPUT

while True:
    print(pwrButton.value)
    time.sleep(1)