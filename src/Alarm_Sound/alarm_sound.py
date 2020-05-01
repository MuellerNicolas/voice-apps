import logging
import threading
from time import sleep

from matrix_lite import gpio

from Alarm_Sound.alarm_song import BuzzerSong
from Logger.logger_init import get_logger


class AlarmSound:
	def __init__(self, broker, PIN_SONG, PIN_BEEP):
		self.broker = broker
		broker.subscribe("alarm-beep", self._beep)
		# stop the alarm on analog button press
		broker.subscribe("alarm-button-stop", self._stopAlarm)
		broker.subscribe("alarm-snooze", self._stopAlarm)
		# stop the alarm if a wakeword was detected or the wakeword is starting to listen
		broker.subscribe("wakeword-status", self._stopAlarm)
		# select the song for the passive buzzer
		broker.subscribe("alarm-song-selected", self._select_alarm_song_cb)
		self._thread_buzzer_flag = None
		# flag to stop the sound
		self._continue_beep = True
		# flag for timeout if the buzzer is already active
		self._last_minute_active = False
		# Pin Belegung
		# Passive buzzer
		self._PIN_SONG = PIN_SONG
		# Active Buzzer
		self._PIN_BEEP = PIN_BEEP
		# Passives Buzzer Objekt
		self._passive_buzzer = None
		# Default: no Song
		self._selected_song = 'Aus'

	def _run(self):
		self._thread_buzzer_flag = threading.Event()
		self._thread_buzzer = threading.Thread(
			target=self._melody, name='voice-app-alarm-sound-thread', daemon=True)
		self._thread_buzzer.start()

	def close(self):
		if self._thread_buzzer_flag != None:
			self._thread_buzzer_flag.set()
		self._continue_beep = False
		# Make sure there is no power on the pin after closing
		gpio.setDigital(self._PIN_BEEP, 'OFF')
		gpio.setDigital(self._PIN_SONG, 'OFF')

	def _select_alarm_song_cb(self, *args, **kwargs):
		self._selected_song = args

	def _melody(self):
		# First try for the not so important song
		try:
			# quiet song
			self._passive_buzzer = BuzzerSong(self._PIN_SONG)
			self._passive_buzzer.setup()
			# start the selected song
			self._passive_buzzer.select_song(self._selected_song)
			get_logger(__name__).info(f'Passive Buzzer alarm was successful')
		except:
			get_logger(__name__).error(f'Critical error in _melody @ passiv buzzer')
			logging.exception('Critical error in _melody @ passiv buzzer')
		finally:
			gpio.setDigital(self._PIN_SONG, 'OFF')

		# Second try in case the passive buzzer fails
		try:
			# loud beeping
			gpio.setFunction(self._PIN_BEEP, 'DIGITAL')
			gpio.setMode(self._PIN_BEEP, 'output')
			while self._continue_beep:
				gpio.setDigital(self._PIN_BEEP, 'ON')
				sleep(1)
				gpio.setDigital(self._PIN_BEEP, 'OFF')
				sleep(1)
			get_logger(__name__).info(f'Active Buzzer alarm was successful')
		except:
			get_logger(__name__).error(f'Critical error in _melody @ activ buzzer')
			logging.exception('Critical error in _melody @ activ buzzer')
		finally:
			# Reset the beep flag
			self._continue_beep = True
			gpio.setDigital(self._PIN_BEEP, 'OFF')
			gpio.setDigital(self._PIN_SONG, 'OFF')

	def _beep(self, *args, **kwargs):
		if(self._last_minute_active == False):
			# start beeping
			self._run()
			self._last_minute_active = True
			"""stop any request to start beeping for the next minute
			   this is because the time keeper would send the whole 
			   minute in 15 second intervals new command
			"""
			try:
				sleep(60)
			except:
				get_logger(__name__).warning(f'Interrupted debouncing of the buzzer')
			finally:
				self._last_minute_active = False

	def _stopAlarm(self, *args, **kwargs):
		# interrupt the melody
		try:
			self._passive_buzzer.set_stop_flag()
		except:
			pass
		# set all pins to low
		self.close()
