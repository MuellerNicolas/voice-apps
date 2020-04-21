from requests import get
import json
import os

class RESTApiHandler:
    def __init__(self):
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

    def _httpRequest(self):
        alarm_info = {}
        time = get(self._urls["url_time"], headers = self._headers)
        # Convert the responses text to string and deserialize the json
        time = time.json()
        alarm_info["hour"] = time["attributes"]["hour"]
        alarm_info["minute"] = time["attributes"]["minute"]
        alarm_info["second"] = time["attributes"]["second"]
        state = get(self._urls["url_state"], headers = self._headers)
        # Convert the responses text to string and deserialize the json
        state = state.json()
        alarm_info["state"] = state["state"]
        print(alarm_info)