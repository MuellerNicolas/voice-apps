from time import sleep
from datetime import datetime
import threading
from threading import Lock
import traceback

class AlarmTimeKeeper:
    def __init__(self, broker):
        # Broker
        self._broker = broker
        self._broker.subscribe('alarm-info' , self._receive_alarm_info_callback)

        # alarm info dictionary
        self._alarm_info = None
        
        # Thread
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(target= self._time_polling, name = 'Time-Keeper-Thread', daemon = True)
        self._thread.start()

    def close(self):
        self._thread_flag.clear()

    def _time_polling(self):
        try:
            while True:
                hour = datetime.now().hour
                minute = datetime.now().minute
                if(self._alarm_info == None):
                    # if no infos received wake me up at 6:00 am
                    if(hour == 6 and minute == 0):
                        self._alarmClockWakeup()
                elif(self._alarm_info["state"] == "on"):
                    if(hour == self._alarm_info["hour"] and minute == self._alarm_info["minute"]):
                        self._alarmClockWakeup()
                # Polling rate
                sleep(15)
        except:
            traceback.print_exc()
            # if any error occurs try to wake me up
            self._broker.publish("alarm-beep")

    def _receive_alarm_info_callback(self, alarm_info):
        self._alarm_info = alarm_info

    def _alarmClockWakeup(self):
        self._broker.publish("alarm-beep")