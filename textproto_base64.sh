#!/usr/bin/env bash
for file in $(ls resources/*.textproto); do
	echo "----- $file -----"
	protoc --encode=ch.epfl.sdp.game.comm.Game proto/Game.proto < $file | base64
	echo "------------------------------------------"
done
