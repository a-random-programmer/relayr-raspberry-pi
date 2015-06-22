#/usr/bin/env python

import sys
import time

def read_temperature(device_id):
    "Read float temperature value from 1wire device DS18B20."

    with open('/sys/bus/w1/devices/%s/w1_slave' % device_id) as f:
        text = f.read().strip()
        fragments = text.split()
        return float(fragments[-1][2:]) / 1000.

if __name__ == '__main__':
    try:
        device_id = sys.argv[1]
    except IndexError:
        print('Please enter sensor ID.')
        sys.exit()
    while True:
        print(read_temperature(device_id))
        time.sleep(1)
