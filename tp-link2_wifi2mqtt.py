#!/usr/bin/env python3

import requests
import re
import paho.mqtt.publish as publish
import sys
import json
import urllib3
urllib3.disable_warnings()

rpc_url = 'https://192.168.178.25/cgi-bin/luci/rpc'
user = sys.argv[1]
pw = sys.argv[2]
mqtt_broker = 'localhost'
mqtt_auth = {'username': sys.argv[3], 'password': sys.argv[4]}

def send_to_mqtt(mqtt_broker, mqtt_auth, hosts):
  doc = json.dumps({ "online": hosts, "_timestamp": str(datetime.datetime.now())})
  publish.single(topic="sensors/wifi/online", payload=doc, hostname=mqtt_broker, auth=mqtt_auth, retain=False)

def auth_body(user, pw):
  return {
    'id': 1,
    'method': 'login',
    'params': [
      user,
      pw
    ]
  }

def host_list_body():
  return {
    'id': 1,
    'method': 'call',
    'params': [
      'iwinfo wlan0 assoclist'
    ]
  }

if __name__ == '__main__':
  session = requests.Session()
  auth_response  = session.post(rpc_url + '/auth', verify=False, data=json.dumps(auth_body(user,pw)))
  ar = json.loads(auth_response.text)
  auth_token = ar['result']
  host_list_response = session.post(rpc_url + '/sys', verify=False, params={'auth':auth_token}, data=json.dumps(host_list_body()))
  host_count = len(re.findall('(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}', host_list_response.text))
  send_to_mqtt(mqtt_broker, mqtt_auth, host_count)
