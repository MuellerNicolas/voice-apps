from matrix_lite import gpio
from time import sleep
PIN = 2

# Set GPIO pin PIN (digital)
gpio.setFunction(PIN, 'DIGITAL')
gpio.setMode(PIN, 'output')
gpio.setDigital(PIN, 'ON')
sleep(.5)
gpio.setDigital(PIN, 'OFF')


"""
# Doesn't work!
# Set GPIO pin PIN (PWM)
gpio.setFunction(PIN, 'PWM')
gpio.setMode(PIN, 'output')
gpio.setPWM({
    "pin": PIN,
    "percentage": 25,
    "frequency": 50, # min 36
})
gpio.setDigital(PIN, 'OFF')
"""