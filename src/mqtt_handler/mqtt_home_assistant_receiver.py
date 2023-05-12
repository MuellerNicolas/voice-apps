import json
import os
import threading

import paho.mqtt.client as mqtt
from logger.logger_init import get_logger
from time import sleep


class MQTTHomeAssistantReceiver(mqtt.Client):
    def __init__(self, broker, recreateSelf):
        super().__init__(client_id='voice-apps')
        self._broker = broker
        self._recreateSelf = recreateSelf
        # read mqtt setting for connection
        path = os.path.join(os.path.dirname(__file__),
                            'mqtt_home_assistant_settings.json')
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

    def on_disconnect(self, userdata, rc, properties):
        # error (bzw. rc) zeigt den Status des Verbindungsverlustes an
        # returned error > 0 dann ist ein Fehler aufgtreten
        if rc != 0:
            get_logger(__name__).warn(f'error in mqtt receiver rc = {rc}')
            get_logger(__name__).warn(f'Unexpected MQTT disconnection. Will auto-reconnect')

    def on_connect(self, userdata, flags, rc, properties):
        # Callback for Alarm Info
        self.message_callback_add(
            'home-assistant/alarm-clock/nicolas', self._broker_notify_alarm_info)
        # Subscribe to all topics
        self.subscribe('#')
        get_logger(__name__).info(f'connected to mqtt broker on {self._ip_adress}:{self._port}')
    
    def on_connect_fail(self, mqttc, userdata, rc):
        get_logger(__name__).warn(f'failed to connect to mqtt broker on {self._ip_adress}:{self._port} with rc {rc}')

    def _run(self):
        try:
            # make sure the listening service are ready yet
            sleep(10)
            if self._user is not None and self._password is not None:
                self.username_pw_set(self._user, self._password)
            self.connect(self._ip_adress, self._port)
            raise Exception('whoops')
            self.loop_forever()
        except Exception as e:
            get_logger(__name__).error(f'Failed to connect mqtt to {self._ip_adress}:{self._port}')
            get_logger(__name__).error(e, exc_info=True)
            self.close()
            self._recreateSelf(self)