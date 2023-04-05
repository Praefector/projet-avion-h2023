import board
import pwmio
import time
import digitalio
import analogio
import terminalio
from adafruit_motor import motor
from adafruit_display_text import bitmap_label
from displayio import Group

pwmPos = pwmio.PWMOut(board.A4, duty_cycle=2 ** 15, frequency=50)
pwnNeg = pwmio.PWMOut(board.A5, duty_cycle=2 ** 15, frequency=50)

enable = digitalio.DigitalInOut(board.A3)
enable.direction = digitalio.Direction.OUTPUT

enable.value = True

potJoystickY = analogio.AnalogIn(board.A1)

motor = motor.DCMotor(pwmPos, pwnNeg)

#Écran TFT
scale = 2
textArea = bitmap_label.Label(terminalio.FONT, scale = scale)
textArea.anchor_point = (0.5, 0.5)
textArea.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
textGroup = Group()
textGroup.append(textArea)
board.DISPLAY.show(textGroup)

temps = time.monotonic()

while True:
    val = potJoystickY.value * 200.00 / 52288
    trueVal = (val * 2.00 / 200.00) - 1.00
    if(trueVal < 0.6 and trueVal > -0.1):
        trueVal = 0

    motor.throttle = trueVal

    if (temps + 0.2) < time.monotonic() :
        textArea.text = "Puissance : " + str(trueVal) + '\n' + "Val : " + str(potJoystickY.value) + '\n' + "Val(200) : " + str(val)
        temps = time.monotonic()
