import threading
from datetime import datetime
from time import sleep

from logger.logger_init import get_logger


class AlarmTimeKeeper:
    def __init__(self, broker):
        # Broker
        self._broker = broker
        self._broker.subscribe('alarm-info', self._receive_alarm_info_callback)

        # alarm info dictionary
        self._alarm_info = None

        # Thread
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(
            target=self._time_polling, name='Time-Keeper-Thread', daemon=True)
        self._thread.start()

    def close(self):
        self._thread_flag.clear()

    def _time_polling(self):
        get_logger(__name__).info(f'start thread time polling')
        try:
            while True:
                hour = datetime.now().hour
                minute = datetime.now().minute
                if(self._alarm_info == None):
                    get_logger(__name__).warn(f'No alarm infos received yet')
                    # if alarm infos were not received via mqtt, try get it via http
                    #self._initiateApiGet()
                    # if no infos received wake me up at 6:00 am
                    if(hour == 6 and minute == 0):
                        get_logger(__name__).warn(f'Wake up at 6:00 am. Current alarm_info={self._alarm_info}')
                        self._alarmClockWakeup()
                elif(self._alarm_info["state"] == "on"):
                    if(hour == self._alarm_info["hour"] and minute == self._alarm_info["minute"]):
                        self._alarmClockWakeup()
                # Polling rate
                sleep(15)
        except:
            get_logger(__name__).error(f'Error while time polling')
        finally:
            # if any error occurs try to wake me up
            # has to wait 10 sec, cuz the alarm_sound has to be initialized
            sleep(10)
            get_logger(__name__).error(f'Waking you up now, as an error occured in _time_polling')
            self._alarmClockWakeup()

    def _receive_alarm_info_callback(self, alarm_info):
        get_logger(__name__).info(f'received alarm_info={alarm_info}')
        self._alarm_info = alarm_info

    def _alarmClockWakeup(self):
        self._broker.publish("alarm-beep")

    def _initiateApiGet(self):
        self._broker.publish("alarm-request-info")
