# WeatherStation

# HowTo :

1. Navigate to influxdb
``` sudo docker-compose up -d ```
---
2. Confirm active containers with ``` sudo docker ps ```
----
3. Open InfluxDB Command Line interface 
``` sudo docker exec -it influxdb influx ```
---
4. Create Database with Username and Password
``` 
CREATE DATABASE weather_stations
CREATE USER mqtt WITH PASSWORD ‘mqtt’
GRANT ALL ON weather_stations TO mqtt
```
---
5. Navigate to Grafana Dashboard in browser RPi-IP:3000
---
6. Log in, go to Datasources and add the InfluxDB with URL => http://RPi-IP:8086
---
7. Import the Dashboard



---
8. Navigate into folder sensor

``` 
sudo docker build -t mqttconnector:1.0 .
sudo docker run -d --device /dev/i2c-1  mqttconnector:1.0 
```
---
**9. Profit**

