import json

import paho.mqtt.client as mqtt


def connect_mqtt_with_credentials(client: mqtt.Client):
    with open('mqtt_settings.json') as json_settings_file:
        settings = json.load(json_settings_file)

    client.username_pw_set(settings["username"], settings["password"])
    client.connect(settings["server_url"], settings["port"])
