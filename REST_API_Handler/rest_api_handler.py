from requests import get, post
import json
import os
import threading
import traceback
from time import sleep

class RESTApiHandler:
    def __init__(self, broker):
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
        # Broker
        self._broker = broker
        self._broker.subscribe("alarm-request-info", self._initiate_request_callback)
        self._broker.subscribe("alarm-button-switch", self._set_alarm_state)

        # Thread
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(target= self._http_polling, name = 'REST-API-Thread', daemon = True)
        self._thread.start()

    def close(self):
        self._thread_flag.set()

    def _http_polling(self):
        try:
            while True:
                time = self._get_alarm_time()
                state = self._get_alarm_state()
                # Check if the request was successful
                if(time.status_code != 200 or state.status_code != 200):
                    # Not successful, go on threading
                    self._thread_flag.set()
                else:
                    # Successful
                    alarm_info = self._format_alarm_info(time, state)
                    # Send the alarm_info to all subscribers
                    self._broker.publish('alarm-info', alarm_info)
                    # Request was successful, stop the thread
                    return
                sleep(1)
                self._thread_flag.wait()
        except:
            traceback.print_exc()
        finally:
            self.close()

    def _get_alarm_time(self):
        time = get(self._urls["url_time"], headers = self._headers)
        return time

    def _get_alarm_state(self):
        state = get(self._urls["url_state"], headers = self._headers)
        return state

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
    
    def _set_alarm_state(self, info):
        # execute on alarm-switch-button push
        time = self._get_alarm_time()
        state = self._get_alarm_state()
        alarm_info = self._format_alarm_info(time, state)
        # Switch alarm state
        if(alarm_info["state"] == "on"):
            # switch the alarm off
            state_response = post(self._urls["url_state"], headers = self._headers, json = {"state": "off"})
            # check successful and give visual feedback
            if(state_response.status_code != 200):
                self._broker.publish('alarm-info', 'fail')
            else:
                self._broker.publish('alarm-info', 'okay')
        else:
            # switch the alarm on
            state_response = post(self._urls["url_state"], headers = self._headers, json = {"state": "on"})
            # check successful and give visual feedback
            if(state_response.status_code != 200):
                self._broker.publish('alarm-info', 'fail')
            else:
                self._broker.publish('alarm-info', 'okay')

    def _initiate_request_callback(self):
        self._thread_flag.set()