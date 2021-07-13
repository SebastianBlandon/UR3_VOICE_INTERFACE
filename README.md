# UR3_VOICE_INTERFACE

En este repositorio se encuentra alojada la implementacion de una interfaz de voz realizada para un brazo robotico colaborativo(Cobot) UR3, 
Para la realizacion de esta interfaz se usó el lenguaje de programación Python en su versión 3.9.5, usaron algunas librerias que se instalan
con el administrados de librerias de py, pip (version 21.1.2), para instalar cada librerias se usan los siguientes comando en el simbolo del 
sistema o cmd:

para instalar el paquete que hace el reconocimeinto de voz se usa:   pip install SpeechRecognition
para instalar el paquete que hace la sintesis de voz se usa:   pip install pyttsx3
para instalar el paquete que envia las notificaciones se usa:   pip install win10toast
**la ultima libreria (win10toast) es nativa de Windows, si tiene otro OS puede insatalas las dependencias o corra el .py que no usa esta libreria

Para poder usar el micrófono para el reconocimiento del habla en python hace falta usar la librería PyAudio la cual se instala con:   pip install PyAudio
si se presentan dificultades en la instalación de esta librería se recomienda hacer la instalación por medio de un wheel (.whl), en el siguiente enlace (https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) se encuentran los .whl de PyAudio, se debe seleccionar el .whl según la versión de Py que se este usando. 
Una vez descargado el .whl se debe ir al directorio donde se guardó y se debe hacer el uso del comando en cmd: pip install NOMBRE_DEL_ARCHIVO.whl y esperar 
a que se instale correctamente.
