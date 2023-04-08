import board
import pwmio
import time
import neopixel
import mfrc522
import adafruit_hcsr04
import adafruit_dht
import terminalio
import analogio
import digitalio
import busio
import adafruit_aw9523
from math import atan2
from math import degrees
from adafruit_motor import servo
from adafruit_motor import motor
from adafruit_display_text import bitmap_label
from displayio import Group

######## STARTING STATE #########

### Expension Board ### À CHANGER LORSQUE NOUVEAU BOARD REÇU

i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA
aw9523 = adafruit_aw9523.AW9523(i2c)

### General attributes ###
tempCelcius = 0
humidity = 0
currentDestination = ""
motorPower = 0
finAngle = 0
isFlightSettingsLocked = False

### Finals
MAX_8BIT = 255
MIN_8BIT = 0

MAX_JOYSTICK_VAL = 52388
MID_JOYSTICK_VAL = 26194
MIN_JOYSTICK_VAL = 380

MAX_DEGREES = 360

COLORS = {'red':(255, 0, 0), 'yellow':(255, 255, 0), 'green':(0, 255, 0), 'white':(255, 255, 255), 'off':(0, 0, 0)}
ANGLE_RANGE = (0, 45, 90 , 135, 180, 225, 270, 315, 360)

### Time ###
passedTime = time.monotonic()
lcdPassedTime = time.monotonic()

### Joystick ###
joystickAxisX = analogio.AnalogIn(board.A0)
joystickAxisY = analogio.AnalogIn(board.A1)
joystickButton = digitalio.DigitalInOut(board.A2)
joystickButton.switch_to_input(pull=digitalio.Pull.UP)

### Screen ###
scale = 1
textArea = bitmap_label.Label(terminalio.FONT, scale = scale)
textArea.anchor_point = (0.5, 0.5)
textArea.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
textGroup = Group()
textGroup.append(textArea)
board.DISPLAY.show(textGroup)

### DHT ###
dht = adafruit_dht.DHT11(board.TX)

### Servomotor ###
finPWM = pwmio.PWMOut(board.RX, duty_cycle=2 ** 15, frequency=50)
fin = servo.Servo(finPWM, min_pulse=500, max_pulse=2300)

### Motor ###
motorPWMPositive = pwmio.PWMOut(board.A4, duty_cycle=2 ** 15, frequency=50)
motorPWMNegative = pwmio.PWMOut(board.A5, duty_cycle=2 ** 15, frequency=50)

enableMotor = digitalio.DigitalInOut(board.A3)
enableMotor.direction = digitalio.Direction.OUTPUT
enableMotor.value = False

motor = motor.DCMotor(motorPWMPositive, motorPWMNegative)
motor.throttle = 0

### Sonar ###
distanceSonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D9, echo_pin=board.D6)

### PixelLed Module ###
pixelLed = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixelLed.brightness = 1

### LED Ring

#ledBoard = neopixel.NeoPixel(PIN PIN PIN, 8)
#ledBoard.brightness = 0.1
#ledBoard.fill(COLORS['off'])


### PWR Button ###
pwrButton = aw9523.get_pin(0)
pwrButton.direction = digitalio.Direction.INPUT

### AIRPORTS CODES ###

airports = {
    101 : "YUL Montreal",
    111 :  "ATL Atlanta",
    222 : "HND Tokyo",
    764 : "LHR London",
    492 : "CAN Baiyun",
    174 : "CDG Paris",
    523 : "AMS Amsterdam"
}

### RFID CODES ###

rfid = {
    
}

def starting_state():
    return state_3()

    #RFID

    #FAIRE LE CHECK LORSQUE RFID FONCTIONNEL
    #while True:
     #   if evenement_externe_1():
     #       # Transition vers l'état 1
     #       return etat_1()
     #   
     #   elif evenement_externe_2():
     #       # Transition vers l'état 2
     #       return etat_2()
      #  else:

      #      # Attente d'un événement externe
      #      attendre_evenement()


