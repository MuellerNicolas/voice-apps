from matrix_lite import led
from time import sleep
from math import trunc

class Wakeword:
    def __init__(self, broker):
        self._broker = broker
        # flag which is true, when the clock for example is displaying the time
        self._led_in_use = False
        self._broker.subscribe('wakeword-status', self._detect_status_cb)
        self._broker.subscribe('clock-time', self._led_in_use_cb)

    def close(self):
        led.set("black")

    def _detect_status_cb(self, payload):
        # led busy
        if(not self._led_in_use):
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

    # Prevents that the wakeword LED is cancelling the clock
    def _led_in_use_cb(self, status):
        if(status == 'start'):
            self._led_in_use = True
        elif(status == 'stop'):
            self._led_in_use = False