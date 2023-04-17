import board
import pwmio
import time
import wifi
import ssl
import socketpool
import adafruit_requests
import os
import neopixel
import mfrc522
import adafruit_hcsr04
import adafruit_dht
import terminalio
import analogio
import digitalio
import busio
from math import atan2
from math import degrees
from adafruit_motor import servo
from adafruit_motor import motor
from adafruit_display_text import bitmap_label
import adafruit_tca8418
from displayio import Group

######## STARTING STATE #########

### Expension Board ### À CHANGER LORSQUE NOUVEAU BOARD REÇU

i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA
tca = adafruit_tca8418.TCA8418(i2c)

### General attributes ###
currentDestination = ""

### Finals ###
MAX_8BIT = 255
MIN_8BIT = 0

MAX_JOYSTICK_VAL = 52388
MID_JOYSTICK_VAL = 26194
MIN_JOYSTICK_VAL = 380

MAX_DEGREES = 360

COLORS = {'red':(255, 0, 0), 'yellow':(255, 255, 0), 'green':(0, 255, 0), 'white':(255, 255, 255), 'off':(0, 0, 0)}
ANGLE_RANGE = (0, 45, 90 , 135, 180, 225, 270, 315, 360)

KEYPAD = (("*", "0", "#", "D"), 
          ("7", "8", "9", "C"), 
          ("4", "5", "6", "B"), 
          ("1", "2", "3", "A"))

AIRPORTS = {
    "101" : "YUL Montreal",
    "111" : "ATL Atlanta",
    "222" : "HND Tokyo",
    "764" : "LHR London",
    "492" : "CAN Baiyun",
    "174" : "CDG Paris",
    "523" : "AMS Amsterdam"
}

### Keypad ###
PINS_TCA = (
    adafruit_tca8418.TCA8418.R0,
    adafruit_tca8418.TCA8418.R1,
    adafruit_tca8418.TCA8418.R2,
    adafruit_tca8418.TCA8418.R3,
    adafruit_tca8418.TCA8418.C0,
    adafruit_tca8418.TCA8418.C1,
    adafruit_tca8418.TCA8418.C2,
    adafruit_tca8418.TCA8418.C3,
)

for pin in PINS_TCA:
    tca.keypad_mode[pin] = True
    tca.enable_int[pin] = True
    tca.event_mode_fifo[pin] = True

tca.key_intenable = True


### Time ###
passedTime = time.monotonic()
lcdPassedTime = time.monotonic()

### Joystick ###
joystickAxisX = analogio.AnalogIn(board.A0)
joystickAxisY = analogio.AnalogIn(board.A1)
joystickButton = adafruit_tca8418.DigitalInOut(7, tca)
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

ledBoard = neopixel.NeoPixel(board.D6, 8)
ledBoard.brightness = 0.1
ledBoard.fill(COLORS['off'])


### PWR Button ###
pwrButton = adafruit_tca8418.DigitalInOut(6, tca)
pwrButton.direction = digitalio.Direction.INPUT

### RFID ###
rfidModule = mfrc522.MFRC522(board.D12, board.D11, board.D13, board.D5, board.D10)
rfidModule.set_antenna_gain(0x07 << 4)

### RFID CODES ###
rfidUid = [
    320
]

### WIFI ###

wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
socket = socketpool.SocketPool(wifi.radio)
context = ssl.create_default_context()
https = adafruit_requests.Session(socket,context)


### FUNCTIONS ####

def selectLedRingIndex(joystickAngle):
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

    return ledIndex

def sendData(tC, hum):
    json_data = {
        "field1": tC,
        "field2": hum,
    }
    response = https.post(os.getenv("APIPOST"), json = json_data)

def defineTempHum():

    tempC = dht.temperature
    hum = dht.humidity
    sendData(tempC, hum)


def state_1():
    pixelLed.fill(COLORS['red'])
    textArea.scale = 2
    #position attente
    enableMotor.value = False
    fin.angle = 90
    textArea.text = "Scannez carte"
    cardUid = ""
    passedTime = time.monotonic()

    #RFID
    while not cardUid in rfidUid:
        (stat, tag_type) = rfidModule.request(rfidModule.REQIDL)
            
        if stat == rfidModule.OK:
            (stat, raw_uid) = rfidModule.anticoll()
            cardUid = raw_uid[0] + raw_uid[1] + raw_uid[2] + raw_uid[3]
            """ DEBUG
            print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            print('')
            print(cardUid)
            """

        if passedTime + 5 < time.monotonic():
            defineTempHum()
            passedTime = time.monotonic()

    return state_2()



