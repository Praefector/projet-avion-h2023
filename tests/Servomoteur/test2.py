import board
import pwmio
import time
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)
patte_servo = servo.Servo(pwm)

while True:
    userInput = int(input("Entrez un angle entre 0 et 180 degrées : "))

    if userInput <= 180 and userInput >= 0 and userInput != "":
        patte_servo.angle = userInput