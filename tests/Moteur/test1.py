import board
import pwmio
import time
import digitalio
from adafruit_motor import motor

pwmPos = pwmio.PWMOut(board.D12, duty_cycle=2 ** 15, frequency=50)
pwnNeg = pwmio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)

pinD11 = digitalio.DigitalInOut(board.D11)
pinD11.direction = digitalio.Direction.OUTPUT

pinD11.value = True

motor = motor.DCMotor(pwmPos, pwnNeg)
temps = time.monotonic()

while True:

    print("1")
    motor.throttle = 0
    while (temps + 5) > time.monotonic():
        motor.throttle += 0.2
        
    temps = time.monotonic()

    print("2")
    while (temps + 10) > time.monotonic():
        motor.throttle += -0.2

    temps = time.monotonic()

    print("3")
    while (temps + 5) > time.monotonic():
        motor.throttle += 0.2

    temps = time.monotonic()

    
