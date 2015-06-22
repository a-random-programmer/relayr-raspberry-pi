#!/usr/bin/env python

"""
Demo receiving prototype device data via Python SDK from relayr cloud.

This code needs the relayr and paho-mqtt packages to be installed,
e.g. with:

pip install git+https://github.com/relayr/python-sdk
pip install paho-mqtt>=1.1
"""

import time
import json

from relayr import Client
from relayr.dataconnection import MqttStream


# MQTT credentials (from relayr.io dashboard)
# *** REPLACE WITH YOUR OWN! ***
creds = {
    "user":     "565738d3-29ef-442d-b055-debb1a1be13c",
    "password": "442SsprjRXbY",
    "clientId": "TVlc51xjvQxywVd67GhvhPA",
    "topic":    "/v1/565738d3-29ef-442d-b055-debb1a1be13c/"
}

def main():
    "Get some current sensor values from a prototype."

    # Use token from your relayr API keys page.
    # *** REPLACE WITH YOUR OWN! ***
    c = Client(token='kKSWtiYvfFoTHD1RY-d7Lif4tPRhUKgU')
    dev = c.get_device(id=creds['user'])
    def mqtt_callback(topic, payload):
        print json.loads(payload)['readings']
    stream = MqttStream(mqtt_callback, [dev])
    stream.start()
    time.sleep(10)
    stream.stop()


if __name__ == '__main__':
    main()
