class AlarmSound:
    def __init__(self, broker):
        self.broker = broker
        broker.subscribe("alarm-beep", self._beep)
        broker.subscribe("alarm-stop", self._stopAlarm)
        broker.subscribe("alarm-snooze", self._stopAlarm)

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