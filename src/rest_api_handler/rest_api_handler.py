import json
import logging
import os
import threading
from time import sleep

from logger.logger_init import get_logger
from requests import get, post


class RESTApiHandler:
    def __init__(self, broker):
        """ 
            !!!ATTENTION!!!
            Adapt example_for_home_assistant_rest_athorization.json with
            your specific authorization aswell as your specific entities
            and replace the filename below
        """
        # get the home assistant authorization key
        path = os.path.join(os.path.dirname(__file__),
                            'Home_Assistant_Authorization.json')
        with open(path) as f:
            home_assistant = json.load(f)
        self._headers = {
            "Authorization": home_assistant['authorization'],
            "content-type": "application/json"
        }
        self._urls = {
            "url_is_workday": home_assistant['url_is_workday'],
            "url_time_workday": home_assistant['url_time_workday'],
            "url_time_weekend": home_assistant['url_time_weekend'],
            "url_state_workday": home_assistant['url_state_workday'],
            "url_state_weekend": home_assistant['url_state_weekend'],
            "url_song_workday": home_assistant['url_song_workday'],
            "url_song_weekend": home_assistant['url_song_weekend']
        }
        # Broker
        self._broker = broker
        self._broker.subscribe("alarm-request-info",
                               self._initiate_request_callback)

        # Thread
        self._threadActive = False
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(
            target=self._http_polling, name='REST-API-Thread', daemon=True)

    def close(self):
        self._thread_flag.set()

    def _http_polling(self):
        try:
            # prevent exceeding requests at startup
            sleep(10)
            while True:
                get_logger(__name__).info(f'http api try')
                
                is_workday = self._get_is_workday()
                
                if(is_workday):
                    get_logger(__name__).info(f'today is a workday')
                    time = self._get_alarm_time_workday()
                    state = self._get_alarm_state_workday()
                    song = self._get_alarm_song_workday()
                else:
                    get_logger(__name__).info(f'today is a weekend day')
                    time = self._get_alarm_time_weekend()
                    state = self._get_alarm_state_weekend()
                    song = self._get_alarm_song_weekend()
                
                # Don't check if song request was successful,
                # because the alarm will work without it
                # Check if the request was successful
                if(time.status_code != 200 or state.status_code != 200):
                    get_logger(__name__).warn(
                        f'GET Request failed with code {time.status_code}!')
                    # Not successful, go on threading
                    self._thread_flag.set()
                else:
                    # Successful
                    alarm_info = self._format_alarm_info(time, state)
                    # Send the alarm_info to all subscribers
                    self._broker.publish('alarm-info', alarm_info)
                    # Send the selected song, if the request was successful
                    if(song.status_code == 200):
                        alarm_song = self._format_alarm_song(song)
                        self._broker.publish('alarm-song-selected', alarm_song)
                    get_logger(__name__).info(
                        f'Successfully received alarm_info={alarm_info}, alarm_song={alarm_song}')
                    # Request was successful, stop the thread
                    return
                sleep(10)
                self._thread_flag.wait()
        except:
            get_logger(__name__).error(f'Error in Api Handler')
            logging.exception("Error info:")
        finally:
            self.close()
            self._threadActive = False

    def _get_is_workday(self):
        return get(self._urls["url_is_workday"], headers=self._headers)
    
    def _get_alarm_time_workday(self):
        return get(self._urls["url_time_workday"], headers=self._headers)

    def _get_alarm_state_workday(self):
        return get(self._urls["url_state_workday"], headers=self._headers)

    def _get_alarm_song_workday(self):
        return get(self._urls["url_song_workday"], headers=self._headers)

    def _get_alarm_time_weekend(self):
        return get(self._urls["url_time_weekend"], headers=self._headers)

    def _get_alarm_state_weekend(self):
        return get(self._urls["url_state_weekend"], headers=self._headers)

    def _get_alarm_song_weekend(self):
        return get(self._urls["url_song_weekend"], headers=self._headers)

    def _format_alarm_song(self, song):
        song = song.json()
        return song["state"]

    def _format_alarm_info(self, time, state):
        alarm_info = {}
        # Convert the responses text to string and deserialize the json
        time = time.json()
        alarm_info["hour"] = time["attributes"]["hour"]
        alarm_info["minute"] = time["attributes"]["minute"]
        alarm_info["second"] = time["attributes"]["second"]
        # Convert the responses text to string and deserialize the json
        state = state.json()
        alarm_info["state"] = state["state"]
        return alarm_info

    def _initiate_request_callback(self):
        if(self._threadActive):
            self._thread_flag.set()
            get_logger(__name__).info(f'Initiate thread active')
        else:
            self._thread_flag = threading.Event()
            self._thread = threading.Thread(
                target=self._http_polling, name='REST-API-Thread', daemon=True)
            self._thread.start()
            self._threadActive = True
            get_logger(__name__).info(f'Initiate thread inactive')
