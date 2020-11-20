from matrix_lite import led
from time import sleep
from math import pi, sin
from time import time

class LEDOthers:
    def __init__(self, broker):
        # add broker
        self._broker = broker
        self._broker.subscribe('led-on', self._led_light)
        self._broker.subscribe('led-rainbow', self._led_rainbow)
        self._broker.subscribe('led-off', self.close)
    
    def close(self):
        led.set('black')
    
    def _led_light(self):
        try:
            sleep(3)
            led.set('white')
            sleep(5)
            led.set('white')
            sleep(180)
        finally:
            led.set('black')

    def _led_rainbow(self):
        try:
            sleep(3)
            # Turn on the rainbow for 15 seconds
            t_end = time() + 15
            
            everloop = ['black'] * led.length

            ledAdjust = 0.0
            if len(everloop) == 35:
                ledAdjust = 0.51 # MATRIX Creator
            else:
                ledAdjust = 1.01 # MATRIX Voice

            frequency = 0.375
            counter = 0.0
            tick = len(everloop) - 1

            while time() < t_end:
                # Create rainbow
                for i in range(len(everloop)):
                    r = round(max(0, (sin(frequency*counter+(pi/180*240))*155+100)/10))
                    g = round(max(0, (sin(frequency*counter+(pi/180*120))*155+100)/10))
                    b = round(max(0, (sin(frequency*counter)*155+100)/10))

                    counter += ledAdjust

                    everloop[i] = {'r':r, 'g':g, 'b':b}

                # Slowly show rainbow
                if tick != 0:
                    for i in reversed(range(tick)):
                        everloop[i] = {}
                    tick -= 1

                led.set(everloop)

                sleep(.035)
        finally:
            led.set('black')