def state_1():
    pixelLed.fill(COLORS['red'])
    enableMotor.value = False
    #position attente
    fin.angle = 90

    textArea.text = "Scannez carte"

    # Actions à effectuer lors de l'entrée dans l'état 1
    while True:
        if evenement_externe_3():
            # Transition vers l'état final
            return etat_final()
        else:
            # Attente d'un événement externe
            attendre_evenement()

def state_2():
    pixelLed.fill(COLORS['yellow'])
    textArea.text = "Afficher sur LCD : \n Entrez code destination sur ligne 1"

    while True:
        if evenement_externe_4():
            # Transition vers l'état final
            return etat_final()
        else:
            # Attente d'un événement externe
            attendre_evenement()

def state_3():

    #Empêche le plantage vu non déclaré ???
    enableMotor.value = True
    pixelLed.fill(COLORS['green'])
    isFlightSettingsLocked = False
    motor.throttle = 0
    fin.angle = 90
    tempCelcius = 0
    humidity = 0
    lcdPassedTime = time.monotonic()
    ledIndex = 0

    ## debug
    currentDestination = "YSC Sherbrooke"

    while pwrButton :

        if not joystickButton.value :
            print("enetring joystick if statement")
            if isFlightSettingsLocked :
                isFlightSettingsLocked = False
                print("isFlight set to False")
            else :
                isFlightSettingsLocked = True
                print("isFlight set to True")

        if not isFlightSettingsLocked :
            ## motor
            motorValue8bit = (joystickAxisY.value - MIN_JOYSTICK_VAL) * MAX_8BIT / MAX_JOYSTICK_VAL
            trueMotorVal = (motorValue8bit * 2.00 / MAX_8BIT) - 1.00
            #pour compenser la calibration ignoble du joystick ig
            if(trueMotorVal < 0.6 and trueMotorVal > -0.1):
                trueMotorVal = 0

            #Empêche erreurs
            if trueMotorVal < -0.98:
                motor.throttle = -1
            elif trueMotorVal > 0.98:
                motor.throttle = 1
            else :
                motor.throttle = trueMotorVal

            ## servo
            finValue8bit = (joystickAxisX.value - MIN_JOYSTICK_VAL) * MAX_8BIT / MAX_JOYSTICK_VAL
            #pour compenser la calibration ignoble du joystick ig
            if(finValue8bit < 195 and finValue8bit > 128):
                finValue8bit = 128
            finAngle = finValue8bit * 180 / MAX_8BIT

            #Empêche erreurs
            if finAngle < 0:
                fin.angle = 0
            elif finAngle > 180:
                fin.angle = 180
            else :
                fin.angle = finAngle

            #Indication position joystick avec ledBoard
            axisYVal = ((joystickAxisY.value - MIN_JOYSTICK_VAL) / MAX_JOYSTICK_VAL) - 0.5
            axisXVal = ((joystickAxisX.value - MIN_JOYSTICK_VAL) / MAX_JOYSTICK_VAL) - 0.5
            joystickAngle = degrees(atan2(axisYVal, axisXVal) + MAX_DEGREES) % MAX_DEGREES

            #Zone neutre
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

            #ledBoard.fill(COLORS['off'])
            if ledIndex != -1:
                #ledBoard[ledIndex] = COLORS['white']
                "temp, enlève moi"

        #Empèche le plantage du esp si spike de courant pour DHT
        try :
            tempCelcius = dht.temperature
            humidity = dht.humidity
            motorPower = motor.throttle * 100

        except RuntimeError as error:
            print(error.args[0])
            continue
    
        if lcdPassedTime + 0.1 < time.monotonic():
            textArea.text = "Puissance moteur : " + str(int(motorPower)) + " %\n" + "Angle aileron : " + str(int(finAngle)) + " deg\n" + "Destination : " + str(currentDestination) + "\n" + "Température : " + str(tempCelcius) + " C\n" + "Humidité : " + str(humidity) + " %\n" + "Autopilote : " + str(isFlightSettingsLocked)
            lcdPassedTime = time.monotonic()


    return state_1()

def main():
    
    # Initialisation de la machine à états finis
    #current_state = starting_state()

    while True:
        # Exécution de l'état courant
        #current_state = starting_state()

        current_state = state_3()

        # Sortie de la boucle si l'état final est atteint
        if current_state == None:
            break

main()