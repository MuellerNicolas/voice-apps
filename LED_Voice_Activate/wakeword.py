from matrix_lite import led
from time import sleep
from math import trunc

class LEDClock:
    def __init__(self, broker):
        self._broker = broker
        self._broker.subscribe('wakeword-start', self._set_lightring)
        self._broker.subscribe('wakeword-stop', self._set_lightring)

    def _set_lightring(self, payload):
        if(payload == 'loaded'):
            color = 'blue'
        else:
            color = 'black'

        everloop = ['black'] * led.length
    
        ledLength = led.length

        for i in range(trunc(ledLength/2)):
            everloop[i] = color
            led.set(everloop)
            everloop[ledLength-1-i] = color
            led.set(everloop)
            sleep(.025)