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
        time = get(self._urls["url_time"], headers = self._headers)
        print(time.text)
        state = get(self._urls["url_state"], headers = self._headers)
        print(state.text)