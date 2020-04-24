from Alarm_Stop_Button.alarm_stop_button import AlarmStopButton
from Alarm_Switch_Button.alarm_switch_button import AlarmSwitchButton
from Broker.broker import Broker
from REST_API_Handler.rest_api_handler import RESTApiHandler
from LED_Clock.led_clock import LEDClock
from LED_Alarm_Status.led_alarm_status import LEDAlarmStatus
from Alarm_Time_Keeper.alarm_time_keeper import AlarmTimeKeeper
from time import sleep
import traceback

if __name__ == "__main__":
    # array with all used components
    thread_objects = []

    # Central broker
    broker = Broker()

    # Components
    # Button - stop 
    #alarm_stop_button = AlarmStopButton(broker, 1, .125)
    #thread_objects.append(alarm_stop_button)
    # Button - switch
    alarm_switch_button = AlarmSwitchButton(broker, 1, .125)
    thread_objects.append(alarm_switch_button)
    # LED Clock
    led_clock = LEDClock(broker, 0, "blue", "red", "yellow")
    thread_objects.append(led_clock)
    # LED alarm status on switch
    led_alarm_status = LEDAlarmStatus(broker)
    thread_objects.append(led_alarm_status)
    # REST-API-Handler for Home Assistant
    rest_api_handler = RESTApiHandler(broker)
    thread_objects.append(rest_api_handler)
    # Time Keeper
    alarm_time_keeper = AlarmTimeKeeper(broker)
    thread_objects.append(broker)
    
    try:
        while(True):
            sleep(10)
    except KeyboardInterrupt as e:
        print(e)
    except:
        traceback.print_exc()

    # close / stop all threads
    for thread_object in thread_objects:
        if hasattr(thread_object, 'close'):
            thread_object.close()
    print('Alle Threads beendet!!!')