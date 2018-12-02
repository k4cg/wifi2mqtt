#!/usr/bin/env python3

import requests
import re
import paho.mqtt.publish as publish
import sys


def wifi_host_count(url):
  response = requests.get(url)
  if response.status_code != requests.code.ok:
    return 0

  match = re.search('(?<=active_wireless::).*?(?=})', response.text)
  data = match.group(0)
  # data is a comma seperated string of values. 10 values per hosts
  return len(data.split(',')) / 10

def send_to_mqtt(mqtt_broker, mqtt_auth, hosts):
  doc = json.dumps({ "online": hosts, "_timestamp": str(datetime.datetime.now())})
  publish.single(topic="sensors/wifi/online", payload=doc, hostname=mqtt_broker, auth=mqtt_auth, retain=False)

def main():
  info_url = 'http://192.168.178.2/Info.live.htm'
  mqtt_broker = "localhost"
  mqtt_auth = {'username': sys.argv[1], 'password': sys.argv[2]}

  count = wifi_host_count(info_url)
  send_to_mqtt(mqtt_broker, mqtt_auth, count)

if __name__ == '__main__':
  main()
