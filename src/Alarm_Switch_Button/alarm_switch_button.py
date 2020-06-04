import threading
from time import sleep

from matrix_lite import gpio

from Alarm_Switch_Button.alarm_switch_button_interface import \
    AlarmSwitchButtonInterface
from Logger.logger_init import get_logger


class AlarmSwitchButton(AlarmSwitchButtonInterface):
    def __init__(self, broker, PIN, POLLING):
        self._broker = broker

        self._PIN = PIN
        self._POLLING = POLLING
        # setup matrix voice pins
        gpio.setFunction(self._PIN, 'DIGITAL')
        gpio.setMode(self._PIN, 'input')
        # thread for polling to press events on the button
        self._thread_button_flag = threading.Event()
        self._thread_button = threading.Thread(
            target=self._check_pressed, name='voice-app-alarm-switch-button', daemon=True)
        self._thread_button.start()

    def close(self):
        self._thread_button_flag.set()

    def _triggered(self):
        # notify all interested compontents about the event
        self._broker.publish('alarm-button-switch', 'pressed')
        get_logger(__name__).info(f'Toggle alarm state')

    def _check_pressed(self):
        try:
            while True:
                sleep(self._POLLING)
                if (gpio.getDigital(self._PIN)) == 1:
                    # notify all interested compontents about the event
                    self._triggered()
                    # debouncetime - 4 second: ignore any buttonpress within the next second
                    # set to 4 seconds, because the leds will last 4 seconds
                    # otherwise multiple presses after one another will cause a strange
                    # led effect
                    sleep(4)
        except:
            get_logger(__name__).error(f'Error in Thread Stop Button')
