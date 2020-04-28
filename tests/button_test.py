from matrix_lite import gpio
from time import sleep


PIN_1 = 1
PIN_2 = 3
gpio.setFunction(PIN_1, 'DIGITAL')
gpio.setMode(PIN_1, 'input')

gpio.setFunction(PIN_2, 'DIGITAL')
gpio.setMode(PIN_2, 'input')



while True:
    if (gpio.getDigital(PIN_1) == 1 and gpio.getDigital(PIN_2) == 1):
        print("Alllllleee")
    elif gpio.getDigital(PIN_1) == 1:
        print("EINS")
    elif gpio.getDigital(PIN_2) == 1:
        print("2")


