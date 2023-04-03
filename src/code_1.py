import board
import keypad
import pwmio
import time
import neopixel
import adafruit_hcsr04
import adafruit_dht
import terminalio
import analogio
import digitalio
from adafruit_motor import servo
from adafruit_hid.keycode import Keycode
from adafruit_display_text import bitmap_label
from displayio import Group

#Screen
scale = 2
textArea = bitmap_label.Label(terminalio.FONT, scale = scale)
textArea.anchor_point = (0.5, 0.5)
textArea.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
textGroup = Group()
textGroup.append(textArea)
board.DISPLAY.show(textGroup)

#DHT
dht = adafruit_dht.DHT11(board.TX)

#Servomotor
pwm = pwmio.PWMOut(board.RX, duty_cycle=2 ** 15, frequency=50)
servoMotor = servo.Servo(pwm, min_pulse=500, max_pulse=2300)

#Sonar
distanceSonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D9, echo_pin=board.D6)

#PixelLed Module
pixelLed = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixelLed.brightness = 1
colors = {'rouge':(255, 0, 0), 'jaune':(255, 255, 0), 'vert':(0, 255, 0)}

def starting_state():

    #RFID

    #FAIRE LE CHECK LORSQUE RFID FONCTIONNEL
    while True:
        if evenement_externe_1():
            # Transition vers l'état 1
            return etat_1()
        
        elif evenement_externe_2():
            # Transition vers l'état 2
            return etat_2()
        else:

            # Attente d'un événement externe
            attendre_evenement()


def state_1():
    pixelLed.fill(colors['rouge'])
    textArea.text = "Scannez carte"

    # Actions à effectuer lors de l'entrée dans l'état 1
    while True:
        if evenement_externe_3():
            # Transition vers l'état final
            return etat_final()
        else:
            # Attente d'un événement externe
            attendre_evenement()

def etat_2():
    pixelLed.fill(colors['jaune'])
    textArea.text = "Afficher sur LCD : \n Entrez code destination sur ligne 1"
    # Actions à effectuer lors de l'entrée dans l'état 2
    while True:
        if evenement_externe_4():
            # Transition vers l'état final
            return etat_final()
        else:
            # Attente d'un événement externe
            attendre_evenement()

def etat_final():
    # Actions à effectuer lors de l'entrée dans l'état final
    return

def main():
    # Initialisation de la machine à états finis
    etat_courant = starting_state()

    while True:
        # Exécution de l'état courant
        etat_courant = starting_state()

        # Sortie de la boucle si l'état final est atteint
        if etat_courant == None:
            break

main()