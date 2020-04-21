from time import sleep
from datetime import datetime
import threading
from threading import Lock

class AlarmTimeKeeper:
    def __init__(self, broker):
        # Broker
        self._broker = broker
        self._broker.subscribe('alarm-info' , self._receive_alarm_info_callback)

        # alarm info dictionary
        self._alarm_info = None
        

    def close(self):
        pass

    def _time_polling(self):
        hour = datetime.now().hour
        minute = datetime.now().minute

    def _receive_alarm_info_callback(self, alarm_info):
        self._alarm_info = alarm_info
        print(self._alarm_info)

    def _alarmClockWakeup(self):
        pass