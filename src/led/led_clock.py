# forked from https://github.com/MuellerNicolas/Matrix-Voice-Clock

import threading
from datetime import datetime
from math import ceil
from threading import Lock
from time import sleep

from matrix_lite import led


class LEDClock:
    def __init__(self, broker, offset, hour_color, minute_color, same_color):
        # add broker
        self._broker = broker
        self._broker.subscribe('alarm-button-stop', self._stop_button_pressed)
        self._broker.subscribe('show-time', self._show_time)
        self._broker.subscribe('alarm-switch-led', self.stop_displaying)
        self._broker.subscribe('alarm-button-info', self._display_alarm_info)
        self._broker.subscribe('alarm-info', self._receive_alarm_info_callback)

        # prevents show time called multiple times
        self._clock_active = False
        # offset depending on the rotation off the materix voice module
        self.offset = offset
        # hour leds
        self._led_array = []
        self._hours_set = False
        self.hour_color = hour_color
        self.minute_color = minute_color
        self.same_color = same_color
        # Flag set to true, to display the current time
        self._display_time = False

        # Thread
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(
            target=self._trigger_time, name='clock_thread', daemon=True)
        self._thread.start()

        # alarm info dictionary
        self._alarm_info = None

    def _stop_button_pressed(self, pressed):
        self._active_callback()

    def _show_time(self):
        self._active_callback()

    def _display_alarm_info(self, *args, **kwargs):
        if(self._alarm_info != None):
            if(self._clock_active == False):
                # display alarm time
                self._clock_active = True
                self.display_specific_time(
                    self._alarm_info["hour"], self._alarm_info["minute"])
                # time period of displaying
                sleep(10)
                self.stop_displaying()
                # display alarm status
                self._broker.publish(
                    "alarm-status-info-led", self._alarm_info["state"])
                sleep(5)
                self.stop_displaying()
                self._clock_active = False

    def _receive_alarm_info_callback(self, alarm_info):
        self._alarm_info = alarm_info

    def display_specific_time(self, hour, minute):
        self._set_all_black()
        self._set_hour(hour)
        self._hours_set = True
        self._set_minute(minute)
        # reset the led array & hours set
        self._led_array = []
        self._hours_set = False

    def _active_callback(self):
        # Make sure, that the button is not pressed multiple times and deactivates for each time
        if(self._clock_active == False):
            self._clock_active = True
            self.display_time()
            # time period of displaying
            sleep(10)
            self.stop_displaying()
            self._clock_active = False

    def close(self):
        self._thread_flag.set()
        led.set("black")

    def display_time(self):
        self._display_time = True

    def stop_displaying(self, *args, **kwargs):
        self._display_time = False
        led.set("black")

    def _trigger_time(self):
        while True:
            if(self._display_time):
                # Adapt led every minute
                self._adapt_led()
            sleep(1)

    def _adapt_led(self):
        hour = datetime.now().hour
        minute = datetime.now().minute
        self._set_all_black()
        self._set_hour(hour)
        self._hours_set = True
        self._set_minute(minute)
        # reset the led array & hours set
        self._led_array = []
        self._hours_set = False

    def _set_hour(self, hour):
        if hour > 12:
            hour = hour % 12
        self._select_meth(hour)
        led.set(self._led_array)

    def _set_minute(self, minute):
        # ceil: i want to display like 10:52 as 10:55,
        #  better be too early than to late
        minute = ceil(minute/5)
        self._select_meth(minute)
        led.set(self._led_array)

    def _select_meth(self, number):
        if(number == 0 or number == 12):
            self._twelve(self.offset)
        elif(number == 1):
            self._odd(2, self.offset)
        elif(number == 2):
            self._even(3, self.offset)
        elif(number == 3):
            self._odd(5, self.offset)
        elif(number == 4):
            self._even(6, self.offset)
        elif(number == 5):
            self._odd(8, self.offset)
        elif(number == 6):
            self._even(9, self.offset)
        elif(number == 7):
            self._odd(11, self.offset)
        elif(number == 8):
            self._even(12, self.offset)
        elif(number == 9):
            self._odd(14, self.offset)
        elif(number == 10):
            self._even(15, self.offset)
        elif(number == 11):
            self._odd(17, self.offset)

    def _set_all_black(self):
        # set all 18 LEDs to off / black
        for x in range(18):
            self._led_array.append("black")

    # Methods setting the leds
    def _odd(self, number, offset):
        if (self._hours_set):
            # -1 cuz array
            if(self._led_array[(number+offset-1) % 18] == self.hour_color):
                self._led_array[(number+offset-1) % 18] = self.same_color
            else:
                self._led_array[(number+offset-1) % 18] = self.minute_color
        else:
            self._led_array[(number+offset-1) % 18] = self.hour_color

    def _even(self, number, offset):
        if (self._hours_set):
            # -1 cuz array
            if(self._led_array[(number+offset-1) % 18] == self.hour_color):
                self._led_array[(number+offset-1) % 18] = self.same_color
                self._led_array[(number+offset) % 18] = self.same_color
            else:
                self._led_array[(number+offset-1) % 18] = self.minute_color
                self._led_array[(number+offset) % 18] = self.minute_color
        else:
            self._led_array[(number+offset-1) % 18] = self.hour_color
            self._led_array[(number+offset) % 18] = self.hour_color

    def _twelve(self, offset):
        if (self._hours_set):
            # -1 cuz array
            if(self._led_array[(18+offset-1) % 18] == self.hour_color):
                self._led_array[(18+offset-1) % 18] = self.same_color
                self._led_array[(0+offset) % 18] = self.same_color
            else:
                self._led_array[(18+offset-1) % 18] = self.minute_color
                self._led_array[(0+offset) % 18] = self.minute_color
        else:
            self._led_array[(18+offset-1) % 18] = self.hour_color
            self._led_array[(0+offset) % 18] = self.hour_color

    def set_all_colors(self, hour_color, minute_color, same_color):
        if(hour_color != minute_color and minute_color != same_color and hour_color != same_color):
            self.hour_color = hour_color
            self.minute_color = minute_color
            self.same_color = same_color
            self._adapt_led()

    def set_hour_color(self, hour_color):
        if(hour_color != self.minute_color and hour_color != self.same_color):
            self.hour_color = hour_color

    def set_minute_color(self, minute_color):
        if(minute_color != self.minute_color and minute_color != self.same_color):
            self.minute_color = minute_color

    def set_same_color(self, same_color):
        if(same_color != self.minute_color and same_color != self.hour_color):
            self.same_color = same_color
