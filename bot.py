import json
from sqlite3 import paramstyle
import requests
import re
import telegram
from telegram.ext import Updater, CommandHandler
from connect import Buscar_Message_id_and, Buscar_Message_id_or

#p_offset="266734324"

with open('.token') as file:
    list = file.readlines()
    TOKEN = list[0].rstrip("\n")
    file.close()

lista=[]
maximotag=20

def extractRelation(p_offset,number_message):
    url = "https://api.telegram.org/bot"+TOKEN+"/getUpdates"

    offsetParam = {
        'offset' : p_offset,
        'limit' : 100
    }
    resp = requests.get(url,params=offsetParam)
    caption = json.loads(resp.text)
    result = caption['result'][0]['channel_post']['caption']
    tags = result.split('#')

def copyMessage(number_message,chat_id):
    url = "https://api.telegram.org/bot"+TOKEN+"/copyMessage"
    parameters = {
        "chat_id" : chat_id,
        "from_chat_id" : "-1001735492901",
        "message_id" : number_message    
    }
    resp = requests.get(url, data = parameters)
def sendMessage(chat_id, text):
    url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage"
    parameters = {
        "chat_id": chat_id,
        "text": text
    }
    resp = requests.get(url, data = parameters)

def start(update, context):
    global lista
    lista = []
    id_chat = update.effective_user['id']
    sendMessage(id_chat, "Ingrese los tags a buscar en formato (/tag param1 param2 ...): ")

def tags(update, context):
    caption_mensaje_actual = update.message['text'].split(" ")
    global lista
    for tag in caption_mensaje_actual:
        lista.append(tag.lower())
    lista.remove("/tag")

def searchall(update, context):
    global lista
    global maximotag
    chat_id = update.effective_user['id']
    param = re.sub("\[|\]","",str(lista))
    lista=[]
    cursor = Buscar_Message_id_or(param).fetchmany(maximotag)
    maximotag=20
    for message_id in cursor:
        copyMessage(message_id[1],chat_id)

def search(update, context):
    global lista
    global maximotag
    chat_id = update.effective_user['id']
    param = re.sub("\[|\]","",str(lista))
    lista=[]
    cursor = Buscar_Message_id_and(param).fetchmany(maximotag)
    maximotag=20
    for message_id in cursor:
        copyMessage(message_id[1],chat_id)

def maxtag(update, context):
    global maximotag
    nuevo_max = int(update.message['text'].split(" ")[1])
    maximotag = nuevo_max

if __name__ == "__main__":
    my_bot = telegram.Bot(token = TOKEN)
    #print(my_bot.getMe())

updater = Updater(my_bot.token, use_context=True)

dp = updater.dispatcher

#Creamos los manejadores
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tag", tags))
dp.add_handler(CommandHandler("searchall", searchall))
dp.add_handler(CommandHandler("maxtags", maxtag))
dp.add_handler(CommandHandler("search", search))

updater.start_polling()

updater.idle()

    

