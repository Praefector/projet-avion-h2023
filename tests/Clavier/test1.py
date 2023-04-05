import board
import keypad
from adafruit_hid.keycode import Keycode
import busio
import adafruit_aw9523

i2c = busio.I2C(scl=board.SCL, sda=board.SDA)  # uses board.SCL and board.SDA
aw = adafruit_aw9523.AW9523(i2c)

km = keypad.KeyMatrix(
    row_pins=(aw.get_pin(15), aw.get_pin(14), aw.get_pin(13), aw.get_pin(12)),
    column_pins=(aw.get_pin(7), aw.get_pin(6), aw.get_pin(5), aw.get_pin(4)),
)


KEYCODES = (
    "1","2","3","A",
    "4","5","6","B",
    "7","8","9","C",
    "*","0","#","D",
)



while True:
    event = km.events.get()
    if event:
        if event.pressed:
            key_number = event.key_number
            print(KEYCODES[key_number])