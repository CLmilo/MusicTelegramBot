from sqlite3 import connect
import requests
import pandas as pd
import telegram
from telethon import TelegramClient
from connect import INSERT_SONG

with open('.token') as file:
    token = file.readlines()
    file.close()

api_id = token[1].rstrip("\n")
api_hash = token[2].rstrip("\n")
group_username = token[3].rstrip("\n")

client = TelegramClient('owo', api_id, api_hash).start()

def Inserccion_masiva_canciones():
    for message in client.iter_messages(group_username, reverse=True):
        for tag in str(message.text).split('#'):
            if (tag!=""):
                INSERT_SONG(message.id,tag)

