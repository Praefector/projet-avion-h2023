import board
import pwmio
import time
import digitalio
import analogio
import terminalio
from adafruit_motor import motor
from adafruit_display_text import bitmap_label
from displayio import Group

pwmPos = pwmio.PWMOut(board.D12, duty_cycle=2 ** 15, frequency=50)
pwnNeg = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)

pinD11 = digitalio.DigitalInOut(board.D11)
pinD11.direction = digitalio.Direction.OUTPUT
pinD11.value = True

pinA0 = analogio.AnalogIn(board.A0)

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
    val = pinA0.value * 200.00 / 52288
    trueVal = (val * 2.00 / 200.00) - 1.00
    motor.throttle = trueVal

    if (temps + 0.2) < time.monotonic() :
        textArea.text = "Puissance : " + trueVal
        temps = time.monotonic()
