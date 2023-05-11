import logging
import threading
from time import sleep

from matrix_lite import gpio

from Alarm_Sound.active_alarm_beep import ActiveAlarmBeep, ActiveBuzzerUserInterrupt
from Alarm_Sound.alarm_song import BuzzerSong, PassiveBuzzerUserInterrupt

from Logger.logger_init import get_logger
import inspect


class AlarmSound:
    def __init__(self, broker, PIN_SONG, PIN_BEEP):
        self._broker = broker
        self._broker.subscribe("alarm-beep", self._beep)
        # stop the alarm on analog button press
        self._broker.subscribe("alarm-button-stop", self._stopAlarm)
        self._broker.subscribe("alarm-snooze", self._stopAlarm)
        # stop the alarm if a wakeword was detected or the wakeword is starting to listen
        self._broker.subscribe("wakeword-status", self._stopAlarm)
        # select the song for the passive buzzer
        self._broker.subscribe("alarm-song-selected",
                               self._select_alarm_song_cb)
        self._thread_buzzer_flag = None
        # flag for timeout if the buzzer is already active
        self._last_minute_active = False
        # Pin Belegung
        # Passive buzzer
        self._PIN_SONG = PIN_SONG
        # Aktiver Buzzer lautes piepen
        self._PIN_BEEP = PIN_BEEP
        # Passives Buzzer Objekt - Melodie
        self._passive_buzzer_melody = None
        # Aktives Buzzer Objekt - beep
        self._active_buzzer_beep = None
        # Default: no Song
        self._selected_song = 'Aus'
        
        self._passive_buzzer_melody = BuzzerSong(self._PIN_SONG)
        self._active_buzzer_beep = ActiveAlarmBeep(self._PIN_BEEP)

    def _run(self):
        self._thread_buzzer_flag = threading.Event()
        self._thread_buzzer = threading.Thread(
            target=self._make_sound, name='voice-app-alarm-sound-thread', daemon=True)
        self._thread_buzzer.start()

    def close(self):
        if self._thread_buzzer_flag != None:
            self._thread_buzzer_flag.set()
        # Make sure there is no power on the pin after closing
        gpio.setDigital(self._PIN_BEEP, 'ON')
        gpio.setDigital(self._PIN_SONG, 'OFF')

    def _select_alarm_song_cb(self, *args, **kwargs):
        # *args is a tuple and we only want the first element (the song)
        song = args[0]
        self._selected_song = song

    def _make_sound(self):
        try:
            # quiet song
            # start the selected song
            self._passive_buzzer_melody.select_song(self._selected_song)
            get_logger(__name__).info(f'Passive Buzzer alarm was successful')
            self._active_buzzer_beep.play(2, 90)
            get_logger(__name__).info(f'Active Buzzer BEEP LOUD alarm was successful')
        except ActiveBuzzerUserInterrupt as ActiveBuzzerException:
            get_logger(__name__).info(f'Exception in _melody: {ActiveBuzzerException.message}')
        except PassiveBuzzerUserInterrupt as PassiveBuzzerException:
            get_logger(__name__).info(f'Exception in _melody: {PassiveBuzzerException.message}')
        except Exception:
            get_logger(__name__).error(
                f'Critical error in _make_sound')
        finally:
            # Reset the beep flag
            gpio.setDigital(self._PIN_BEEP, 'ON')
            gpio.setDigital(self._PIN_SONG, 'OFF')
        # display the time
        sleep(5)
        self._broker.publish('alarm-button-stop', 'voice-triggered')

    def _beep(self, *args, **kwargs):
        if(self._last_minute_active == False):
            try:
                # start beeping
                self._run()
                self._last_minute_active = True
                """stop any request to start beeping for the next minute
                this is because the time keeper would send the whole 
                minute in 15 second intervals new command
                """
                sleep(60)
            except Exception as e:
                get_logger(__name__).warning(f'error in _beep:')
                get_logger(__name__).error(e, exc_info=True)
            finally:
                self._last_minute_active = False
                self.close()

    def _stopAlarm(self, *args, **kwargs):
        # interrupt the melody
        try:
            if(self._passive_buzzer_melody):
                self._passive_buzzer_melody.set_stop_flag()
            if(self._active_buzzer_beep):
                self._active_buzzer_beep.set_stop_flag()
        except Exception as e:
            get_logger(__name__).error(f'stop alarm could not executed properly:')
            get_logger(__name__).error(e, exc_info=True)
        finally:
            # set all pins to low
            self.close()
