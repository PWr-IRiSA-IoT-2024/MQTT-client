import json
import logging

from .convert_payload import convert_payload


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def decode_uplink(message):
    try:
        data = json.loads(message)

        encoded_payload = data["uplink_message"]["frm_payload"]
        type, value = convert_payload(encoded_payload)

        measurement = type
        tags = {"device": data["end_device_ids"]["device_id"]}
        time = data["uplink_message"]["received_at"]
        fields = {"value": value}

        return measurement, tags, time, fields
    
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON payload: %s", e)
        return None, None, None, None