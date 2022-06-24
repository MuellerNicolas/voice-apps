import time
from time import sleep

from matrix_lite import gpio

triggerPIN = 4

def setup():
    gpio.setFunction(triggerPIN, 'DIGITAL')
    gpio.setMode(triggerPIN, 'output')

def play(melody, tempo, pause, pace=0.800):
        for i in range(150):
        #for i in range(0, len(melody)):		# Play song
            # if self._stop_flag:
            #     return
            noteDuration = pace/tempo
            # Change the frequency along the song note
            buzz(melody, noteDuration)

            pauseBetweenNotes = noteDuration * pause
            time.sleep(pauseBetweenNotes)

def buzz(frequency, length):

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
        gpio.setDigital(triggerPIN, 'ON')  # set buzzer_pin to high
        time.sleep(delayValue)  # wait with buzzer_pin high
        gpio.setDigital(triggerPIN, 'OFF')  # set buzzer_pin to low
        time.sleep(delayValue)  # wait with buzzer_pin low

if __name__ == "__main__":
    try:
        setup()
        play(melody=1000, tempo=4, pause=4)
    finally:
        gpio.setDigital(triggerPIN, 'OFF')

    