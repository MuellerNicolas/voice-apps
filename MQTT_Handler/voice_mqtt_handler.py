from MQTT_Handler.mqtt_receiver import MQTTReceiver
import traceback
import logging
import json
import os

class MQTTHandler:
    def __init__(self, broker):
        # internal pubsub broker
        self._broker = broker

        # read mqtt setting 4 connection
        path = os.path.join(os.path.dirname(__file__), 'mqtt_settings.json')
        with open(path) as f:
            mqtt_settings = json.load(f)
        self._ip = mqtt_settings["ip"]
        self._port = mqtt_settings["port"]

        # mqtt receiver for wakeword detection
        self._mqtt_receiver = MQTTReceiver(self._broker, self._ip, self._port)
        self._setup()

    def _setup(self):
        # start mqtt receiver
        try:
            self._mqtt_receiver.run()
        except:
            pass
            # logging.warning("Error in mqtt_receiver run")
            # traceback.print_exc()