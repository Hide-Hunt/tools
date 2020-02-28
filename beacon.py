#!/usr/bin/env python3
import csv
import sys
import time
import threading

import paho.mqtt.client as mqtt
import proto.Location_pb2 as proto

if len(sys.argv) != 3:
    print("Usage: ./beacon game_id replay_file")
    print("\tgame_id is a positive integer")
    print("\treplay_file is a csv file with columns(player_id, timestamp, latitude, longitude)")
    exit(0)

gameID = sys.argv[1]
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

with open(sys.argv[2]) as file:
    # CSV FORMAT:
    # 0          1          2         3
    # player_id, timestamp, latitude, longitude
    data = csv.reader(file)

    b.acquire()
    for row in data:
        if current_time == 0:
            current_time = int(row[1])
        else:
            payload = proto.Location()
            payload.latitude = float(next_row[2])
            payload.longitude = float(next_row[3])
            print(next_row)
            client.publish(gameID+"/"+next_row[0], payload.SerializeToString())
        next_row = row
        time.sleep(int(row[1]) - current_time)
        current_time = int(row[1])
    print(next_row)
    payload = proto.Location()
    payload.latitude = float(next_row[2])
    payload.longitude = float(next_row[3])
    client.publish(gameID+"/"+next_row[0], payload.SerializeToString())

