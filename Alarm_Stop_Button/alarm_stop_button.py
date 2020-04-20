from Alarm_Stop_Button.alarm_stop_button_interface import AlarmStopButtonInterface
from matrix_lite import gpio
from time import sleep

class AlarmStopButton(AlarmStopButtonInterface):
    def __init__(self, PIN):
        self.PIN = PIN
        gpio.setFunction(self.PIN, 'DIGITAL')
        gpio.setMode(self.PIN, 'input')
    def close(self):
        pass
    def _triggered(self):
        pass
    def check_press(self):
        try:
            while True:
                if (gpio.getDigital(self.PIN)) == 1:
                    print("TRUE")
                else:
                    print("FALSE")
        except:
            pass



