import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
# from typing import NamedTuple
import time
import logging
from bme280 import *

MQTT_ADDRESS = '192.168.0.80'
MQTT_USER = 'mqtt'
MQTT_PASSWORD = 'mqtt'
MQTT_TOPIC = 'sensors/weather'
MQTT_REGEX = 'weather/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'BME280'
LOCATION = 'Duesseldorf'

# class SensorData(NamedTuple):
#     location: str
#     measurement: str
#     value: float

def getSensorData():
    (chip_id, chip_version) = readBME280ID()
    temperature,pressure,humidity = readBME280All()
    return temperature, pressure, humidity

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)



# def persists(msg):
#     current_time = datetime.datetime.utcnow().isoformat()
#     json_body = [
#         {
#             "measurement": "weather",
#             "tags": {},
#             "time": current_time,
#             "fields": {
#                 "value": int(msg.payload)
#             }
#         }
#     ]
#     logging.info(json_body)
#     influx_client.write_points(json_body)

# logging.baseConfig(level=logging.INFO)
# influx_client = InfluxDBClient('docker', 8086, database='weather_station')

def main():
    
    

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    while(1):
        temperature,pressure,humidity = getSensorData()
        print("Temperature : " + str(temperature) + " C")
        print("Pressure : " + str(pressure) + " hPa")
        print("Humidity : " + str(humidity) + " %")

        payloadtemp = "weather,location=" + LOCATION + " temperature=" + str(temperature)
        payloadpress = "weather,location=" + LOCATION + " pressure=" + str(pressure)
        payloadhum = "weather,location=" + LOCATION + " humidity=" + str(humidity)

        if mqtt_client.publish(MQTT_TOPIC + "/temperature", payload=payloadtemp, qos=0):
            print("Temperature sent!")
        else:
            print("Sending Temperature has failed, reconnecting and trying again")
            mqtt_client.connect(MQTT_ADDRESS, 1883)
            time.sleep(1)
            mqtt_client.publish(MQTT_TOPIC + "/temperature", payload=payloadtemp, qos=0)
        time.sleep(1)

        if mqtt_client.publish(MQTT_TOPIC + "/pressure", payload=payloadpress, qos=0):
            print("Pressure sent!")
        else:
            print("Sending Pressure has failed, reconnecting and trying again")
            mqtt_client.connect(MQTT_ADDRESS, 1883)
            time.sleep(1)
            mqtt_client.publish(MQTT_TOPIC + "/pressure", payload=payloadpress, qos=0)
        time.sleep(1)

        if mqtt_client.publish(MQTT_TOPIC + "/humidity", payload=payloadhum, qos=0):
            print("Humidity sent!")  
        else:
            print("Sending Humidity has failed, reconnecting and trying again")
            mqtt_client.connect(MQTT_ADDRESS, 1883)
            time.sleep(1)
            mqtt_client.publish(MQTT_TOPIC + "/humidity", payload=payloadhum, qos=0)
        time.sleep(60)
if __name__=="__main__":
    main()