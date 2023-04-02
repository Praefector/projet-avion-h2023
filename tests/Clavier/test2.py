import board
import keypad
from adafruit_hid.keycode import Keycode

km = keypad.KeyMatrix(
    row_pins=(board.D13, board.D12, board.D11, board.D10),
    column_pins=(board.D9, board.D6, board.D5, board.SCL),
)

KEYCODES = (
    "1","2","3","A",
    "4","5","6","B",
    "7","8","9","C",
    "*","0","#","D",
)

entree = ""

while True:
    event = km.events.get()
    if event:
        if event.pressed:
            key_number = event.key_number
            
            if KEYCODES[key_number] == "#":
                nbr = int(entree)
                entree = ""
                nbrPow = pow(nbr, 2)
                print(nbrPow)
            else:
                entree += KEYCODES[key_number]
                print(entree)
