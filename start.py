from Alarm_Stop_Button.alarm_stop_button import AlarmStopButton
from Broker.broker import Broker
from time import sleep
import traceback

if __name__ == "__main__":
    thread_objects =[]

    # Central broker
    broker = Broker()

    # Components
    alarm_stop_button = AlarmStopButton(broker, 1, .125)


    try:
        while(True):
            sleep(10)
    except KeyboardInterrupt as e:
        print(e)
    except:
        traceback.print_exc()

    for thread_object in thread_objects:
        if hasattr(thread_object, 'stop_thread'):
            thread_object.stop_thread()
    print('Alle Threads beendet!!!')