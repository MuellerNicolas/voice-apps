from Alarm_Switch_Button.alarm_switch_button import AlarmSwitchButtonInterface
from matrix_lite import gpio
from time import sleep
import threading
import traceback

class AlarmSwitchButton(AlarmSwitchButtonInterface):
    def __init__(self, broker, PIN, POLLING):
        self._broker = broker

        self._PIN = PIN
        self._POLLING = POLLING
        # setup matrix voice pins
        gpio.setFunction(self._PIN, 'DIGITAL')
        gpio.setMode(self._PIN, 'input')
        #thread for polling to press events on the button
        self._thread_button_flag = threading.Event()
        self._thread_button = threading.Thread(target= self._check_pressed, name = 'voice-app-alarm-switch-button', daemon = True)
        self._thread_button.start()

    def close(self):
        self._thread_button_flag.set()

    def _triggered(self):
        # notify all interested compontents about the event
        self._broker.publish('alarm-button-switch', 'pressed')

    def _check_pressed(self):
        try:
            while True:
                sleep(self._POLLING)
                if (gpio.getDigital(self._PIN)) == 1:
                    # notify all interested compontents about the event
                    self._triggered()                    
                    # debouncetime - 1 second: ignore any buttonpress within the next second
                    sleep(1)
        except:
            traceback.print_exc()

