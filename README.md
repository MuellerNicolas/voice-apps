# Voice-Apps
Actions triggered by intends, received via MQTT and HTTP. Therefore the application is using the publish-subscribe design pattern. New components can easily implemented by subscibing to certain topics at the broker.

## Current Apps
- Alarm Clock
- Enables LEDs by speech

## Dependencies
- Listening to Rhasspy's (Voice Assistant) MQTT commands
- Getting the time of a RESP-API from Home Assistant (Smart Home Assistant)

## Hardware
- RaspberryPi3B+
- Matrix Voice Standard
