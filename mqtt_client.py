import os
import sys
import json
import logging
import signal
import paho.mqtt.client as mqtt

from dotenv import load_dotenv

load_dotenv()

from utils.decode_uplink import decode_uplink
from utils.db import write_data_to_db


required_vars = ["APP_ID", "TENANT_ID", "MQTT_HOST", "MQTT_PORT", "ACCESS_KEY"]

for var in required_vars:
    if not os.getenv(var):
        sys.exit(f"Error: Environment variable {var} is not set.")

APP_ID = os.getenv("APP_ID")
TENANT_ID = os.getenv("TENANT_ID")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
ACCESS_KEY = os.getenv("ACCESS_KEY")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Starting MQTT client...")


def on_connect(client, _userdata, _flags, reason_code, _properties):
    if reason_code == 0:
        logging.info(f"Successfully connected to {MQTT_HOST}:{MQTT_PORT} MQTT broker")
        
        # The '+' wildcard subscribes to any device uplinks within the application
        client.subscribe(f"v3/{APP_ID}@{TENANT_ID}/devices/+/up")
    else:
        logging.error("Connection failed with return code %s", reason_code)


def on_disconnect(client, _userdata, reason_code):
    if reason_code != 0:
        logging.warning("Unexpected disconnection, attempting to reconnect...")
        client.reconnect()
    else:
        logging.info("Disconnected from MQTT broker")


def on_message(_client, _userdata, msg):
    try:
        payload = msg.payload.decode()
        measurement, tags, time, fields = decode_uplink(payload)

        if not all([measurement, tags, time, fields]):
            raise ValueError("Failed to decode uplink message")

        write_data_to_db(measurement, tags, time, fields)

        logging.info("Message received and added to queue from topic %s", msg.topic)
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON payload: %s", e)


def on_log(_client, _userdata, _level, buf):
    logging.debug("MQTT log: %s", buf)


def shutdown_handler(_signum, _frame):
    logging.info("Shutdown signal received, stopping MQTT client...")
    client.disconnect()
    client.loop_stop()
    logging.info("MQTT client stopped")


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(f"{APP_ID}@{TENANT_ID}", ACCESS_KEY)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_log = on_log

try:
    client.connect(MQTT_HOST, MQTT_PORT, 60)
except Exception as e:
    logging.error("Failed to connect to MQTT broker: %s", e)
    exit(1)

client.loop_forever()
