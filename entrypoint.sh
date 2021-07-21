#!/bin/bash

if [ -z "$DISCORD_TOKEN" ]; then
	echo "cannot start bot, no token was specified"
fi
cd /opt/
python3 ./discord.py
