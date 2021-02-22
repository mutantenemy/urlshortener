# URLSHORTENER

_Este programa usa PYTHON para acortar URLs._


## Requerimientos
El proyecto está pensado para ejecutarlo en un servidor Linux.

La página y la lógica requiere **PYTHON 3.8.6 64-bit**, **flask**, **flask_wtf**

El _bot.py_ para testear el tiempo de creación, requiere **PYTHON 3.8.6 64-bit** y **Mechanize**

Existe un _dockerfile_ para crear una imagen. Ver la seccion de Docker


## Cómo usar la página:
La página poseé un campo de texto y dos botones para ejecutar sus funciones, _Transform_ y _Remove_.

Al ingresar un destino fuera de este dominio, se genera e imprime un link que permite a los usuarios utilizarlo como proxy del destino real.

Si lo que se ingresa es un destino remoto ya guardado o un link local aún vigente, abajo se imprime el vinculo respectivo.

Si lo que se ingresa no es válido o es un vinculo ya removido, aparece un mensaje de error.

También es posible remover vinculos. Si se ingresa tanto el link local como el destino remoto y se remueve, la informacion de ese vinculo es eliminado.
Si la página descripta no corresponde a un vinculo en funcionamiento, aparece un mensaje de error.

También es posible ver el contenido guardado en disco de los datos guardados visitando _localhost/debug/json_.


## Breve repaso de los archivos:
PYTHON:
**main.py** > Main va a crear la página y administrar la mayoria de la lógica.
**fileManager.py** > Esto se ocupa de escribir los datos al disco.
**encoder.py** > Esto genera el código para los vinculos locales.
**urlData.py** > Esto serializa los vinculos creados como arrays.
**forms.py** > Esto se ocupa de generar el formulario con _jinja_.

HTML:
**index.html** > Index presenta el formulario y otros datos generados en _main.py_
**json.html** Está página se utliza para poder revisar _dict.json_ desde la web.(Se accede mediante _localhost/debug/json_)

ARCHIVOS AUTOGENERADOS:
**dict.json** > Este archivo almacena el proximo al último indice usado, los vinculos creados y su metadata.
**logs.log** > Este archivo presenta los logs que ocurren durante la ejecución. (Se borran cada vez que se lanza el server)

PYTHON NO INTEGRADO O DE ASISTENCIA:
**bot.py** > Este programa se útiliza para crear cualquier cantidad de vinculos en poco tiempo y saber cuanto demoró.
**tables.py** > Esta clase se iba a utilizar para generar tablas HTML para mostrar los metadatos en index.
**logger.py** > Este archivo guarda el formato en el que el logger funciona.
**orchestrator.py** > Esta clase se iba a ocupar monitorear los recursos para optimizar la ejecucion del programa.


## Cómo funciona el backend de la página:

### Arranque
El programa arranca desde _main.py_ y desde acá hace la configuración inicial.

Primero se revisa si el archivo que contiene los logs "_logs.log_" existe y de ser así borra su contenido.
Si el archivo no existe, crea uno nuevo.

Luego intenta leer el archivo _dict.json_ que guarda en disco el siguiente del ultimo index utilizado y la información completa de todos los vinculos generados aún validos.
Si el archivo no existe, crea uno nuevo con un index de 1.

Finalmente entra en un loop para mantener la página corriendo en 0.0.0.0:80 y en debug por si se hacen cambios en runtime


### Validar el texto ingresado
El texto ingresado es validado en el archivo _forms.py_ por las herramientas que entrega **Flask**.
Flask y wtforms poseén herramientas propias para revisar que lo ingresado es una URL. Es por esto que el texto debe ser _https://domain.any:port/whatever_.

Esto en el futuro podria ser reemplazdo por un REGEX que permita obviar el protocolo o utilizar direcciones IP, pero hasta tanto, esta es una solución agil y barata.

### Transformar una nueva URL

La transformación la administra _main.py_. Cada vez que se valida una URL exitosamente, se pregunta si es que la página ingresada es local o externa y si se encuentra o no registrada.

Si el destino es remoto y no está registrado, se le pide a _encoder.py_ que genere un nuevo ID (en base 62) para vincular ambas páginas. Luego, se crea un objeto _URLData_ para serializar el vinculo en un array junto a la cantidad de entradas que tuvo el link, la fecha creada y la ultima fecha utilizada. Este método permite serializar cualquier metadato nuevo.

Una vez que se genera el nuevo link local, se vincula en un diccionario el código junto al array y se guarda en disco bajo el archivo dict.json.

Finalmente se le imprime al usuario el vinculo generado.


### Obtener la URL local apartir de un destino remoto
La transformación la administra _main.py_. Cada vez que se valida una URL exitosamente, se pregunta si es que la pagina ingresada es local o externa y si se encuentra o no registrada.

Si el destino es remoto y está registrado, se revisa entre los vinculos ya generados que código le corresponde.

Finalmente se le imprime al usuario el vinculo generado.


### Obtener el destino apartir de una URL local
La transformación la administra _main.py_. Cada vez que se valida una URL exitosamente, se pregunta si es que la pagina ingresada es local o externa y si se encuentra o no registrada.

Si el destino ingresado pertenece a nuestra página, se revisa si su código aún es valido. De ser así, facilmente obtenemos el destino real consultando al diccionario.


### Utilizar una URL generada
Al intentar abrir una URL generada valida, _main.py_ actualiza su metadata incrementando la cantidad de llamadas y su útlimo uso. Luego redirige al usuario a la página vinculada sin interrupción.

Si la URL es de dominio local pero no corresponde a ninugn vinculo activo, el usuario es llevado automaticamente al index.


### Quitar un vinculo
El remover un vinculo es administrado por _main.py_. Al intentar remover una direccion, se consulta si es parte o no del diccionario ya existente.

Si la información ingresada pertenecía a un link local o link externo ya registrado, se lo quita del diccionario y se guarda en disco la accion.

Finalmente se le muestra al usuario un mensaje de exito o fracaso en la accion.


## Cómo ver los datos guardados en _dict.json_
Se puede acceder a los datos guardados en disco entrando a _localhost/debug/json_


## BOT
El bot actualmente funciona únicamente para intentar generar nuevos links. Se elije el tamaño del loop que se quiere realizar y le ingresa a la página un dominio remoto "_http://[i].com_"

Despues de esto, el bot escupe cuanto tiempo demoró en generar todos estos links.


## Docker
Para correr el programa en un container de docker, hace falta _switchear_ los campos con comentarios marcados con **FOR LOCAL TESTING** y **FOR SERVER TESTING** que se encuentran en _main.py_, _encoder.py_ y _filemanager.py_

```
if __name__ == '__main__': # SERVER DEBUG OPTIONS
    # app.run(host="0.0.0.0", port=80, debug=True) # FOR SERVER TESTING
    app.run(debug=True) # FOR LOCAL TESTING
```

```
# logging.basicConfig(filename = "/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FOR SERVER TESTING
logging.basicConfig(filename = "/home/taitz/Documents/Python/urlshortener/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FORM LOCAL TESTING
```

```
workspace = "/home/taitz/Documents/Python/urlshortener" # FOR LOCAL TESTING
# workspace = "" # FOR SERVER TESTING
```