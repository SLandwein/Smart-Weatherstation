# docker run --device /dev/gpiomem -d whatever
FROM arm32v7/python:3

WORKDIR /usr/src/app  

COPY sensorDataToMQTT.py ./
COPY requirements.txt ./
COPY bme280.py ./

RUN pip install -r requirements.txt

CMD ["python", "./sensorDataToMQTT.py"]
