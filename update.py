from sqlite3 import connect
import requests
from telethon import TelegramClient
from connect import INSERT_NAME_SONG, INSERT_SONG
import psycopg2
from config import config
import time

with open('.token') as file:
    token = file.readlines()
    file.close()

TOKEN = token[0].rstrip("\n")
api_id = token[1].rstrip("\n")
api_hash = token[2].rstrip("\n")
group_username = token[3].rstrip("\n")

client = TelegramClient('owo', api_id, api_hash).start()

def Get_last_id_song():
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("select message_id from songs order by id_tag desc limit 1")
    for message in cursor:
        id_lista = message[0]
    return id_lista

def Inserccion_masiva_canciones_update(id_lista):
    id_lista = int(id_lista)
    for message in client.iter_messages(group_username, reverse=True):
        if(message.id > int(id_lista)):
            owner_name = "name="+ str(message.post_author) 
            INSERT_SONG(message.id,owner_name)
            for tag in str(message.text).split('#'):
                if (tag!=""):
                    INSERT_SONG(message.id,tag)
        else:
            pass
def Inserccion_masiva_nombres_canciones_update(id_lista):
    id_lista = int(id_lista)
    for message in client.iter_messages(group_username, reverse=True):
        if(message.id > int(id_lista)):
            try:
                name_song=str(message.media.document.attributes[0].performer)+" - " + str(message.media.document.attributes[0].title)
                INSERT_NAME_SONG(message.id,name_song)
            except:
                print("error")
                pass
        else:
            pass

id_lista = Get_last_id_song()
Inserccion_masiva_canciones_update(id_lista)
Inserccion_masiva_nombres_canciones_update(id_lista)
