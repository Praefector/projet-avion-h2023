import board
import pwmio
import analogio
import time
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)
patte_servo = servo.Servo(pwm)
pinD6 = analogio.AnalogIn(board.D13)

while True:
    val = pinD6.value * 180 / 52288
    patte_servo.angle = val
