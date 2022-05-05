#!/bin/bash
cd /home/pi/Discord_Bot
screen -X -S bot kill
screen -S bot python3.10 bot.py
/home/pi/Discord_Bot/Scripts/botReload.sh