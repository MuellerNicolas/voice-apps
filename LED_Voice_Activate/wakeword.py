from matrix_lite import led
from time import sleep
from math import trunc

class LEDClock:
    def __init__(self, broker):
        self._broker = broker
        self._broker.subscribe('wakeword-status', self._set_lightring)

    def close(self):
        led.set("black")

    def _detect_status(self, payload):
        print(payload)
        if(payload == 'loaded'):
            color = 'blue'
            self._set_lightring(color)
        elif(payload == 'listening'):
            color = 'black'
            self._set_lightring(color)

    def _set_lightring(self, color):
        everloop = ['black'] * led.length
    
        ledLength = led.length

        for i in range(trunc(ledLength/2)):
            everloop[i] = color
            led.set(everloop)
            everloop[ledLength-1-i] = color
            led.set(everloop)
            sleep(.025)
