FROM python:3.10-slim

RUN pip install paho-mqtt
RUN pip install influxdb

COPY mqtt_client.py /app/mqtt_client.py

WORKDIR /app

CMD ["python", "mqtt_client.py"]
