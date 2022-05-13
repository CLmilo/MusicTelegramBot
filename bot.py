import json
from sqlite3 import paramstyle
from unicodedata import name
import requests
import re
import telegram
from telegram.ext import Updater, CommandHandler
from connect import Add_to_list, Buscar_Message_id_and, Buscar_Message_id_or, Create_user, Create_list, Get_max_song, Get_post_author, Modify_max_song, Modify_post_author, Obtain_id_list

#p_offset="266734324"

with open('.token') as file:
    list = file.readlines()
    TOKEN = list[0].rstrip("\n")
    file.close()

lista_tag=[]

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

def help(update, context):
    id_chat = update.effective_user['id']
    sendMessage(id_chat, "Ingrese los tags a buscar en formato (/tag param1 param2 ...): \nOpciones de búsqueda:\n/maxsongs : Número máximo de mensajes de respuesta (default=20).\n/search : Búsqueda de canciones que tengan todos los tags puestos.\n/searchall : Búsqueda de todas las canciones que cumplan con al menos uno de los tags puestos.")
    print(update.effective_user['id'])

def createuser(update,context):
    id = update.effective_user['id']
    nombre = update.effective_user['first_name']+" "+update.effective_user['last_name']
    Create_user(id, nombre)

def createlist(update,context):
    id = update.effective_user['id']
    name_list = update.message['text'].split(" ")[1]
    Create_list(id,name_list)

def addtolist(update,context):
    id = update.effective_user['id']
    mensaje = update.message['text'].split(" ")
    name_list = mensaje[1]
    id_lista = Obtain_id_list(id,name_list)
    lista_mensajes = []
    for message_id in mensaje:
        lista_mensajes.append(message_id)
    lista_mensajes.remove("/addtolist")
    lista_mensajes.remove(name_list)
    for message_id in lista_mensajes:
        Add_to_list(id_lista, message_id)
    
def searchall(update,context):
    lista_tag=[]
    chat_id = update.effective_user['id']
    caption_mensaje_actual = update.message['text'].split(" ")
    for tag in caption_mensaje_actual:
        lista_tag.append(tag.lower())
    post_author = "name=" + str(Get_post_author(str(chat_id)))
    if post_author == "name=all":
        pass
    else:
        lista_tag.append(post_author)
    lista_tag.remove("searchall")
    param = re.sub("\[|\]","",str(lista_tag))
    lista_tag=[]
    max_songs = int(Get_max_song(str(chat_id)))
    cursor = Buscar_Message_id_or(param).fetchmany(max_songs)
    if (cursor==""):
        sendMessage(chat_id,"No hay resultados")
    for message_id in cursor:
        copyMessage(message_id[1],chat_id)
        sendMessage(chat_id, "Código de Canción : "+str(message_id[1]))

def search(update,context):
    global maximotag
    lista_tag=[]
    chat_id = update.effective_user['id']
    caption_mensaje_actual = update.message['text'].split(" ")
    for tag in caption_mensaje_actual:
        lista_tag.append(tag.lower())
    post_author = "name=" + str(Get_post_author(str(chat_id)))
    if post_author == "name=all":
        pass
    else:
        lista_tag.append(post_author)
    lista_tag.remove("/search")
    param = re.sub("\[|\]","",str(lista_tag))
    lista_tag=[]
    cant=len(lista_tag)-1
    cant=str(cant)
    max_songs = Get_max_song(str(chat_id))
    print(max_songs)
    cursor = Buscar_Message_id_and(param,cant).fetchmany(max_songs)
    if (cursor==""):
        sendMessage(chat_id,"No hay resultados")
    maximotag=20
    for message_id in cursor:
        copyMessage(message_id[1],chat_id)
        sendMessage(chat_id, "Código de Canción : "+str(message_id[1]))

def maxsongs(update,context):
    id_user = str(update.effective_user["id"])
    nuevo_max = str((update.message['text'].split(" ")[1]))
    Modify_max_song(id_user, nuevo_max)

def post_author(update,context):
    id_user = str(update.effective_user["id"])
    post_author = str(int(update.message['text'].split(" ")[1]))
    Modify_post_author(id_user,post_author)

if __name__ == "__main__":
    my_bot = telegram.Bot(token = TOKEN)
    #print(my_bot.getMe())

updater = Updater(my_bot.token, use_context=True)

dp = updater.dispatcher

#Creamos los manejadores
dp.add_handler(CommandHandler("searchall", searchall))
dp.add_handler(CommandHandler("maxsongs", maxsongs))
dp.add_handler(CommandHandler("search", search))
dp.add_handler(CommandHandler("createuser", createuser))
dp.add_handler(CommandHandler("createlist", createlist))


updater.start_polling()

updater.idle()

