import board
import pwmio
import time
import digitalio
from adafruit_motor import motor

pwmPos = pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
pwnNeg = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

pinA0 = digitalio.DigitalInOut(board.A0)
pinA0.direction = digitalio.Direction.OUTPUT

pinA0.value = True

motor = motor.DCMotor(pwmPos, pwnNeg)
temps = time.monotonic()

motor.throttle = 0

print(motor.throttle)

while True:

    print("etape 1")
    motor.throttle = 0
    while (temps + 5) > time.monotonic():
        motor.throttle += 0.2
        time.sleep(1)
        
    temps = time.monotonic()
    print(motor.throttle)

    print("etape 2")
    while (temps + 10) > time.monotonic():
        motor.throttle += -0.2
        time.sleep(1)

    temps = time.monotonic()
    print(motor.throttle)

    print("etape 3")
    while (temps + 5) > time.monotonic():
        motor.throttle += 0.2
        time.sleep(1)

    temps = time.monotonic()
    print(motor.throttle)

    
