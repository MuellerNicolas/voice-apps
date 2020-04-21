from requests import get
import json
import os
import threading
import traceback
from time import sleep

class RESTApiHandler:
    def __init__(self, broker):
        self._broker = broker
        # get the home assistant authorization key
        path = os.path.join(os.path.dirname(__file__), 'Home_Assistant_Authorization.json')
        with open(path) as f:
            home_assistant = json.load(f)
        self._headers = {
            "Authorization": home_assistant['authorization'],
            "content-type": "application/json"
        }
        self._urls = {
            "url_time": home_assistant['url_time'],
            "url_state": home_assistant['url_state']
        }

        # Thread
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(target= self._http_polling, name = 'REST-API-Thread', daemon = True)
        self._thread.start()

    def close(self):
        self._thread_flag.clear()

    def _http_polling(self):
        try:
            while True:
                self._httpRequest()
                sleep(1)
                self._thread_flag.wait()
        except:
            traceback.print_exc()
            self.close()

    def _httpRequest(self):
        alarm_info = {}
        time = get(self._urls["url_time"], headers = self._headers)
        # Check if it was successful
        if(time.status_code != 200):
            # not successful, go on threading
            self._thread_flag.set()
            return
        # Convert the responses text to string and deserialize the json
        time = time.json()
        alarm_info["hour"] = time["attributes"]["hour"]
        alarm_info["minute"] = time["attributes"]["minute"]
        alarm_info["second"] = time["attributes"]["second"]
        state = get(self._urls["url_state"], headers = self._headers)
        # Convert the responses text to string and deserialize the json
        state = state.json()
        alarm_info["state"] = state["state"]
        # Request was successful, stop the thread
        self.close()