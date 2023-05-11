import logging
from time import sleep
import signal

from Alarm_Sound.alarm_sound import AlarmSound
from Alarm_Buttons.alarm_stop_button import AlarmStopButton
from Alarm_Buttons.alarm_info_button import AlarmInfoButton
from Alarm_Time_Keeper.alarm_time_keeper import AlarmTimeKeeper
from Broker.broker import Broker
from LED.led_alarm_status import LEDAlarmStatus
from LED.led_clock import LEDClock
from LED.led_others import LEDOthers
from Logger.logger_init import get_logger, setup_logging
from MQTT_Handler.mqtt_intend_receiver import MQTTIntendReceiver
from MQTT_Handler.mqtt_home_assistant_receiver import MQTTHomeAssistantReceiver
from REST_API_Handler.rest_api_handler import RESTApiHandler

def terminateProgram():
    get_logger(__name__).info(f'received signal to stop')
    global ACTIVE
    ACTIVE = False
    
def handleStop(_signum, frame):
    terminateProgram()

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
    thread_objects = [
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
        MQTTIntendReceiver(broker, terminateProgram),
        # MQTT Receiver from Home Assistant
        MQTTHomeAssistantReceiver(broker, terminateProgram),
    ]

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
