#!/usr/bin/env python3
import csv
import sys
import time
import threading

import paho.mqtt.client as mqtt

gameID = 0
playerID = 1
topic = str(gameID) + "/" + str(playerID)
b = threading.Semaphore(0)


def on_connect(client, userdata, flags, rc):
    b.release()


client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("jprnwwdd:jprnwwdd", "aDs-KxLr1cTqGgBSWKExxmCUXBcsWfOE")
client.connect("kangaroo.rmq.cloudamqp.com", 1883)
client.loop_start()

current_time = 0
next_row = []

with open(sys.argv[1]) as file:
    data = csv.reader(file)

    b.acquire()
    for row in data:
        if current_time == 0:
            current_time = int(row[0])
        else:
            print(next_row)
            client.publish(topic, str(next_row))
        next_row = row
        time.sleep(int(row[0]) - current_time)
        current_time = int(row[0])
    print(next_row)
    client.publish(topic, str(next_row))

