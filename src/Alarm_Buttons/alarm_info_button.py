import threading
from time import sleep, time

from matrix_lite import gpio

from Logger.logger_init import get_logger


class AlarmInfoButton:
    def __init__(self, broker, PIN, POLLING):
        self._broker = broker

        self._broker.subscribe('alarm-info', self._alarm_info_received)
        self._broker.subscribe('trigger-button-alarm-info', self._triggered_button_alarm_info)
        self.alarm_info_received = False
        
        self._PIN = PIN
        self._POLLING = POLLING
        # setup matrix voice pins
        gpio.setFunction(self._PIN, 'DIGITAL')
        gpio.setMode(self._PIN, 'input')
        # thread for polling to press events on the button
        self._thread_button_flag = threading.Event()
        self._thread_button = threading.Thread(
            target=self._check_pressed, name='alarm-info-button', daemon=True)
        self._thread_button.start()

    def _alarm_info_received(self, alarm_info):
        self.alarm_info_received = True
            
    def _triggered_button_alarm_info(self, *args, **kwargs):
        self._triggered()
        # sleep(6)
        if(self.alarm_info_received):
            self._broker.publish('alarm-button-info', 'pressed')
            self.alarm_info_received = False

    def close(self):
        self._thread_button_flag.set()

    def _triggered(self):
        get_logger(__name__).info(f'Get info about alarm')
        self._broker.publish('alarm-request-info')
        timestamp = time()
        while (not self.alarm_info_received and time() - timestamp < 30):
            sleep(0.250)


    def _check_pressed(self):
        try:
            while True:
                sleep(self._POLLING)
                if (gpio.getDigital(self._PIN)) == 1:
                    self._triggered()                    
                    # debouncetime - 15 second: ignore any buttonpress within the next second
                    # notify all interested compontents about the event
                    # set to 15 seconds, because the leds will last 15 seconds
                    # otherwise multiple presses after one another will cause a strange
                    # led effect
                    if(self.alarm_info_received):
                        self._broker.publish('alarm-button-info', 'pressed')
                        self.alarm_info_received = False
                    sleep(15)

        except:
            get_logger(__name__).error(f'Error in Thread Info Button')
        finally:
            self.alarm_info_received = False
            self.close()
            
