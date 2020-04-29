from MQTT_Handler.mqtt_receiver import MQTTReceiver

class MQTTHandler:
    def __init__(self, broker):
        self._broker = broker
        self._mqtt_receiver = MQTTReceiver(self._broker)
        self._setup()

    def setup(self):
        # start mqtt receiver
        self._mqtt_receiver.run()