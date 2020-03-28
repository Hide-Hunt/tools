#!/usr/bin/env bash
python3 -m venv venv
source venv/bin/activate
pip install paho-mqtt

if [[ -n $(command -v pacman) ]]; then
  sudo pacman -S protobuf
elif [[ -n $(command -v apt) ]]; then
    sudo apt install -y protobuf-compiler
elif [[ -n $(command -v brew) ]]; then
    brew install protobuf
else
    echo "Missing implementation for your system, sorry!"
    exit 1
fi

pip install protobuf # Does this need to be installed after protobuf itself ? I don't know...
bash compile_protobuf.sh

bash generate_mqtt_settings.sh