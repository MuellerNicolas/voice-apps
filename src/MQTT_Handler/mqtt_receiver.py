import json
import logging
import os
import threading

import paho.mqtt.client as mqtt
from Logger.logger_init import get_logger
from time import sleep

class MQTTReceiver(mqtt.Client):
    def __init__(self, broker):
        super().__init__()
        self._broker = broker
        # read mqtt setting 4 connection
        path = os.path.join(os.path.dirname(__file__), 'mqtt_settings.json')
        with open(path) as f:
            mqtt_settings = json.load(f)
        self._ip_adress = mqtt_settings["ip"]   # usually 192.168.178.19
        self._port = mqtt_settings["port"]  # usually 1883
        #setup logging
        self.enable_logger(get_logger(__name__))
        # Thread zum empfangen der MQTT Nachrichten
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def close(self):
        self._thread_flag.set()
        self.disconnect()

    # for msg: msg.topic, msg.qos, msg.payload
    # any message which did not match the special callbacks

    def on_message(self, mqttrec, obj, msg):
        pass

    def _broker_notify_wakeword(self, mosq, obj, msg):
        # test if the payload is in byte format (starting with b)
        msg_test = str(msg.payload)
        if(msg_test[0] == 'b'):
            # decode byte to utf-8
            msg.payload = msg.payload.decode("utf-8")
        # payload possibilities: loaded and the opposite: listening
        self._broker.publish('wakeword-status', msg.payload)

    def _broker_notify_show_time(self, mosq, obj, msg):
        self._broker.publish('voice-show-time')

    def _run(self):
        # ensure the mqtt-broker is already running
        sleep(30)
        try:
            self.connect(self._ip_adress, self._port)
            # Subscribe to all topics
            self.subscribe('#')
            """
                !!!Attention!!!
                Adapt the wake word topic to your specific wake word topic, which may vary 
                by wake word engine and your country
            """
            # Special mqtt msg callback
            self.message_callback_add(
                'rhasspy/en/transition/SnowboyWakeListener', self._broker_notify_wakeword)
            self.message_callback_add(
                'rhasspy/intent/GetTime', self._broker_notify_show_time)

            # error (bzw. rc) zeigt den Status des Verbindungsverlustes an
            # returned error > 0 dann ist ein Fehler aufgtreten
            error = 0
            while error == 0:
                error = self.loop()
            return error
        finally:
            get_logger(__name__).info(f'error in mqtt receiver rc = {error}')
            logging.exception("error info: ")
