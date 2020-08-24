import logging
from time import sleep

from Alarm_Sound.alarm_sound import AlarmSound
from Alarm_Stop_Button.alarm_stop_button import AlarmStopButton
from Alarm_Switch_Button.alarm_switch_button import AlarmSwitchButton
from Alarm_Time_Keeper.alarm_time_keeper import AlarmTimeKeeper
from Broker.broker import Broker
from LED_Alarm_Status.led_alarm_status import LEDAlarmStatus
from LED_Clock.led_clock import LEDClock
from Logger.logger_init import get_logger, setup_logging
from MQTT_Handler.mqtt_receiver import MQTTReceiver
from REST_API_Handler.rest_api_handler import RESTApiHandler

if __name__ == "__main__":
    # Setup logging
    setup_logging(default_filename = 'logging_config.json')
    get_logger(__name__).info(f'voice-apps started!')
    # Central broker
    broker = Broker()
    # array including all components
    thread_objects = [
        AlarmSound(broker, PIN_SONG=6, PIN_BEEP=4),        # Alarm sound - PIN-SONG = Passive Buzzer / PIN_BEEP = Active Buzzer
        AlarmStopButton(broker, PIN=0, POLLING=.125),      # Button - stop
        #AlarmSwitchButton(broker, PIN=2, POLLING=.125),    # Button - switch
        MQTTReceiver(broker),                              # MQTT
        LEDClock(broker, 0, "blue", "red", "yellow"),      # LED Clock
        LEDAlarmStatus(broker),                            # LED alarm status on switch
        RESTApiHandler(broker),                            # REST-API-Handler for Home Assistant
        AlarmTimeKeeper(broker),                           # Time Keepre
    ]


    try:
        while(True):
            sleep(10)
    except KeyboardInterrupt as e:
        get_logger(__name__).info(f'KeyboardInterrupt')
    except:
        get_logger(__name__).info(f'Shutdown or Error')
        logging.exception('Shutdown or Error!')

    # close / stop all threads
    for thread_object in thread_objects:
        if hasattr(thread_object, 'close'):
            thread_object.close()
    get_logger(__name__).info(f'voice-apps stopped!')
