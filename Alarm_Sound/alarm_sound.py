import threading
from matrix_lite import gpio
from time import sleep
import traceback

class AlarmSound:
    def __init__(self, broker, PIN):
        self.broker = broker
        broker.subscribe("alarm-beep", self._beep)
        broker.subscribe("alarm-button-stop", self._stopAlarm)
        broker.subscribe("alarm-snooze", self._stopAlarm)
        self._thread_buzzer_flag = None
        # flag to stop the sound
        self._continue_beep = True
        # flag for timeout if the buzzer is already active
        self._buzzer_active = False
        self._PIN = PIN
    def _run(self):
        self._thread_buzzer_flag = threading.Event()
        self._thread_buzzer = threading.Thread(target= self._melody, name = 'voice-app-alarm-sound-thread', daemon = True)
        self._thread_buzzer.start()

    def close(self):
        if self._thread_buzzer_flag != None:
            self._thread_buzzer_flag.set()
        self._continue_beep = False
        # Make sure there is no power on the pin after closing
        gpio.setDigital(self._PIN, 'OFF')

    def _melody(self):
        if(self._buzzer_active == False):
            try:
                self._buzzer_active = True
                gpio.setFunction(self._PIN, 'DIGITAL')
                gpio.setMode(self._PIN, 'output')
                while self._continue_beep:
                    gpio.setDigital(self._PIN, 'ON')
                    sleep(1)
                    gpio.setDigital(self._PIN, 'OFF')
                    sleep(1)
            except:
                traceback.print_exc()
            finally:
                # Reset the beep / buzzer flag
                self._continue_beep = True
                self._buzzer_active = False
                gpio.setDigital(self._PIN, 'OFF')

    def _beep(self):
        self._run()


    def _stopAlarm(self, *args, **kwargs):
        self.close()