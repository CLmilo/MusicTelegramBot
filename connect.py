#!/usr/bin/python
from http.server import executable
import psycopg2
from config import config
from telethon import TelegramClient

def INSERT_SONG(p_message_id, p_tag):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    # Insercción de datos
    sql="insert into public.songs(message_id, tag) values (%s,%s)"
    datos = (p_message_id, p_tag)
    cursor.execute(sql, datos)
    conn.commit()

def INSERT_NAME_SONG(p_message_id, p_name):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    # Insercción de datos
    sql="insert into public.name_songs(message_id, name_song) values (%s,%s)"
    datos = (p_message_id, p_name)
    cursor.execute(sql, datos)
    conn.commit()

def Buscar_Message_id_or(param):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    #param = 'anime', 'opening'
    cursor.execute("SELECT distinct on (message_id) * FROM public.songs where lower(TRIM(tag)) in ("+param+")")
    return cursor

def Buscar_Message_id_and(param,cant):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    #param = 'anime', 'opening'
    #cursor.execute("SELECT RANDOM() as random, message_id FROM (SELECT * FROM public.songs where (lower(TRIM(tag)) IN ("+param+"))) as busqueda GROUP BY message_id HAVING count(*)>"+cant+"order by random")
    cursor.execute("SELECT RANDOM() AS random, * from(SELECT message_id FROM (SELECT * FROM public.songs where (lower(TRIM(tag)) IN ("+param+"))) as busqueda group by message_id having count(message_id)>"+cant+") as busqueda2 order by random")
    return cursor

def Create_user(p_user_id,p_nombre_user, maxsong=20, post_author='all'):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql="insert into public.users(id_user,nombre_user, max_song, post_author) values (%s,%s,%s,%s)"
    datos = (p_user_id, p_nombre_user, maxsong, post_author)
    cursor.execute(sql, datos)
    conn.commit()

def Create_list(p_user_id, p_nombre_lista):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql="insert into public.lists(id_user,nombre_lista) values (%s,%s)"
    datos = (p_user_id, p_nombre_lista)
    cursor.execute(sql, datos)
    conn.commit()
    return cursor

def Obtain_id_list(p_user_id, p_nombre_lista):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("Select * from public.lists where (id_user='"+p_user_id+"' and nombre_lista = '"+p_nombre_lista+"')")
    for message in cursor:
        id_lista = message[0]
    return id_lista

def Add_to_list(p_id_lista, message_id):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql="insert into public.songs_list(id_lista,message_id) values (%s,%s)"
    datos = (p_id_lista, message_id)
    cursor.execute(sql, datos)
    conn.commit()

def Modify_post_author(p_id_user, p_post_author):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql="update public.users set post_author = (%s) where id_user = (%s)"
    datos = (p_post_author, p_id_user)
    cursor.execute(sql, datos)
    conn.commit()

def Modify_max_song(p_id_user, p_max_song):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("update public.users set max_song = "+p_max_song+" where id_user ='"+p_id_user+"'")
    conn.commit()

def Get_max_song(p_id_user):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql = "Select * from public.users where id_user = '"+p_id_user+"'"
    cursor.execute(sql)
    return cursor

def Get_post_author(p_id_user):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("SELECT post_author from public.users where id_user ='"+p_id_user+"'")
    return cursor

def Get_userlists(p_id_user):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("select * from public.lists where id_user ='"+p_id_user+"'")
    return cursor

def Get_songs_in_list(p_id_list):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("select * from public.songs_list, public.name_songs where (songs_list.id_lista ='"+p_id_list+"' and songs_list.message_id=name_songs.message_id)")
    return cursor

def List_Song(p_messages_id):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    #p_messages_id = '1','2','3','4'
    cursor.execute("select * from public.songs where id_lista in ("+p_messages_id+")")
    return cursor

def Get_playlist(p_id_list):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("select * from public.songs_list where id_lista ='"+p_id_list+"'")
    return cursor

def Get_playlistr(p_id_list):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("select random() as random, * from public.songs_list where id_lista ='"+p_id_list+"' order by random")
    return cursor

def Delete_playlist(p_id_list):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql="Delete from public.songs_list where id_lista = %s"
    datos = (p_id_list)
    cursor.execute(sql, datos)
    conn.commit()
    sql="Delete from public.lists where id_lista = %s"
    datos = (p_id_list)
    cursor.execute(sql, datos)
    conn.commit()
    return(cursor)

def Delete_song_in_playlist(p_id_list, message_id):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql="Delete from public.songs_list where (id_lista = %s and message_id = %s)"
    datos = (p_id_list ,message_id)
    cursor.execute(sql, datos)
    conn.commit()

# ACTUALIZACIÓN DE DATOS MANUAL
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

def Inserccion_forzada_canciones():
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("drop table songs")
    conn.commit()
    cursor.execute("create table songs(id_tag SERIAL,message_id VARCHAR(10), tag VARCHAR(100))")
    conn.commit()
    for message in client.iter_messages(group_username, reverse=True):
        owner_name = "name="+ str(message.post_author) 
        INSERT_SONG(message.id,owner_name)
        for tag in str(message.text).split('#'):
            if (tag!=""):
                INSERT_SONG(message.id,tag) 
def Inserccion_forzada_nombres_canciones():
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("drop table name_songs")
    conn.commit()
    cursor.execute("create table name_songs(message_id NUMERIC(9) PRIMARY KEY,name_song VARCHAR(100))")
    conn.commit()
    for message in client.iter_messages(group_username, reverse=True):
        try:
            name_song=str(message.media.document.attributes[0].performer)+" - " + str(message.media.document.attributes[0].title)
            INSERT_NAME_SONG(message.id,name_song)
        except:
            print("error")
            pass


def hard(input):
    input = input.replace("-","")
    input = input.replace("'","")
    input = input.replace("?","")
    input = input.replace("=","")
    input = input.replace('"',"")
    return input

#if __name__ == '__main__':
#    connect()

