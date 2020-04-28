#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from matrix_lite import gpio
 
BuzzPin = 4 # Raspberry Pi Pin 17-GPIO 17
 
def setup():
	gpio.setFunction(BuzzPin, 'DIGITAL')
	gpio.setMode(BuzzPin, 'output')
 
def on():
    gpio.setDigital(BuzzPin, 'ON')
 
def off():
    gpio.setDigital(BuzzPin, 'OFF')
 
def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)
 
def loop():
    while True:
        beep(0.5)
 
def destroy():
    gpio.setDigital(BuzzPin, 'OFF')
 
if __name__ == '__main__': # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
        destroy()