from MQTT_Handler.mqtt_receiver import MQTTReceiver
import traceback
import logging

class MQTTHandler:
    def __init__(self, broker):
        self._broker = broker
        self._mqtt_receiver = MQTTReceiver(self._broker, '192.168.178.41', 1883)
        self._setup()

    def _setup(self):
        # start mqtt receiver
        try:
            self._mqtt_receiver.run()
        except:
            pass
            # logging.warning("Error in mqtt_receiver run")
            # traceback.print_exc()