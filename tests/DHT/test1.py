import time
import board
import terminalio
import adafruit_dht
from adafruit_display_text import bitmap_label
from displayio import Group

dht = adafruit_dht.DHT11(board.TX)
tempArray = []
humArray = []

##écran
scale = 2
textArea = bitmap_label.Label(terminalio.FONT, scale = scale)
textArea.anchor_point = (0.5, 0.5)
textArea.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
textGroup = Group()
textGroup.append(textArea)
board.DISPLAY.show(textGroup)

while True:

    currentTemp = dht.temperature
    currentHum = dht.humidity

    if len(tempArray) >= 10 and len(humArray) >= 10 :
        tempArray.pop(0)
        humArray.pop(0)

    tempArray.append(currentTemp)
    humArray.append(currentHum)

    avgTemp = sum(tempArray) / len(tempArray)
    avgHum = sum(humArray) / len(humArray)

    textArea.text = "Temperature : " + str(currentTemp) + "\n" + "Humidite : " + str(currentHum) + "\n" + "Avg Temp : " + str(avgTemp) + "\n" + "Avg Hum : " + str(avgHum)
    time.sleep(0.5)