import time
import board
import analogio
import terminalio
from  math import atan
from math import degrees
from adafruit_display_text import bitmap_label
from displayio import Group

axisX = analogio.AnalogIn(board.A0)
axisY = analogio.AnalogIn(board.A1)

maxPot = 52388
midPot = 52388/2
minPot = 595

scale = 2
textArea = bitmap_label.Label(terminalio.FONT, scale = scale)
textArea.anchor_point = (0.5, 0.5)
textArea.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
textGroup = Group()
textGroup.append(textArea)
board.DISPLAY.show(textGroup)

temps = time.monotonic()

angle = 0

while True:

    posX = axisX.value - midPot
    posY = axisY.value - midPot
    
    if (posX > 6200 and posX < 7200):
        posX = 0
    elif (posX == -25599):
        posX = -26194

    if (posY > 6200 and posY < 7200):
        posY = 0
    elif (posY == -25599):
        posY = -26194

    if (posY > 0 and posX > 0):
        angle = degrees(atan(abs(posY/posX))) + 90
    elif (posY > 0 and posX < 0):
        angle = degrees(atan(abs(posX/posY))) + 180
    elif (posY < 0 and posX < 0):
        angle = degrees(atan(abs(posY/posX))) + 270
    elif (posY < 0 and posX > 0):
        angle = degrees(atan(abs(posX/posY)))


    textArea.text = "Axis X : " + str(posX) + "\n" + "Axis Y : " + str(posY) + "\n" + "Angle : " + str(angle)
    #textArea.text = "Axis X : " + str(axisX.value) + "\n" + "Axis Y : " + str(axisY.value)
    time.sleep(0.5)



