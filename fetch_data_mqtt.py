#!/usr/bin/env python

"""
Demo receiving prototype device data via MQTT from relayr cloud.

This subscribes to a given MQTT topic and receives messages
for this topic. This code needs the paho-mqtt package to be
installed, e.g. with:

pip install paho-mqtt>=1.1   
"""

import json

import paho.mqtt.client as mqtt


# MQTT credentials (from relayr.io dashboard)
# *** REPLACE WITH YOUR OWN! ***
creds = creds = {
    "user":     "565738d3-29ef-442d-b055-debb1a1be13c",
    "password": "442SsprjRXbY",
    "clientId": "TVlc51xjvQxywVd67GhvhPA",
    "topic":    "/v1/565738d3-29ef-442d-b055-debb1a1be13c/"
}


class MqttDelegate(object):
    "A delegate class providing callbacks for an MQTT client."

    def __init__(self, client, credentials):
        self.client = client
        self.credentials = credentials

    def on_connect(self, client, userdata, flags, rc):
        print('Connected.')
        self.client.subscribe(self.credentials['topic'] + 'data')

    def on_message(self, client, userdata, msg):
        print('Message received: %s' % msg.payload.decode('utf-8'))


def main(credentials):
    client = mqtt.Client(client_id=credentials['clientId'])
    delegate = MqttDelegate(client, creds)
    client.on_connect = delegate.on_connect
    client.on_message = delegate.on_message
    user, password = credentials['user'], credentials['password']
    client.username_pw_set(user, password)
    try:
        print('Connecting to mqtt server.')
        server, port = credentials['server'], credentials['port']
        client.connect('mqtt.relayr.io', port=1883, keepalive=60)
    except:
        print('Connection failed, check your credentials!')
        return
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print('')


if __name__ == '__main__':
    main(creds)
