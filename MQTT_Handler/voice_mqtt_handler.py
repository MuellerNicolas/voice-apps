from MQTT_Handler.mqtt_receiver import MQTTReceiver
import threading
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
        self._mqtt_receiver = MQTTReceiver(broker, self._ip, self._port)
        # Thread zum empfangen der MQTT Nachrichten
        self._thread_flag = threading.Event()
        self._thread = threading.Thread(target= self._run_receive_msg, daemon = True)
        self._thread.start()
        
    def close(self):
        self._thread_flag.set()

    def _run_receive_msg(self):
        self._broker.publish('bullshit')
        # start mqtt receiver
        try:
            self._mqtt_receiver.run()
        except:
            pass
            # logging.warning("Error in mqtt_receiver run")
            # traceback.print_exc()
        finally:
            self._mqtt_receiver.disconnect()
            # Schliessen der MQTT Verbindung