#!/usr/bin/python
import psycopg2
from config import config

def INSERT_SONG(p_message_id, p_tag):
    # creación cursor
    conn = None
    # read connection parameters
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

def Buscar_Message_id_and(param):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    #param = 'anime', 'opening'
    cursor.execute("SELECT DISTINCT ON (message_id) * FROM (SELECT * FROM public.songs where (lower(TRIM(tag)) IN ("+param+"))) as busqueda1 WHERE(message_id) IN(SELECT message_id FROM (SELECT * FROM public.songs where (lower(TRIM(tag)) IN ("+param+"))) as busqueda GROUP BY message_id HAVING count(*)>1)")
    return cursor

#if __name__ == '__main__':
#    connect()

