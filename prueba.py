from sqlite3 import connect
import requests
import telegram
from telethon import TelegramClient
from connect import INSERT_NAME_SONG, INSERT_SONG
import psycopg2
import config
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
    print(id_lista)
    conn.close()
    return id_lista
    

def Inserccion_masiva_canciones_update(id_lista):
    for message in client.iter_messages(group_username, reverse=True):
        owner_name = "name="+ str(message.post_author) 
        INSERT_SONG(message.id,owner_name)
        if(message.id > int(id_lista)):
            for tag in str(message.text).split('#'):
                if (tag!=""):
                    INSERT_SONG(message.id,tag)
        else:
            pass
def Inserccion_masiva_nombres_canciones_update(id_lista):
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

def recreacion_tabla_songs():
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("drop table songs")
    conn.commit()
    cursor.execute("create table songs(id_tag SERIAL,message_id VARCHAR(10), tag VARCHAR(100))")
    conn.commit()
    conn.close

def Inserccion_forzada_canciones(client,group_username):
    for message in client.iter_messages(group_username, reverse=True):
        owner_name = "name="+ str(message.post_author) 
        INSERT_SONG(message.id,owner_name)
        for tag in str(message.text).split('#'):
            if (tag!=""):
                INSERT_SONG(message.id,tag)

def recreacion_tabla_name_songs():
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("drop table name_songs")
    conn.commit()
    time.sleep(3)
    cursor.execute("create table name_songs(message_id NUMERIC(9) PRIMARY KEY,name_song VARCHAR(100))")
    conn.commit()
    conn.close()

def Inserccion_forzada_nombres_canciones():
    for message in client.iter_messages(group_username, reverse=True):
        try:
            name_song=str(message.media.document.attributes[0].performer)+" - " + str(message.media.document.attributes[0].title)
            INSERT_NAME_SONG(message.id,name_song)
        except:
            print("error")
            pass


#Inserccion_masiva_nombres_canciones()
#Inserccion_masiva_canciones()

def Inserccion_masiva_canciones():
    for message in client.iter_messages(group_username, reverse=True):
        owner_name = "name="+ str(message.post_author) 
        INSERT_SONG(message.id,owner_name)
        for tag in str(message.text).split('#'):
            if (tag!=""):
                INSERT_SONG(message.id,tag) 

def Inserccion_masiva_nombres_canciones():
    for message in client.iter_messages(group_username, reverse=True):
        try:
            name_song=str(message.media.document.attributes[0].performer)+" - " + str(message.media.document.attributes[0].title)
            INSERT_NAME_SONG(message.id,name_song)
        except:
            print("error")
            pass

def setWebhook():
    url = "https://api.telegram.org/bot"+TOKEN+"/setWebhook"
    parameters = {
        "url" : "207.246.76.77:8443"
    }
    resp = requests.get(url, data = parameters)

