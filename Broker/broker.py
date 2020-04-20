import threading

#  Orientierung an dem in "Entwicklung eines IoT-Devices" gezeigten Entwurfsmuster Publish-Subscribe

class Broker:
    def __init__(self):
        # Dictionairy: Mapping subscribers to topics
        self._topics = {}

    def subscribe(self, topic, callback):
        if topic not in self._topics:
            self._topics[topic] = []

        self._topics[topic].append(callback)

    def unsubscribe(self, topic, callback):
        if topic in self._topics:
            self._topics[topic].remove(callback)

    # notification to all subscribers about a specific topic
    def publish(self, topic, *args, **kwargs):
        if not topic in self._topics:
            return
        
        for callback in self._topics[topic]:
            notify_thread = threading.Thread(target = callback, args = args, kwargs = kwargs, name = "app-broker-thread")
            notify_thread.start()