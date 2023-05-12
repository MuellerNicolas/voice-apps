from time import sleep
import signal

from alarm_sound.alarm_sound import AlarmSound
from alarm_buttons.alarm_stop_button import AlarmStopButton
from alarm_buttons.alarm_info_button import AlarmInfoButton
from alarm_time_keeper.alarm_time_keeper import AlarmTimeKeeper
from broker.broker import Broker
from led.led_alarm_status import LEDAlarmStatus
from led.led_clock import LEDClock
from led.led_others import LEDOthers
from logger.logger_init import get_logger, setup_logging
from mqtt_handler.mqtt_intend_receiver import MQTTIntendReceiver
from mqtt_handler.mqtt_home_assistant_receiver import MQTTHomeAssistantReceiver
from rest_api_handler.rest_api_handler import RESTApiHandler

thread_objects = []

def handleStop(_signum, frame):
    get_logger(__name__).info(f'received signal to stop')
    global ACTIVE
    ACTIVE = False

# used to recreate the MQTT Handlers as sometimes no connection to the mqtt is established
def recreateMqttHandler(mqttHandler):
    if isinstance(mqttHandler, MQTTIntendReceiver):
        get_logger(__name__).info(f'MQTTIntendReceiver recreated!')
        thread_objects.remove(mqttHandler)
        thread_objects.append(MQTTIntendReceiver(broker, recreateMqttHandler))
    elif isinstance(mqttHandler, MQTTHomeAssistantReceiver):
        get_logger(__name__).info(f'MQTTHomeAssistantReceiver recreated!')
        thread_objects.remove(mqttHandler)
        thread_objects.append(MQTTHomeAssistantReceiver(broker, recreateMqttHandler))


if __name__ == "__main__":
    ACTIVE = True
    
    signal.signal(signal.SIGTERM, handleStop)
    signal.signal(signal.SIGINT, handleStop)
 
    # Setup logging
    setup_logging(default_filename='logging_config.json')
    get_logger(__name__).info(f'voice-apps started!')
    # Central broker
    broker = Broker()
    # array including all components
    thread_objects.extend([
        AlarmTimeKeeper(broker),                           # Time Keeper
        # Alarm sound - PIN-SONG = Passive Buzzer / PIN_BEEP = Active Buzzer
        AlarmSound(broker, PIN_SONG=6, PIN_BEEP=4),
        AlarmStopButton(broker, PIN=0, POLLING=.125),      # Button - stop
        AlarmInfoButton(broker, PIN=2, POLLING=.125),      # Button - info
        LEDClock(broker, 0, "blue", "red", "yellow"),      # LED Clock
        # LED alarm status on switch
        LEDAlarmStatus(broker),
        # LED other stuff like lights or rainbow
        LEDOthers(broker),
        # REST-API-Handler for Home Assistant
        #RESTApiHandler(broker),
        # MQTT Receiver from mqtt-Broker of Rhasspy
        MQTTIntendReceiver(broker, recreateMqttHandler),
        # MQTT Receiver from Home Assistant
        MQTTHomeAssistantReceiver(broker, recreateMqttHandler),
    ])

    try:
        while(ACTIVE):
            sleep(10)
    except KeyboardInterrupt as e:
        get_logger(__name__).info(f'KeyboardInterrupt')
    except:
        get_logger(__name__).info(f'Shutdown due to error')
    finally:
        ACTIVE = False

    # close / stop all threads
    for thread_object in thread_objects:
        if hasattr(thread_object, 'close'):
            thread_object.close()
    get_logger(__name__).info(f'voice-apps stopped!')
