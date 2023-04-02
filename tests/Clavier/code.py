import board
import busio
import adafruit_aw9523
import time
import digitalio

#i2c = board.I2C()
i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA
aw = adafruit_aw9523.AW9523(i2c)


rows = [aw.get_pin(15), aw.get_pin(14), aw.get_pin(13), aw.get_pin(12)]
cols = [aw.get_pin(7), aw.get_pin(6), aw.get_pin(5), aw.get_pin(4)]
keys = ((1, 2, 3, "A"),
        (4, 5, 6, "B"),
        (7, 8, 9, "C"),
        ('*', 0, '#', "D"))


keymap=[]
keymap.append('123A')
keymap.append('456B')
keymap.append('789C')
keymap.append('*0#D')

for pin in rows:
   pin.direction = digitalio.Direction.INPUT
for pin in cols:
   pin.direction = digitalio.Direction.INPUT

old_row=0;
for pin in rows:
    pin.value=1

switch_state = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]
               ]
while True:
    for r in range(4):
        rows[old_row].value=1
        rows[r].value=0
        old_row=r
        for c in range(4):
            if (cols[c].value==0 and switch_state[r][c]==0):
                switch_state[r][c]=1
                print(keys[r][c])
            if (cols[c].value==1 and switch_state[r][c]==1):
                switch_state[r][c]=0
    time.sleep(0.01)  # debounce