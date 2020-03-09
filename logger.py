#!/usr/bin/env python3
import sys
import time

import paho.mqtt.client as mqtt

from proto import Location_pb2, Catch_pb2
from mqtt_helper import connect_mqtt_with_credentials

if len(sys.argv) != 3:
    print("Usage: ./logger game_id playerIDs")
    print("\t- game_id     is a positive integer")
    print("\t- playerIDs   is either a comma separated list(no space) or a range in the form [start,end]")
    exit(0)


def on_message(client, obj, msg):
    topic = msg.topic.split("/")
    if topic[1] == "catch":
        payload = Catch_pb2.Catch()
        payload.ParseFromString(msg.payload)
        print("catch," + str(int(time.time())) + "," + str(payload.predatorID) + "," + str(payload.preyID))
    else:
        payload = Location_pb2.Location()
        payload.ParseFromString(msg.payload)
        print("loc," + str(int(time.time())) + "," + topic[1] + "," + str(payload.latitude) + "," + str(payload.longitude))


gameID = sys.argv[1]
if sys.argv[2].startswith("["):
    strRange = sys.argv[2][1:-1].split(",")
    if len(strRange) != 2:
        print("Invalid range")
        exit(1)
    playerIDs = range(int(strRange[0]), int(strRange[1]))
else:
    playerIDs = list(map(lambda x: int(x), sys.argv[2].split(",")))

mqtt_client = client = mqtt.Client()
mqtt_client.on_message = on_message
connect_mqtt_with_credentials(mqtt_client)

mqtt_client.subscribe(str(gameID) + "/catch")  # Catch topic
for playerID in playerIDs:
    mqtt_client.subscribe(str(gameID) + "/" + str(playerID))

print("For game with id="+gameID)
print("\t-> Subscribed to catch topic")
print("\t-> Subscribed to player topics with ids in " + str(playerIDs))

mqtt_client.loop_forever()
