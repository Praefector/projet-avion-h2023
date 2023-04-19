import time
import board
import analogio
import terminalio
import neopixel
from  math import atan2
from math import degrees
from adafruit_display_text import bitmap_label
from displayio import Group

MAX_JOYSTICK_VAL = 52388
MID_JOYSTICK_VAL = 26194
MIN_JOYSTICK_VAL = 380
MAX_DEGREES = 360

COLORS = {'red':(255, 0, 0), 'yellow':(255, 255, 0), 'green':(0, 255, 0), 'white':(255, 255, 255), 'off':(0, 0, 0)}
ANGLE_RANGE = (0, 45, 90 , 135, 180, 225, 270, 315, 360)

joystickAxisX = analogio.AnalogIn(board.A0)
joystickAxisY = analogio.AnalogIn(board.A1)

scale = 2
textArea = bitmap_label.Label(terminalio.FONT, scale = scale)
textArea.anchor_point = (0.5, 0.5)
textArea.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
textGroup = Group()
textGroup.append(textArea)
board.DISPLAY.show(textGroup)

ledBoard = neopixel.NeoPixel(board.SDA, 8)
ledBoard.brightness = 0.1
ledBoard.fill(COLORS['off'])

while True:
    axisYVal = ((joystickAxisY.value - MIN_JOYSTICK_VAL) / MAX_JOYSTICK_VAL) - 0.5
    axisXVal = ((joystickAxisX.value - MIN_JOYSTICK_VAL) / MAX_JOYSTICK_VAL) - 0.5
    joystickAngle = degrees(atan2(axisYVal, axisXVal) + MAX_DEGREES) % MAX_DEGREES

    if (axisXVal < 0.26 and axisXVal > 0.24) and (axisYVal < 0.13 and axisYVal > 0.11):
        joystickAngle = -1

    if joystickAngle == -1:
        ledIndex = -1
    elif joystickAngle > ANGLE_RANGE[0] and joystickAngle < ANGLE_RANGE[1]:
        ledIndex = 0
    elif joystickAngle < ANGLE_RANGE[2]:
        ledIndex = 1
    elif joystickAngle < ANGLE_RANGE[3]:
        ledIndex = 2
    elif joystickAngle < ANGLE_RANGE[4]:
        ledIndex = 3
    elif joystickAngle < ANGLE_RANGE[5]:
        ledIndex = 4
    elif joystickAngle < ANGLE_RANGE[6]:
        ledIndex = 5
    elif joystickAngle < ANGLE_RANGE[7]:
        ledIndex = 6
    else :
        ledIndex = 7

    ledBoard.fill(COLORS['off'])
    if ledIndex != -1:
        ledBoard[ledIndex] = COLORS['white']

    ledBoard.write()
    textArea.text = "Axis X : " + str(axisXVal) + "\n" + "Axis Y : " + str(axisYVal) + "\n" + "Angle : " + str(joystickAngle) + "\n" + "index : " + str(ledIndex)
    time.sleep(1)


