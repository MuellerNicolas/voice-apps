from Alarm_Stop_Button.alarm_stop_button import AlarmStopButton
from Broker.broker import Broker
from LED_Clock.led_clock import LEDClock
from time import sleep
import traceback

if __name__ == "__main__":
    # array with all used components
    thread_objects = []

    # Central broker
    broker = Broker()

    # Components
    # Button
    alarm_stop_button = AlarmStopButton(broker, 1, .125)
    thread_objects.append(alarm_stop_button)
    # LED Clock
    led_clock = LEDClock(broker, 0, "blue", "red", "yellow")
    thread_objects.append(led_clock)

    try:
        while(True):
            sleep(10)
    except KeyboardInterrupt as e:
        print(e)
    except:
        traceback.print_exc()

    # close / stop all threads
    for thread_object in thread_objects:
        if hasattr(thread_object, 'stop_thread'):
            thread_object.stop_thread()
    print('Alle Threads beendet!!!')