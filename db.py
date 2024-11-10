import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

DB_URL = os.getenv("DB_URL")
DB_TOKEN = os.getenv("DB_TOKEN")
DB_ORG = os.getenv("DB_ORG")

client = InfluxDBClient(url=DB_URL, token=DB_TOKEN, org=DB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


BUCKET = "my-bucket"
MEASUREMENT = "my_measurement"
TAG_SET = ["connection_type", "LoRaWAN"]
FIELD_KEY = "temperature"


def write_to_db(field_value):
    p = Point(MEASUREMENT).tag(TAG_SET[0], TAG_SET[1]).field(FIELD_KEY, field_value)

    write_api.write(bucket=BUCKET, record=p)
