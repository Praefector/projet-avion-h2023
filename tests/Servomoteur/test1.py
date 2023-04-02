import board
import pwmio
import time
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)
servoMotor = servo.Servo(pwm)

#500
#2300

while True:
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        servoMotor.angle = angle
        time.sleep(0.05)
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        servoMotor.angle = angle
        time.sleep(0.05)