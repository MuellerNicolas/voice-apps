import time
from time import sleep

from matrix_lite import gpio

class AlarmBeep:
    def __init__(self, buzzer_pin):
        self._buzzer_pin = buzzer_pin
        self._stop_flag = False
        self.setup()
        
    def setup(self):
        gpio.setFunction(self._buzzer_pin, 'DIGITAL')
        gpio.setMode(self._buzzer_pin, 'output')

    def set_stop_flag(self):
        self._stop_flag = True
        self.close()
    
    def close(self):
        gpio.setDigital(self._buzzer_pin, "OFF")	
    
    def play(self, melody, tempo, pause, pace=0.800):
            for i in range(200):
                if self._stop_flag:
                    return
                noteDuration = pace/tempo
                # Change the frequency along the song note
                self.buzz(melody, noteDuration)

                pauseBetweenNotes = noteDuration * pause
                time.sleep(pauseBetweenNotes)

    def buzz(self, frequency, length):

        if(frequency == 0):
            time.sleep(length)
            return
        # in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        period = 1.0 / frequency
        delayValue = period / 2  # calcuate the time for half of the wave
        # the number of waves to produce is the duration times the frequency
        numCycles = int(length * frequency)

        # start a loop from 0 to the variable "cycles" calculated above
        for i in range(numCycles):
            gpio.setDigital(self._buzzer_pin, 'ON')  # set buzzer_pin to high
            time.sleep(delayValue)  # wait with buzzer_pin high
            gpio.setDigital(self._buzzer_pin, 'OFF')  # set buzzer_pin to low
            time.sleep(delayValue)  # wait with buzzer_pin low
    