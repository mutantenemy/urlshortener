# URLSHORTENER

Este programa usa PYTHON para acortar URLs.

## Requerimientos

El proyecto está pensado para ejecutarlo en un servidor UNIX.

La página y la lógica requiere **PYTHON3**, **flask**, **flask_wtf**

El _bot.py_ para testear el tiempo de creación, requiere **PYHTON3** y **Mechanize**

Existe un _dockerfile_ para crear una imagen. Ver la seccion de Docker

### Cómo usar la página:

### Cómo ver los datos guardados en _dict.json_

Se puede acceder a los datos guardados en disco entrando a **localhost:5000/debug/json**

### BOT


### Docker

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
