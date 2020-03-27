#!/usr/bin/env python3
import csv
import sys
import time

import paho.mqtt.client as mqtt

import proto.Location_pb2
import proto.Catch_pb2
from mqtt_helper import connect_mqtt_with_credentials

if len(sys.argv) < 3:
    print("Usage: ./beacon game_id replay_file [options]")
    print("\tgame_id      is a positive integer")
    print("\treplay_file  is a csv file with columns(player_id, timestamp, latitude, longitude)")
    print("\tEvent type to publish:")
    print("\t\t--all    publish all events")
    print("\t\t--loc    publish location events(default)")
    print("\t\t--catch  publish catch events")
    exit(0)

gameID = sys.argv[1]

if len(sys.argv) > 3:
    options = list(map(lambda o: o[2:], sys.argv[3:]))  # Removing "--" from each option
else:
    options = ["loc"]

mqtt_client = mqtt.Client()
connect_mqtt_with_credentials(mqtt_client)
mqtt_client.loop_start()


def publish_loc(csv_line):
    payload = proto.Location_pb2.Location()
    payload.latitude = float(csv_line[3])
    payload.longitude = float(csv_line[4])
    mqtt_client.publish(gameID + "/" + csv_line[2], payload.SerializeToString())


def publish_catch(csv_line):
    payload = proto.Catch_pb2.Catch()
    payload.predatorID = int(csv_line[2])
    payload.preyID = int(csv_line[3])
    mqtt_client.publish(gameID + "/catch", payload.SerializeToString())


def handle_line(csv_line):
    if "all" in options or csv_line[0] in options:
        print(csv_line)
        {
            "loc": publish_loc,
            "catch": publish_catch,
        }[csv_line[0]](csv_line)
    else:
        print("(ignored) " + str(csv_line))


with open(sys.argv[2]) as file:
    # CSV FORMAT:
    # 0 (event)  1           2            3          4
    # loc,       timestamp,  player_id,   latitude,  longitude
    # catch,     timestamp,  predatorID,  preyID
    data = csv.reader(file)

    current_time = 0
    next_row = []
    print("Starting to publish events")
    for row in data:
        if current_time == 0:
            current_time = int(row[1])
        else:
            handle_line(next_row)
        next_row = row
        time.sleep(int(row[1]) - current_time)
        current_time = int(row[1])

    handle_line(next_row)
