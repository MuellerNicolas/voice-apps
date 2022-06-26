import threading

from time import sleep

from matrix_lite import gpio

from Alarm_Buttons.alarm_stop_button_interface import \
    AlarmStopButtonInterface
from Logger.logger_init import get_logger


class AlarmStopButton(AlarmStopButtonInterface):
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
            target=self._check_pressed, name='voice-app-alarm-stop-button', daemon=True)
        self._thread_button.start()

    def close(self):
        self._thread_button_flag.set()

    def _triggered(self):
        get_logger(__name__).info(f'alarm-button-stop fired!')
        # notify all interested compontents about the event
        self._broker.publish('alarm-button-stop', 'pressed')

    def _check_pressed(self):
        try:
            while True:
                sleep(self._POLLING)
                if (gpio.getDigital(self._PIN)) == 1:
                    # accept only a long press (prevent noisy signals from the buzzer due to the magnetic field)
                    sleep(1)
                    if (gpio.getDigital(self._PIN)) == 1:
                        # notify all interested compontents about the event
                        self._triggered()
                        # debouncetime - 1 second: ignore any buttonpress within the next second
                        sleep(1)
        except:
            get_logger(__name__).error(f'Error in Thread Stop Button')
