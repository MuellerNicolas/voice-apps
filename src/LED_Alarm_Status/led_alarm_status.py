from time import sleep

from matrix_lite import led


class LEDAlarmStatus:
    def __init__(self, broker):
        # add broker
        self._broker = broker
        self._broker.subscribe('alarm-switch-led', self._show_status)

    def _show_status(self, result):
        if(result == "on"):
            self._alarm_on()
        elif(result == "off"):
            self._alarm_off()
        else:
            self._status_update_failed()

    def _alarm_on(self):
        # Alarm is no turned on
        try:
            led.set("green")
            sleep(4)
            led.set("black")
        finally:
            led.set("black")

    def _alarm_off(self):
        # Alarm is no turned off
        try:
            led.set("red")
            sleep(4)
            led.set("black")
        finally:
            led.set("black")

    def _status_update_failed(self):
        # Alarm status update failed
        try:
            for x in range(4):
                led.set("yellow")
                sleep(.5)
                led.set("black")
                sleep(.5)
        finally:
            led.set("black")
