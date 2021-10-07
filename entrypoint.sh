#!/bin/sh

if [ -z "$DISCORD_TOKEN" ]; then
	echo "cannot start bot, no token was specified"
fi
cd /app/
python3 dumberchild.py
