#!/bin/bash

#Wait for the auth server to come up
until $(curl -k -XPOST --output /dev/null --silent https://video.datasetu.org:3002); do
	printf '.'
	sleep 1
done
	echo "ready"
