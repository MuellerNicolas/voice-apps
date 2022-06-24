import time
from time import sleep

from matrix_lite import gpio

triggerPIN = 4

def setup():
    gpio.setFunction(triggerPIN, 'DIGITAL')
    gpio.setMode(triggerPIN, 'output')

def play(delay, repeat):
     # start a loop from 0 to the variable "cycles" calculated above
    for i in range(repeat):
        gpio.setDigital(triggerPIN, 'ON')  # set buzzer_pin to high
        time.sleep(delay)  # wait with buzzer_pin high
        gpio.setDigital(triggerPIN, 'OFF')  # set buzzer_pin to low
        time.sleep(delay)  # wait with buzzer_pin low


if __name__ == "__main__":
    try:
        setup()
        play(1, 10)
    finally:
        gpio.setDigital(triggerPIN, 'OFF')

    