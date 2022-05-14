import json
from sqlite3 import paramstyle
import requests
import re
import telegram
from telegram.ext import Updater, CommandHandler
from connect import Add_to_list, Buscar_Message_id_and, Buscar_Message_id_or, Create_user, Create_list, Delete_playlist, Delete_song_in_playlist, Get_max_song, Get_playlistr, Get_post_author, Get_songs_in_list, Get_userlists, Modify_max_song, Modify_post_author, Obtain_id_list, Get_playlist

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
    sendMessage(id_chat, """Crea un usuario con /createuser la primera vez
    Ingrese los tags a buscar en formato (/search param1 param2 ...) or (/searchall): 
    /search : Búsqueda de canciones que tengan todos los tags puestos.
    /searchall : Búsqueda de todas las canciones que cumplan con al menos uno de los tags puestos.
    Opciones de búsqueda:
    /maxsongs: Número máximo de mensajes de respuesta (default=20). 
    /post_author: Persona que ha subido la canción (ver su nombre en el canal), si deseas regresar a buscar todos colocar "all".
    Opciones de lista:
    /createlist: Cree una lista con el formato (/createlist nombredelista) el nombre de la lista sin espacios.
    /deletelist: Elimine una lista con el formato (/deletelist nombredelista) el nombre de la lista sin espacios(no hay backup tenga cuidado).
    /addtolist: Añada canciones a la lista con el formato(/addtolist nombredelista codigo_cancion1 codigo_cancion2 ...) donde el código de canción lo ves buscando canciones con search.
    /rmfromlist: Remover canciones de una lista con el formato (/rmfromlist nombredelista codigo_cancion1 codigo_cancion2 ...).
    /listplaylists: Mostar todas tus listas 
    Reproducción:
    /play: Reproducir una lista en el orden guardado con el formato (/play nombredelista).
    /playr: Reproducir una lista en orden aleatorio con el formato (/playr nombredelista).
    """)

def createuser(update,context):
    id = update.effective_user['id']
    nombre = update.effective_user['first_name']+" "+update.effective_user['last_name']
    Create_user(id, nombre)

def createlist(update,context):
    id = update.effective_user['id']
    name_list = update.message['text'].split(" ")[1]
    cursor = Create_list(id,name_list)
    print (cursor)

def addtolist(update,context):
    id = str(update.effective_user['id'])
    mensaje = update.message['text'].split(" ")
    name_list = str(mensaje[1])
    id_lista = str(Obtain_id_list(id,name_list))
    lista_mensajes = []
    for message_id in mensaje:
        lista_mensajes.append(message_id)
    lista_mensajes.remove("/addtolist")
    lista_mensajes.remove(name_list)
    for message_id in lista_mensajes:
        Add_to_list(id_lista, message_id)

def removefromlist(update,context):
    id = str(update.effective_user['id'])
    mensaje = update.message['text'].split(" ")
    name_list = str(mensaje[1])
    id_lista = str(Obtain_id_list(id,name_list))
    lista_mensajes = []
    for message_id in mensaje:
        lista_mensajes.append(message_id)
    lista_mensajes.remove("/rmfromlist")
    lista_mensajes.remove(name_list)
    for message_id in lista_mensajes:
        Delete_song_in_playlist(id_lista, message_id)

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
    lista_tag=[]
    chat_id = update.effective_user['id']
    caption_mensaje_actual = update.message['text'].split(" ")
    for tag in caption_mensaje_actual:
        lista_tag.append(tag.lower())
    table_author = Get_post_author(str(chat_id))
    for lines in table_author:
        post_author = "name=" + lines[0].lower()
    if post_author == "name=all":
        pass
    else:
        lista_tag.append(post_author)
    lista_tag.remove("/search")
    param = re.sub("\[|\]","",str(lista_tag))
    print(lista_tag)
    cant=len(lista_tag)-1
    lista_tag=[]
    cant=str(cant)
    print ("\nelementos cantidad : " + cant)
    table_max_songs = Get_max_song(str(chat_id))
    for num in table_max_songs:
        max_songs = int(num[2])
    print("\nmaximo de canciones:" + str(max_songs))
    cursor = Buscar_Message_id_and(param,cant).fetchmany(max_songs)
    if (cursor==""):
        sendMessage(chat_id,"No hay resultados")
    for message_id in cursor:
        copyMessage(message_id[1],chat_id)
        sendMessage(chat_id, "Código de Canción : "+str(message_id[1]))

def maxsongs(update,context):
    id_user = str(update.effective_user["id"])
    nuevo_max = str((update.message['text'].split(" ")[1]))
    Modify_max_song(id_user, nuevo_max)

def post_author(update,context):
    id_user = str(update.effective_user["id"])
    post_author = str(update.message['text'])[13:]
    Modify_post_author(id_user,post_author)

def play(update,context):
    id_user = str(update.effective_user["id"])
    name_playlist = str(update.message["text"].split(" ")[1])
    id_list = str(Obtain_id_list(id_user, name_playlist))
    cursor = Get_playlist(id_list)
    for message_id in cursor:
        copyMessage(message_id[2], id_user)
        sendMessage(id_user, "Código de Canción : " + str(message_id[2]))

def playr(update,context):
    id_user = str(update.effective_user["id"])
    name_playlist = str(update.message["text"].split(" ")[1])
    id_list = str(Obtain_id_list(id_user, name_playlist))
    cursor = Get_playlistr(id_list)
    for message_id in cursor:
        copyMessage(message_id[2], id_user)
        sendMessage(id_user, "Código de Canción : " + str(message_id[2]))

def deleteplaylist(update,context):
    id_user = str(update.effective_user["id"])
    name_playlist = str(update.message["text"].split(" ")[1])
    id_list = str(Obtain_id_list(id_user, name_playlist))
    cursor = Delete_playlist(id_list)
    print(cursor)

def listplaylists(update,context):
    id_user = str(update.effective_user["id"])
    listas = Get_userlists(id_user)
    mensaje = ""
    mensaje= mensaje +"Las listas existentes son: "
    for lista in listas:
        canciones = Get_songs_in_list(str(lista[0]))
        mensaje = mensaje + "\n- "+str(lista[1])+ " contiene: "
        for cancion in canciones:
           mensaje = mensaje + "\n  *"+ cancion[3]+ " ("+str(cancion[1])+")"
    sendMessage(id_user,mensaje)
    mensaje=""
    
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
dp.add_handler(CommandHandler("addtolist", addtolist))
dp.add_handler(CommandHandler("play", play))
dp.add_handler(CommandHandler("playr", playr))
dp.add_handler(CommandHandler("deleteplaylist", deleteplaylist))
dp.add_handler(CommandHandler("rmfromlist", removefromlist))
dp.add_handler(CommandHandler("listplaylists", listplaylists))
dp.add_handler(CommandHandler("post_author", post_author))
dp.add_handler(CommandHandler("help", help))



updater.start_polling()

updater.idle()

