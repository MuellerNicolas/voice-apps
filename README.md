# Voice-Apps
Actions triggered by intends, received via MQTT and HTTP. Therefore the application is using the publish-subscribe design pattern. New components can easily implemented by subscibing to certain topics at the broker. **This application is embedded in an offline, mostly open source ecosystem.**

## Attention
I developed this python program in my freetime and therefore focused on integrating this special hardware to my smart home ecosystem. You might be able to use it without some of the components i've used or even with your own hardware, if you adapt the code accordingly. This application shows an approach on how to add an alarm to your (rhasspy) voice assistant. Even if you have the same setup and smart home ecosystem, there are a few things, you would have to adjust in the code. (mainly concerning the home assistant entities and rest-api)

## Current Apps
- Alarm Clock (ft. Super Mario & Star Wars melody via the GPIO Pins of the Matrix Voice board)
- Display the time

## Dependencies
- Note: All the dependecies I have used are working 100% offline
- Listening to Rhasspy's (Voice Assistant) MQTT commands
- Getting the alarm time aswell as additional infos from Home Assistant's REST-API (Smart Home Assistant)

## How it works
- You can press the enable/disable button to set the state of the alarm or just force an update of the alarm info from the backend
- Use the stop/time button to stop the alarm if the alarm is active or just show the time
- The alarm can also be stopped by saying rhasspy's wakeword (in my case Jarvis)
- **Important: The MQTT Topic for the wake word detection has to be adapted depending on your wake word engine and language**
- **Wakeword LEDs are not support in the current version, check out [HermesLedControl](https://github.com/project-alice-assistant/HermesLedControl) for a nice alternative**
- The functionality of rhasspy should be fully maintained

## Hardware
- RaspberryPi3B+
- Matrix Voice Standard
- Passive Buzzer for the melody
- Active Buzzer for the pure beeps
- TTP223 Touch Sensor to enable and disable the alarm
- TTP223 Touch Sensor to stop the active alarm and to show the time

## Setup inspiration
<img src="https://github.com/MuellerNicolas/voice-apps/blob/master/src/img/voice-control-jarvis.jpg" width="500em"></img><br/>
<img src="https://github.com/MuellerNicolas/voice-apps/blob/master/src/img/voice-control-from-side.jpg" width="500em"></img><br/>
<img src="https://github.com/MuellerNicolas/voice-apps/blob/master/src/img/voice-control-from-above.jpg" width="500em"></img>
