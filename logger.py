#!/usr/bin/env python3
import base64
import time

import paho.mqtt.client as mqtt
import proto.Location_pb2 as proto

gameID = 0
playerID = 1

topic = str(gameID) + "/" + str(playerID)
topic2 = str(gameID) + "/24"


def on_message(client, obj, msg):
    payload = proto.Location()
    payload.ParseFromString(msg.payload)
    msg_player_id = msg.topic.split("/")[1]
    print(msg_player_id + "," + str(int(time.time())) + "," + str(payload.latitude) + "," + str(payload.longitude))


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set("jprnwwdd:jprnwwdd", "aDs-KxLr1cTqGgBSWKExxmCUXBcsWfOE")
client.connect("kangaroo.rmq.cloudamqp.com", 1883)

client.subscribe(topic)
client.subscribe(topic2)

client.loop_forever()

