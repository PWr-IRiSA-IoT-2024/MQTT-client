import json
import base64
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def decode_uplink(message):
    try:
        data = json.loads(message)

        encoded_payload = data["uplink_message"]["frm_payload"]
        payload = base64.b64decode(encoded_payload)
        payload = json.loads(payload)

        measurement = payload # Update when final structure is known
        tags = {"device": data["end_device_ids"]["device_id"]}
        time = data["uplink_message"]["rx_metadata"][0]["time"]
        fields = {"value": payload} # Update when final structure is known

        return measurement, tags, time, fields
    
    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON payload: %s", e)
        return None, None, None, None