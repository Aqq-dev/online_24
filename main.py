import os
import threading
import time
import logging
from pypresence import Presence
from flask import Flask
from keep_alive import keep_alive
import requests

logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TOKEN")

keep_alive()

client_id = '1392336534992064675'

rpc = Presence(client_id)
try:
    rpc.connect()
    logging.info("RPC connected successfully.")
except Exception as e:
    logging.error(f"Failed to connect RPC: {e}")

def rich_presence_loop():
    while True:
        try:
            rpc.update(
                state="test",
                details="Nexus bot",
                large_image="_1_",
                large_text="Aqq",
                small_image="nexus",
                small_text="nexus bot",
                start=time.time(),
                party_id="ae488379-351d-4a4f-ad32-2b9b01c91657",
                party_size=[1, 5],
                join="MTI4NzM0OjFpMmhuZToxMjMxMjM=",
                buttons=[
                    {"label": "Join Nexus", "url": "https://discord.gg/WwfhkmTWTg"},
                    {"label": "GitHub", "url": "https://github.com/nexus-bot"}
                ]
            )
            logging.info("Presence updated.")
        except Exception as e:
            logging.error(f"RPC Error: {e}")
        time.sleep(15)

def set_online_status():
    headers = {
        'Authorization': TOKEN,
        'Content-Type': 'application/json'
    }
    json_data = {
        'status': 'online',
        'since': 0,
        'afk': False
    }

    while True:
        try:
            response = requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json=json_data)
            if response.status_code == 200:
                logging.info("Online status updated.")
            else:
                logging.warning(f"Failed to update online status. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            logging.error(f"Status update error: {e}")
        time.sleep(300)

threading.Thread(target=rich_presence_loop, daemon=True).start()
threading.Thread(target=set_online_status, daemon=True).start()
