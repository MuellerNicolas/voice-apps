import json
import logging
import os
import threading

import paho.mqtt.client as mqtt
from Logger.logger_init import get_logger
from time import sleep


class MQTTHomeAssistantReceiver(mqtt.Client):
    def __init__(self, broker):
        super().__init__()
        self._broker = broker
        # read mqtt setting 4 connection
        path = os.path.join(os.path.dirname(__file__),
                            'mqtt_home_assistant_settings.json')
        with open(path) as f:
            mqtt_settings = json.load(f)
        path = os.path.join(os.path.dirname(__file__),
                            'MQTT_Home_Assistant_Authorization.json')
        with open(path) as f:
            mqtt_authorization = json.load(f)
        self._ip_adress = mqtt_settings["ip"]   # usually 192.168.178.21
        self._port = mqtt_settings["port"]  # usually 1883
        self._user = mqtt_authorization["user"]
        self._password = mqtt_authorization["password"]

        # setup logging
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

    def _broker_notify_alarm_info(self, mosq, obj, msg):
        response = json.loads(msg.payload.decode("utf-8"))
        alarm_info = {}
        alarm_info["hour"], alarm_info["minute"], alarm_info["second"] = map(
            int, response["time"].split(':'))
        alarm_info["state"] = response["state"]
        alarm_song = response["song"]
        # Send the alarm_info to all subscribers
        self._broker.publish('alarm-info', alarm_info)
        # Send the alarm_song to all subscribers
        self._broker.publish('alarm-song-selected', alarm_song)
        get_logger(__name__).info(
            f'received & published the following alarm_infos={alarm_info}, alarm_song={alarm_song}')

    def _run(self):
        # ensure the mqtt-broker is already running
        sleep(30)
        try:
            self.username_pw_set(self._user, self._password)
            self.connect(self._ip_adress, self._port)
            # Subscribe to all topics
            self.subscribe('#')
            # Callback for Alarm Info
            self.message_callback_add(
                'home-assistant/alarm-clock/nicolas', self._broker_notify_alarm_info)
            # error (bzw. rc) zeigt den Status des Verbindungsverlustes an
            # returned error > 0 dann ist ein Fehler aufgtreten
            error = 0
            while error == 0:
                error = self.loop()
            return error
        finally:
            get_logger(__name__).info(f'error in mqtt receiver rc = {error}')
            logging.exception("error info: ")
