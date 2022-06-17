# MusicTelegramBot

***BOT QUE PERMITE ESCUCHAR MÚSICAS EN ALTA CALIDAD DE UN CANAL EN ESPECÍFICO (JPOP EN SU MAYORÍA)***:

Crea un usuario con /createuser la primera vez

Ingrese los tags a buscar en formato (/search param1 param2 ...) or (/searchall):

/search : Búsqueda de canciones que tengan todos los tags puestos.
/searchall : Búsqueda de todas las canciones que cumplan con al menos uno de los tags puestos.
/searchx : Búsqueda exacta de los parámetros que le pongas (/search param1 param2) busca canciones que el tag sea "param1" con exactitud.

**Opciones de búsqueda**:

/maxsongs: Número máximo de mensajes de respuesta (default=20).
/post_author: Persona que ha subido la canción (ver su nombre en el canal) (/post_author nombrepersona), si deseas regresar a buscar todos colocar "all".

**Opciones de lista**:

/createlist: Cree una lista con el formato (/createlist nombredelista) el nombre de la lista sin espacios.
/deletelist: Elimine una lista con el formato (/deletelist nombredelista) el nombre de la lista sin espacios(no hay backup tenga cuidado).
/addtolist: Añada canciones a la lista con el formato(/addtolist nombredelista codigo_cancion1 codigo_cancion2 ...) donde el código de canción lo ves buscando canciones con search.
/rmfromlist: Remover canciones de una lista con el formato (/rmfromlist nombredelista codigo_cancion1 codigo_cancion2 ...).
/showlists: Mostar todas tus listas
/showexlists: Mostrar listas de otras personas (/showexlists nombrepersona)

**Reproducción**:

/play: Reproducir una lista en el orden guardado con el formato (/play nombredelista).
/playr: Reproducir una lista en orden aleatorio con el formato (/playr nombredelista).
/playex: Reproducir una lista en orden aleatorio de un usuario diferente con el formato (/playex nombreusuario nombredelista).
/status: muestra tu status.
