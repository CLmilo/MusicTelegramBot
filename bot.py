import time
import json
from sqlite3 import paramstyle
import requests
import re
from config import config
import telegram
from telegram.ext import Updater, CommandHandler
from connect import Buscar_Message_id_and_exacto, Get_external_user_info, Get_user_info, hard, Add_to_list, Buscar_Message_id_and, Buscar_Message_id_or, Create_user, Create_list, Delete_playlist, Delete_song_in_playlist, Get_playlistr, Get_songs_in_list, Get_userlists, Modify_max_song, Modify_post_author, Obtain_id_list, Get_playlist
import os

with open('.token') as file:
    lista = file.readlines()
    TOKEN = lista[0].rstrip("\n")
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
    /searchx : Búsqueda exacta de los parámetros que le pongas (/search param1 param2) busca canciones que el tag sea "param1" con exactitud.
    Opciones de búsqueda:
    /maxsongs: Número máximo de mensajes de respuesta (default=20). 
    /post_author: Persona que ha subido la canción (ver su nombre en el canal) (/post_author nombrepersona), si deseas regresar a buscar todos colocar "all".
    Opciones de lista:
    /createlist: Cree una lista con el formato (/createlist nombredelista) el nombre de la lista sin espacios.
    /deletelist: Elimine una lista con el formato (/deletelist nombredelista) el nombre de la lista sin espacios(no hay backup tenga cuidado).
    /addtolist: Añada canciones a la lista con el formato(/addtolist nombredelista codigo_cancion1 codigo_cancion2 ...) donde el código de canción lo ves buscando canciones con search.
    /rmfromlist: Remover canciones de una lista con el formato (/rmfromlist nombredelista codigo_cancion1 codigo_cancion2 ...).
    /showlists: Mostar todas tus listas
    /showexlists: Mostrar listas de otras personas (/showexlists nombrepersona) 
    Reproducción:
    /play: Reproducir una lista en el orden guardado con el formato (/play nombredelista).
    /playr: Reproducir una lista en orden aleatorio con el formato (/playr nombredelista).
    /playex: Reproducir una lista en orden aleatorio de un usuario diferente con el formato (/playex nombreusuario nombredelista).
    /status: muestra tu status.
    """)

def atajos(update, context):
    id_chat = update.effective_user['id']
    sendMessage(id_chat, """ ATAJOS:
    /sr : /search
    /sra : /searchall
    /srx : /searchx
    /ms: /maxsongs
    /pa: /post_author
    /cl: /createlist
    /dl: /deletelist
    /atl: /addtolist
    /rfl: /rmfromlist
    /sl: /showlists
    /sel: /showexlists
    /p: /play
    /pr: /playr
    /pex: /playex
    /st: /status
    """)

def createuser(update,context):
    chat_id = update.effective_user['id']
    lastname = str(update.effective_user['last_name'])
    if lastname == "None":
        lastname = ""
    nombre = hard(str(update.effective_user['first_name'])+lastname).strip()
    try:
        Create_user(chat_id, nombre)
        sendMessage(chat_id, "Usuario creado con éxito")
    except:
        sendMessage(chat_id, "Usuario no creado, mandar mensaje a https://t.me/Cl_Milo") 

def createlist(update,context):
    chat_id = update.effective_user['id']
    name_list = hard(str(update.message['text'].split(" ")[1]))
    try:
        Create_list(chat_id,name_list)
        sendMessage(chat_id, "Lista creada con el nombre "+name_list) 
    except:
        sendMessage(chat_id, "Lista no creada, mandar mensaje a https://t.me/Cl_Milo") 

def addtolist(update,context):
    user_id = str(update.effective_user['id'])
    mensaje = update.message['text'].split(" ")
    name_list = str(hard(str(mensaje[1])))
    id_lista = str(Obtain_id_list(user_id,name_list))
    lista_mensajes = []
    for message_id in mensaje:
        lista_mensajes.append(str(hard(message_id)))
    try:
        lista_mensajes.remove("/addtolist")
    except:
        lista_mensajes.remove("/atl")
    lista_mensajes.remove(name_list)
    mensaje_enviar = ""
    for message_id in lista_mensajes:
        mensaje_enviar += str(Add_to_list(id_lista, message_id)) + "\n"
        print(mensaje_enviar)
    
    sendMessage(user_id,mensaje_enviar)

def removefromlist(update,context):
    id = str(update.effective_user['id'])
    mensaje = update.message['text'].split(" ")
    name_list = str(hard(str(mensaje[1])))
    id_lista = str(Obtain_id_list(id,name_list))
    lista_mensajes = []
    for message_id in mensaje:
        lista_mensajes.append(str(hard(message_id)))
    try:
        lista_mensajes.remove("/rmfromlist")
    except:
        lista_mensajes.remove("/rfl")
    lista_mensajes.remove(name_list)
    for message_id in lista_mensajes:
        Delete_song_in_playlist(id_lista, message_id)

def searchall(update,context):
    lista_tag=[]
    chat_id = update.effective_user['id']
    caption_mensaje_actual = update.message['text'].split(" ")
    for tag in caption_mensaje_actual:
        lista_tag.append(str(hard(tag.lower())))
    table_info_user = Get_user_info(str(chat_id))
    for num in table_info_user:
        max_songs = int(num[2])
        post_author = "name=" + str(num[3]).strip().lower()    
    if post_author == "name=all":
        pass
    else:
        lista_tag.append(post_author)
    try:
        lista_tag.remove("/searchall")
    except:
        lista_tag.remove("/sra")
    param = re.sub("\[|\]","",str(lista_tag))
    try:
        cursor = Buscar_Message_id_or(param).fetchmany(max_songs)
        for message_id in cursor:
            copyMessage(message_id[1],chat_id)
            sendMessage(chat_id, "Código de Canción : "+str(message_id[1]))
        lista_tag=[]
    except:
        sendMessage(chat_id,"No hay resultados")


def search(update,context):
    lista_tag=[]
    chat_id = update.effective_user['id']
    caption_mensaje_actual = update.message['text'].split(" ")
    for tag in caption_mensaje_actual:
        lista_tag.append(str(hard(tag.lower())))
    table_info_user = Get_user_info(str(chat_id))
    for num in table_info_user:
        max_songs = int(num[2])
        post_author = "name=" + str(num[3]).strip().lower()    
    if post_author == "name=all":
        pass
    else:
        lista_tag.append(post_author)
    try:
        lista_tag.remove("/search")
    except:
        lista_tag.remove("/sr")
    try:
        cursor = Buscar_Message_id_and(lista_tag).fetchmany(max_songs)
        for message_id in cursor:
            copyMessage(message_id[1],chat_id)
            sendMessage(chat_id, "Código de Canción : "+str(message_id[1]))
        lista_tag=[]
    except:
        sendMessage(chat_id,"No hay resultados")
    

def searchexacto(update,context):
    lista_tag=[]
    chat_id = update.effective_user['id']
    caption_mensaje_actual = update.message['text'].split(" ")
    for tag in caption_mensaje_actual:
        lista_tag.append(str(hard(tag.lower())))
    table_info_user = Get_user_info(str(chat_id))
    for num in table_info_user:
        max_songs = int(num[2])
        post_author = "name=" + str(num[3]).strip().lower()    
    if post_author == "name=all":
        pass
    else:
        lista_tag.append(post_author)
    try:
        lista_tag.remove("/searchx")
    except:
        lista_tag.remove("/srx")
    cant = len(lista_tag) -1 
    param = re.sub("\[|\]","",str(lista_tag))
    cursor = Buscar_Message_id_and_exacto(param,str(cant)).fetchmany(max_songs)
    if (cursor==""):
        sendMessage(chat_id,"No hay resultados")
    for message_id in cursor:
        copyMessage(message_id[1],chat_id)
        sendMessage(chat_id, "Código de Canción : "+str(message_id[1]))
    lista_tag=[]

def maxsongs(update,context):
    id_user = str(update.effective_user["id"])
    nuevo_max = str(hard(str((update.message['text'].split(" ")[1]))))
    Modify_max_song(id_user, nuevo_max)

def post_author(update,context):
    id_user = str(update.effective_user["id"])
    mensaje = str(hard(str(update.message['text'])))
    if mensaje[0:3]=="/pa":
        post_author = mensaje[3:]
    else :
        post_author = str(hard(str(update.message['text'])[13:]))
    Modify_post_author(id_user,post_author)

def play(update,context):
    id_user = str(update.effective_user["id"])
    name_playlist = str(hard(str(update.message["text"].split(" ")[1])))
    id_list = str(Obtain_id_list(id_user, name_playlist))
    table_info_user = Get_user_info(str(id_user))
    for num in table_info_user:
        max_songs = int(num[2])
    cursor = Get_playlist(id_list).fetchmany(max_songs)
    for message_id in cursor:
        copyMessage(message_id[1], id_user)
        sendMessage(id_user, "Código de Canción : " + str(message_id[1]))

def playr(update,context):
    id_user = str(update.effective_user["id"])
    name_playlist = str(hard(str(update.message["text"].split(" ")[1])))
    id_list = str(Obtain_id_list(id_user, name_playlist))
    table_info_user = Get_user_info(str(id_user))
    for num in table_info_user:
        max_songs = int(num[2])
    cursor = Get_playlistr(id_list).fetchmany(max_songs)
    for message_id in cursor:
        copyMessage(message_id[2], id_user)
        sendMessage(id_user, "Código de Canción : " + str(message_id[2]))

def searchexternallist(update,context):
    id_user = str(update.effective_user["id"])
    name_external_user = str(hard(str(update.message["text"].split(" ")[1])))
    datos = Get_external_user_info(name_external_user)
    for linea in datos:
        id_user_external = linea[0]
    listas = Get_userlists(id_user_external)
    mensaje= "Las listas existentes son: "
    for lista in listas:
        mensaje += "\n*"+lista[1]
    sendMessage(id_user,mensaje)
    mensaje=""

def playexternallist(update,context):
    id_user = str(update.effective_user["id"])
    name_external_user = str(hard(str(update.message["text"].split(" ")[1])))
    name_playlist = str(hard(str(update.message["text"].split(" ")[2])))
    datos = Get_external_user_info(name_external_user)
    for linea in datos:
        id_user_external = linea[0]
    id_list = str(Obtain_id_list(id_user_external, name_playlist))
    table_info_user = Get_user_info(str(id_user))
    for num in table_info_user:
        max_songs = int(num[2])
    try :
        cursor = Get_playlistr(id_list).fetchmany(max_songs)
        for message_id in cursor:
            copyMessage(message_id[2], id_user)
            sendMessage(id_user, "Código de Canción : " + str(message_id[2]))
    except:
        sendMessage(id_user, "No existe la lista")

def deleteplaylist(update,context):
    id_user = str(update.effective_user["id"])
    name_playlist = str(hard(str(update.message["text"].split(" ")[1])))
    id_list = str(Obtain_id_list(id_user, name_playlist))
    print(id_user + name_playlist + id_list)
    cursor = Delete_playlist(id_list)
    

def listplaylists(update,context):
    id_user = str(update.effective_user["id"])
    listas = Get_userlists(id_user)
    for lista in listas:
        mensaje = ""
        canciones = Get_songs_in_list(str(lista[0]))
        mensaje += "\n((-)) "+str(lista[1])+ " contiene: "
        for cancion in canciones:
           mensaje += "\n    *"+ cancion[3]+ " ("+str(cancion[1])+")"
        sendMessage(id_user,mensaje)

def status(update,context):
    id_user = str(update.effective_user["id"])
    datos = Get_user_info(id_user)
    for linea in datos:
        nombre_user = str(linea[1])
        max_songs = str(linea[2])
        post_author = str(linea[3])
    mensaje = "Nombre de Usuario: "+nombre_user+" \nCantidad máxima de songs: "+max_songs+" \nAutor Preferencia: "+post_author
    sendMessage(id_user,mensaje)


# ACTUALIZACIÓN DE DATOS MANUAL

def update(update,context):
    id_user = str(update.effective_user["id"])
    mensaje = str(update.message["text"])
    os.system('python3 update.py')
    sendMessage(id_user,"se terminó de ejecutar")

def updatef(update,context):
    id_user = str(update.effective_user["id"])
    mensaje = str(update.message["text"])
    os.system('python3 updatef.py')
    sendMessage(id_user,"se terminó de ejecutar")

if __name__ == "__main__":
    my_bot = telegram.Bot(token = TOKEN)
    #print(my_bot.getMe())

updater = Updater(my_bot.token, use_context=True)

dp = updater.dispatcher


#Creamos los manejadores
dp.add_handler(CommandHandler("searchall", searchall))
dp.add_handler(CommandHandler("maxsongs", maxsongs))
dp.add_handler(CommandHandler("search", search))
dp.add_handler(CommandHandler("searchx",searchexacto))
dp.add_handler(CommandHandler("createuser", createuser))
dp.add_handler(CommandHandler("createlist", createlist))
dp.add_handler(CommandHandler("addtolist", addtolist))
dp.add_handler(CommandHandler("play", play))
dp.add_handler(CommandHandler("playr", playr))
dp.add_handler(CommandHandler("playex",playexternallist))
dp.add_handler(CommandHandler("deletelist", deleteplaylist))
dp.add_handler(CommandHandler("rmfromlist", removefromlist))
dp.add_handler(CommandHandler("showlists", listplaylists))
dp.add_handler(CommandHandler("post_author", post_author))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("updatef", updatef))
dp.add_handler(CommandHandler("update", update))
dp.add_handler(CommandHandler("atajos", atajos))
dp.add_handler(CommandHandler("status", status))
dp.add_handler(CommandHandler("showexlists", searchexternallist))

#Atajos
dp.add_handler(CommandHandler("sra", searchall))
dp.add_handler(CommandHandler("ms", maxsongs))
dp.add_handler(CommandHandler("sr", search))
dp.add_handler(CommandHandler("srx",searchexacto))
dp.add_handler(CommandHandler("cl", createlist))
dp.add_handler(CommandHandler("atl", addtolist))
dp.add_handler(CommandHandler("p", play))
dp.add_handler(CommandHandler("pr", playr))
dp.add_handler(CommandHandler("pex",playexternallist))
dp.add_handler(CommandHandler("dl", deleteplaylist))
dp.add_handler(CommandHandler("rfl", removefromlist))
dp.add_handler(CommandHandler("sl", listplaylists))
dp.add_handler(CommandHandler("pa", post_author))
dp.add_handler(CommandHandler("st", status))
dp.add_handler(CommandHandler("sel",searchexternallist))


updater.start_polling()

updater.idle()

