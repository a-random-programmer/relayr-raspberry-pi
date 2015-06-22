#!/usr/bin/env python

"""
Demo publishing device data via MQTT to relayr cloud.

This code needs the paho-mqtt package to be installed, e.g. with:

pip install paho-mqtt>=1.1
"""

import json
import time

import paho.mqtt.client as mqtt


# MQTT credentials (from relayr.io dashboard)
# *** REPLACE WITH YOUR OWN! ***
creds = {
    "user":     "565738d3-29ef-442d-b055-debb1a1be13c",
    "password": "442SsprjRXbY",
    "clientId": "TVlc51xjvQxywVd67GhvhPA",
    "topic":    "/v1/565738d3-29ef-442d-b055-debb1a1be13c/"
}


# ATTENTION !!!
# DO NOT try to set values under 200 ms of the server
# will kick you out
publishing_period = 1000


class MqttDelegate(object):
    "A delegate class providing callbacks for an MQTT client."

    def __init__(self, client, credentials):
        self.client = client
        self.credentials = credentials

    def on_connect(self, client, userdata, flags, rc):
        print('Connected.')
        self.client.subscribe(self.credentials['topic'] + 'cmd')
    
    def on_publish(self, client, userdata, mid):
        print('Message published.')


def read_temperature(device_id):
    "Read float temperature value from 1wire device DS18B20."

    with open('/sys/bus/w1/devices/%s/w1_slave' % device_id) as f:
        text = f.read().strip()
        data = text.split()
        temp = float(data[-1][2:]) / 1000.

    return temp


def publish_sensor_data(credentials, publishing_period):
    ""

    client = mqtt.Client(client_id=credentials['clientId'])
    delegate = MqttDelegate(client, creds)
    client.on_connect = delegate.on_connect
    client.on_publish = delegate.on_publish
    user, password = credentials['user'], credentials['password']
    client.username_pw_set(user, password)
    try:
        print('Connecting to mqtt server.')
        server, port = credentials['server'], credentials['port']
        client.connect('mqtt.relayr.io', port=1883, keepalive=60)
    except:
        print('Connection failed, check your credentials!')
        return
    
    # set 200 ms as minimum publishing period
    if publishing_period < 200:
        publishing_period = 200

    while True:
        client.loop()
        # read sensor
        device_id = '28-000004a365ef'
        sensor_value = read_temperature(device_id)
        # publish temerature data
        message = {
            'meaning': 'temperature',
            'value': sensor_value
        }
        client.publish(credentials['topic'] + 'data', json.dumps(message))
        time.sleep(publishing_period / 1000.)

        # publish more complex data (uncomment to see effect)
        # message = {
        #     'meaning': 'fancy_stuff',
        #     'value': {
        #         'temperature_kelvin': sensor_value * 9/5. + 32,
        #         'temperature_fahrenheit': sensor_value ** 2
        #     }
        # }
        # client.publish(credentials['topic'] + 'data', json.dumps(message))
        # time.sleep(publishing_period / 1000.)


if __name__ == '__main__':
    publish_sensor_data(creds, publishing_period)
