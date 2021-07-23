##############################################
# Instalar las dependencias
# pip3 install pyaudio
# pip3 install SpeechRecognition
##############################################

import speech_recognition as sr         # Se importa la libreria y se añade una abreviatura.

def reconocer(duracion):                #Se define la función principal para realizar el reconocimiento del habla
    global r                            #Se define la variable global r
    r = sr.Recognizer()                 #A la variable r se le asignan los atributos de reconocedor
    global source                       #Se define la variable global source o fuente
    with sr.Microphone() as source:     #Con el micrófono como fuente hacer lo siguiente
        if ("None" in duracion):        #Aquí pregunta si la duración de escuha no está definida, hacer lo siguiente
            r.adjust_for_ambient_noise(source, duration = 0.5)  #Ajustar el ruido del micrófono y usar medio segundo para ajustarlo
            audio = r.listen(source,phrase_time_limit = None)   #Recibe en la variable audio lo que se escucha en el micrófono
                                                                #hasta que la persona pueda decir el comando de voz
        else:                           #Si está definida la la duración de escucha, hacer lo siguiente
            r.adjust_for_ambient_noise(source, duration = 1)   #Ajustar el ruido del micrófono y usar un segundo para ajustarlo
            audio = r.listen(source,phrase_time_limit = int(duracion))  #Recibe en la variable audio lo que se escuchó por el micrófono
                                                                        #pero una vez se active el micrófono, el programa solo usará el 
                                                                        #micrófono como fuente de adquisición de señal el tiempo definido
                                                                        #en la variable duracion
        try:                            #El programa intenta realizar una acción hasta que haya un interrupción o excepción 
            response = r.recognize_google(audio, language="es-CO")      #Se guarda en la variable response el reconocimiento de voz usando
                                                                        #el recoonocedor de google y pasandolo a español
            print("Entendi: '" + response + "'")                        #En esta linea se retroalimeta al usuario por medio de la consola
                                                                        #mostrando lo que pudo entender el programa
            return response                                             #Se retorna el valor que se haya reconocido
        except sr.UnknownValueError:                                    #Estas ultimas lineas son excepciones por si no entiende lo que se
            return 'No te entendi'                                      #dictó o si no se reconoce el audio.
        except sr.RequestError as e:
            print("GSR; {0}".format(e))
            return 'No logre reconocer ningun audio'
