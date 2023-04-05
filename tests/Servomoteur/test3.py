import board
import pwmio
import analogio
import time
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.RX, duty_cycle=2 ** 15, frequency=50)
servoMotor = servo.Servo(pwm, min_pulse=500, max_pulse=2300)   
pot = analogio.AnalogIn(board.A0)

while True:
    val = pot.value * 180 / 52288
    servoMotor.angle = val
