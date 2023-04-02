import board
import pwmio
import time
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.RX, duty_cycle=2 ** 15, frequency=50)
servoMotor = servo.Servo(pwm, min_pulse=500, max_pulse=2300)   

while True:
    userInput = int(input("Entrez un angle entre 0 et 180 degrées : "))

    if userInput <= 180 and userInput >= 0 and userInput != "":
        servoMotor.angle = userInput