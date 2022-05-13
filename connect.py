#!/usr/bin/python
from http.server import executable
import psycopg2
from config import config

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
    cursor.execute("SELECT RANDOM() as random, message_id FROM (SELECT * FROM public.songs where (lower(TRIM(tag)) IN ("+param+"))) as busqueda GROUP BY message_id HAVING count(*)>"+cant+"order by random")
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

def Obtain_id_list(p_user_id, p_nombre_lista):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    id_lista = cursor.execute("Select id_lista from public.lists where (id_user='"+p_user_id+"' and nombre_lista = '"+p_nombre_lista+"')")
    return id_lista

def Add_to_list(p_id_lista, message_id):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    sql="insert into public.song_list(id_lista,message_id) values (%s,%s)"
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
    sql="Select max_song from public.users where id_user = (%s)"
    datos = (p_id_user)
    cursor.execute(sql, datos)
    conn.commit()
    return cursor

def Get_post_author(p_id_user):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("SELECT post_author from public.users where id_user = "+p_id_user)
    return cursor

#if __name__ == '__main__':
#    connect()