def state_2():
    pixelLed.fill(COLORS['yellow'])
    textArea.scale = 2
    textArea.text =  "Entrez code\ndestination"
    keypadString = ""
    lcdPassedTime = time.monotonic()
    passedTime = time.monotonic()
    global currentDestination

    while currentDestination == "":
        if lcdPassedTime + 0.1 < time.monotonic():
            textArea.text =  "Entrez code\ndestination \n" + keypadString
            lcdPassedTime = time.monotonic()
        
        ### DEBUG ### PERMET DE SIMULER UN CLAVIER
        """
        charInput = input()

        if charInput == "#" and len(keypadString) == 3:
            if keypadString in AIRPORTS :
                currentDestination = AIRPORTS[keypadString]
            else :
                textArea.text = "Veuillez entrer\nun code valide !"
                keypadString = ""
                charInput = ""
                time.sleep(2)

        elif charInput == "#" and len(keypadString) == 0:
            return state_1()

        elif charInput == "#" and len(keypadString) != 3:
            textArea.text = "Veuillez entrer\nun code valide !"
            charInput = ""
            time.sleep(2)

        elif len(keypadString) >= 3:
            textArea.text = "Veuillez entrer\nun code valide\nde 3 caractères !"
            keypadString = ""
            charInput = ""
            time.sleep(2)

        keypadString += charInput
        """

        if tca.key_int:
            events = tca.events_count

            for _ in range(events):
                keyevent = tca.next_event
                #  strip keyevent
                event = keyevent & 0x7F
                event -= 1
                row = event // 10
                col = event % 10

                if keyevent & 0x80:
                    if KEYPAD[col][row] == "#" and len(keypadString) == 3:
                        if keypadString in AIRPORTS :
                            currentDestination = AIRPORTS[keypadString]

                    elif KEYPAD[col][row] == "#" and len(keypadString) == 0:
                        return state_1()

                    elif KEYPAD[col][row] == "#" and len(keypadString) != 3:
                        textArea.text = "Veuillez entrer un code valide !"
                        keypadString = ""
                        time.sleep(2)

                    elif len(keypadString) > 3:
                        textArea.text = "Veuillez entrer un code \n valide de 3 caractères !"
                        keypadString = ""
                        time.sleep(2)
                    else:
                        keypadString += KEYPAD[col][row]

            tca.key_int = True  
        
    textArea.text =  currentDestination + "\nAttend PWR ON"

    if passedTime + 5 < time.monotonic():
        defineTempHum()
        passedTime = time.monotonic()

    while True:
        if pwrButton.value :
            return state_3()

def state_3():

    textArea.scale = 1
    enableMotor.value = True
    pixelLed.fill(COLORS['green'])
    isFlightSettingsLocked = False
    motor.throttle = 0
    fin.angle = 90
    tempCelcius = 0
    humidity = 0
    lcdPassedTime = time.monotonic()
    passedTime = time.monotonic()
    ledIndex = 0
    global currentDestination

    while pwrButton.value :

        if distanceSonar.distance < 10:
            return state_1()

        if not joystickButton.value :
            if isFlightSettingsLocked :
                isFlightSettingsLocked = False
            else :
                isFlightSettingsLocked = True

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
            if (axisXVal < 0.26 and axisXVal > 0.24) and (axisYVal < 0.14 and axisYVal > 0.11):
                joystickAngle = -1

            ledIndex = selectLedRingIndex(joystickAngle)

            ledBoard.fill(COLORS['off'])
            if ledIndex != -1:
                ledBoard[ledIndex] = COLORS['white']

        #Empèche le plantage du esp si spike de courant pour DHT
        try :
            tempCelcius = dht.temperature
            humidity = dht.humidity
            motorPower = motor.throttle * 100

        except RuntimeError as error:
            print(error.args[0])
            continue
    
        if lcdPassedTime + 0.1 < time.monotonic():
            textArea.text = "Puissance moteur : " + str(int(motorPower)) + " %\n" + "Angle aileron : " + str(int(finAngle)) + " deg\n" + "Destination : " + str(currentDestination) + "\n" + "Température : " + str(tempCelcius) + " C\n" + "Humidité : " + str(humidity) + " %\n" + "Autopilote : " + str(isFlightSettingsLocked) +  " %\n" + "Distance : " + str(distanceSonar.distance)
            lcdPassedTime = time.monotonic()

        if passedTime + 5 < time.monotonic():
            sendData(tempCelcius, humidity)
            passedTime = time.monotonic()


    currentDestination = ""
    return state_1()

def main():

    while True:
        current_state = state_1()

        # Sortie de la boucle si l'état final est atteint
        if current_state == None:
            break

main()