import traceback
import paho.mqtt.client as mqtt

class MQTTReceiver(mqtt.Client):
    def __init__(self, broker, ip_adress, port):
        super().__init__()
        self._broker = broker
        self._ip_adress = ip_adress #192.168.178.19
        self._port = port   #1883

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
        print('publsihing')
        print(msg.payload)
        self._broker.publish('wakeword-status', msg.payload)

    def run(self):
        self.connect(self._ip_adress, self._port)
        # Subscribe to all topics
        self.subscribe('#')
    	
        # Special mqtt msg callback
        self.message_callback_add('rhasspy/en/transition/SnowboyWakeListener', self._broker_notify_wakeword)

        # error (bzw. rc) zeigt den Status des Verbindungsverlustes an
        # returned error > 0 dann ist ein Fehler aufgtreten
        error = 0
        while error == 0:
            error = self.loop()
        return error