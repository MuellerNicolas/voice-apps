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

    def _broker_notify_show_time(self, mosq, obj, msg):
        self._broker.publish('voice-show-time')
    def _broker_notify_led_on(self, mosq, obj, msg):
        self._broker.publish('led-on')
    def _broker_notify_led_rainbow(self, mosq, obj, msg):
        self._broker.publish('led-rainbow')
    def _broker_notify_led_off(self, mosq, obj, msg):
        self._broker.publish('led-off')
        
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
            # Time app
            self.message_callback_add(
                'hermes/intent/GetTime', self._broker_notify_show_time)
            # light leds
            self.message_callback_add(
                'hermes/intent/LedOn', self._broker_notify_led_on)
            # led rainbow
            self.message_callback_add(
                'hermes/intent/LedRainbow', self._broker_notify_led_rainbow)
            # turn led off
            self.message_callback_add(
                'hermes/intent/LedOff', self._broker_notify_led_off)
            # error (bzw. rc) zeigt den Status des Verbindungsverlustes an
            # returned error > 0 dann ist ein Fehler aufgtreten
            error = 0
            while error == 0:
                error = self.loop()
            return error
        finally:
            get_logger(__name__).info(f'error in mqtt receiver rc = {error}')
            logging.exception("error info: ")
