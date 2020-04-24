import threading

class AlarmSound:
    def __init__(self, broker):
        self.broker = broker
        broker.subscribe("alarm-beep", self._beep)
        broker.subscribe("alarm-stop", self._stopAlarm)
        broker.subscribe("alarm-snooze", self._stopAlarm)

    def _run(self):
        self._thread_button_flag = threading.Event()
        self._thread_button = threading.Thread(target= self._melody, name = 'voice-app-alarm-sound-thread', daemon = True)
        self._thread_button.start()

    def close(self):
        pass

    def _melody(self):
        pass

    def _stopAlarm(self):
        pass

    def _beep(self):
        pass

    def _stopAlarm(self):
        pass