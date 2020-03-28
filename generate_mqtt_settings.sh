#!/usr/bin/env bash

function ask_yes_or_no() {
    read -p "$1 ([y]es or [N]o): "
    case $(echo $REPLY | tr '[A-Z]' '[a-z]') in
        y|yes) echo "yes" ;;
        *)     echo "no" ;;
    esac
}

echo "Please setup your mqtt_settings.json file with appropriate connexion information"
echo "Indicate your MQTT server URL (example \"kangaroo.rmq.cloudamqp.com\"):"
read server_url
echo "Indicate the server port (typically 1883):"
read server_port
echo "Indicate your username:"
read username
echo "Indicate your password:"
read password

if [[ -f "mqtt_settings.json" ]]; then
  if [[ "no" == $(ask_yes_or_no "mqtt_settings.json already exists. Do you want to overwrite?") ]]; then
    echo "Skipped"
    exit 0
  fi
fi

echo "Generating mqtt_settings.json"
echo '{"username": "$username","password": "$password","server_url": "$server_url","port": $server_port}' | jq . > mqtt_settings.json