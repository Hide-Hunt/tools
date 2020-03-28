#!/usr/bin/env bash
python3 -m venv venv
source venv/bin/activate
pip install paho-mqtt protobuf
./compile_protobuf.sh