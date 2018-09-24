#!/usr/bin/env python3

import sys
import json
import datetime
import requests
import warnings
import paho.mqtt.publish as publish

login = 'https://192.168.178.2/login.cgi'
user = sys.argv[1]
pw = sys.argv[2]
mqtt_broker = "localhost"
mqtt_auth = {'username': sys.argv[3], 'password': sys.argv[4]}


def fetch_hosts_from_ap(login, user, pw):
    """
    Return hosts in the network from status.cgi of
    our ubiquity network wireless ap
    :login: str (url)
    :user: str
    :pw: str
    :returns: float
    """ # arrange new session and login
    s = requests.Session()
    s.get(login, verify=False)

    # query ip/status.cgi which results in json
    r = s.post(login, verify=False, data={'username': user, 'password': pw, 'uri':'/status.cgi'})
    r = r.text
    r = json.loads(r)

    # fetch count of wireless connections from json
    try:
        hosts = r['wireless']['count']
    except KeyError:
        hosts = 0

    return hosts

def send_to_mqtt(mqtt_broker, mqtt_auth, hosts):
    doc = json.dumps({ "online": hosts, "_timestamp": str(datetime.datetime.now())})
    publish.single(topic="sensors/wifi/online", payload=doc, hostname=mqtt_broker, auth=mqtt_auth, retain=False)

# disable warnings
warnings.filterwarnings('ignore', 'Unverified HTTPS request')

# fetch hosts
hosts = fetch_hosts_from_ap(login, user, pw)

# send to mqtt
send_to_mqtt(mqtt_broker, mqtt_auth, hosts)
