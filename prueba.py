from sqlite3 import connect
import requests
import telegram
from telethon import TelegramClient
from connect import INSERT_NAME_SONG, INSERT_SONG

with open('.token') as file:
    token = file.readlines()
    file.close()

TOKEN = token[0].rstrip("\n")
api_id = token[1].rstrip("\n")
api_hash = token[2].rstrip("\n")
group_username = token[3].rstrip("\n")

client = TelegramClient('owo', api_id, api_hash).start()


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

#Inserccion_masiva_nombres_canciones()
#Inserccion_masiva_canciones()

def hardening(input):
    input = input.replace("-","")
    return input

param = input()
print(hardening(param))


def setWebhook():
    url = "https://api.telegram.org/bot"+TOKEN+"/setWebhook"
    parameters = {
        "url" : "207.246.76.77:8443"
    }
    resp = requests.get(url, data = parameters)

