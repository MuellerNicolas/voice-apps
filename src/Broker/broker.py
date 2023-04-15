import threading
from Logger.logger_init import get_logger

class Broker:
    def __init__(self):
        # Dictionairy: Mapping subscribers to topics
        self._topics = {}

    def subscribe(self, topic, callback):
        if topic not in self._topics:
            self._topics[topic] = []

        #print(topic, ": ", callback)
        self._topics[topic].append(callback)

    def unsubscribe(self, topic, callback):
        if topic in self._topics:
            self._topics[topic].remove(callback)

    # notification to all subscribers about a specific topic
    def publish(self, topic, *args, **kwargs):
        if not topic in self._topics:
            get_logger(__name__).warn(f'published but no subscribers for topic "{topic}"')
            return

        get_logger(__name__).info(f'published topic "{topic}", args "{args}", kwargs "{kwargs}"')
        for callback in self._topics[topic]:
            notify_thread = threading.Thread(
                target=callback, args=args, kwargs=kwargs, name="app-broker-thread")
            notify_thread.start()
