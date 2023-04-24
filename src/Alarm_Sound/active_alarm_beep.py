import time
from time import sleep

from matrix_lite import gpio

class ActiveBuzzerUserInterrupt(Exception):
    def __init__(self):
        self.message = 'Active Buzzer was stopped by the user.'

# Inverted Signal due to transistor
# OFF - will cause a beep
# ON  - will cause silence
class ActiveAlarmBeep:
    def __init__(self, buzzer_pin):
        self._buzzer_pin = buzzer_pin
        self._stop_flag = False
        self.setup()
        
    def setup(self):
        gpio.setFunction(self._buzzer_pin, 'DIGITAL')
        gpio.setMode(self._buzzer_pin, 'output')
        gpio.setDigital(self._buzzer_pin, "ON")	

    def set_stop_flag(self):
        self._stop_flag = True
        self.close()
    
    def close(self):
        gpio.setDigital(self._buzzer_pin, "ON")	
    
    def play(self, delay, repeat):
        for i in range(repeat):
            if self._stop_flag:
                raise ActiveBuzzerUserInterrupt()
            gpio.setDigital(self._buzzer_pin, 'OFF')
            time.sleep(delay)
            gpio.setDigital(self._buzzer_pin, 'ON')
            time.sleep(delay)
