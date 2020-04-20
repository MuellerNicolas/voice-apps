from requests import get
import json
import os

class RESTApiHandler:
    def __init__(self, url, state):
        self._url_time = url
        self._url_state = state

    def _httpRequest(self):
        # get the home assistant authorization key
        path = os.path.join(os.path.dirname(__file__), 'Home_Assistant_Authorization.json')
        with open(path) as f:
            home_assistant = json.load(f)
        headers = {
            "Authorization": home_assistant['authorization'],
            "content-type": "application/json",
        }

        time = get(self._url_time, headers = headers)
        print(time.text)
        state = get(self._url_state, headers = headers)
        print(state.text)