#!/usr/bin/env python3
import paho.mqtt.client as mqtt

gameID = 0
playerID = 1
topic = str(gameID) + "/" + str(playerID)


def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = mqtt.Client()
client.on_message = on_message
client.username_pw_set("jprnwwdd:jprnwwdd", "aDs-KxLr1cTqGgBSWKExxmCUXBcsWfOE")
client.connect("kangaroo.rmq.cloudamqp.com", 1883)

client.subscribe(topic)

client.loop_forever()

