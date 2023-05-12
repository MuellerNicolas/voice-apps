import json
import logging
import os
import threading
import sys

import paho.mqtt.client as mqtt
from logger.logger_init import get_logger
from time import sleep


class MQTTIntendReceiver(mqtt.Client):
    def __init__(self, broker, terminateProgram):
        super().__init__()
        self._broker = broker
        self._recreateSelf = terminateProgram
        # Callback to active Hotword on button press
        self._broker.subscribe("alarm-button-stop", self._unmute)
        # read mqtt setting for connection
        path = os.path.join(os.path.dirname(__file__),
                            'mqtt_intend_settings.json')
        with open(path) as f:
            mqtt_settings = json.load(f)
        self._ip_adress = mqtt_settings.get("ip")  # usually 192.168.178.19
        self._port = mqtt_settings.get("port")  # usually 1883
        self._user = mqtt_settings.get("user")
        self._password = mqtt_settings.get("password")
        # setup logging
        self.enable_logger(get_logger(__name__))
        # Thread zum empfangen der MQTT Nachrichten
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def close(self):
        get_logger(__name__).info(f'disconnect from mqtt broker on {self._ip_adress}:{self._port}')
        self.disconnect()
        self._thread_flag.set()

    # for msg: msg.topic, msg.qos, msg.payload
    # any message which did not match the special callbacks

    def on_message(self, mqttrec, obj, msg):
        pass

    def _broker_notify_wakeword(self, mosq, obj, msg):
        self._broker.publish('wakeword-status')

    def _broker_notify_show_time(self, mosq, obj, msg):
        self._broker.publish('show-time')

    def _broker_notify_led_on(self, mosq, obj, msg):
        self._broker.publish('led-on')

    def _broker_notify_led_rainbow(self, mosq, obj, msg):
        self._broker.publish('led-rainbow')

    def _broker_notify_led_off(self, mosq, obj, msg):
        self._broker.publish('led-off')
        
    def _broker_notify_led_mute(self, mosq, obj, msg):
        self._broker.publish('led-mute')

    def _broker_notify_get_alarm_state(self, mosq, obj, msg):
        self._broker.publish('trigger-button-alarm-info')

    def _broker_notify_get_alarm_time(self, mosq, obj, msg):
        self._broker.publish('trigger-button-alarm-info')

    def _broker_notify_get_alarm_info(self, mosq, obj, msg):
        self._broker.publish('trigger-button-alarm-info')

    # Active Hotword
    def _unmute(self, *args, **kwargs):
        # Start listening again
        topic = "hermes/hotword/toggleOn"
        payload = '{"siteId": "default", "reason": ""}'
        qos = 0
        retain = False
        self.publish(topic, payload=payload, qos=qos, retain=retain)
        # Enable Hermes LED Control again
        topic = "hermes/leds/toggleOn"
        payload = '{"siteId" : "default"}'
        qos = 0
        retain = False
        self.publish(topic, payload=payload, qos=qos, retain=retain)
        
    def on_disconnect(self, userdata, rc, properties):
        # error (bzw. rc) zeigt den Status des Verbindungsverlustes an
        # returned error > 0 dann ist ein Fehler aufgtreten
        if rc != 0:
            get_logger(__name__).warn(f'error in mqtt receiver rc = {rc}')
            get_logger(__name__).warn(f'Unexpected MQTT disconnection. Will auto-reconnect')
            
    def on_connect(self, userdata, flags, rc, properties):
        get_logger(__name__).info(f'connected to mqtt broker on {self._ip_adress}:{self._port}')
        
        # Subscribe to all topics
        self.subscribe('#')
        """
            !!!Attention!!!
            Adapt the wake word topic to your specific wake word topic, which may vary 
            by wake word engine and your country
        """
        # Wakeword
        self.message_callback_add(
            'hermes/hotword/+/detected', self._broker_notify_wakeword)
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
        # led mute
        self.message_callback_add(
            'voice-apps/led/mute', self._broker_notify_led_mute)
        # get alarm status
        self.message_callback_add(
            'hermes/intent/AlarmState', self._broker_notify_get_alarm_state)
        # get alarm time
        self.message_callback_add(
            'hermes/intent/AlarmTime', self._broker_notify_get_alarm_time)
        # get alarm info
        self.message_callback_add(
            'hermes/intent/AlarmInfo', self._broker_notify_get_alarm_time)

    def _run(self):
        try:
            if self._user is not None and self._password is not None:
                self.username_pw_set(self._user, self._password)
            self.connect(self._ip_adress, self._port)
            self.loop_forever(timeout=1.0)
        except Exception as e:
            get_logger(__name__).error(f'Failed to connect mqtt to {self._ip_adress}:{self._port}')
            get_logger(__name__).error(e, exc_info=True)
            self.close()
            self._recreateSelf(self)
            