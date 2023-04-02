import time
import board
import neopixel
import adafruit_hcsr04
import terminalio
from adafruit_display_text import bitmap_label
from displayio import Group

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D6, echo_pin=board.D5)
pixelLed = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixelLed.brightness = 1

couleurs = {'rouge':(255, 0, 0), 'jaune':(255, 255, 0), 'vert':(0, 255, 0)}

##écran
scale = 2
textArea = bitmap_label.Label(terminalio.FONT, scale = scale)
textArea.anchor_point = (0.5, 0.5)
textArea.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
textGroup = Group()
textGroup.append(textArea)
board.DISPLAY.show(textGroup)

while True:
    try:
        if sonar.distance > 15:
            pixelLed.fill(couleurs['vert'])
        elif sonar.distance >= 5:
            pixelLed.fill(couleurs['jaune'])
        else:
            pixelLed.fill(couleurs['rouge'])

        textArea.text = "Distance : " + str(sonar.distance)
        
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.5)