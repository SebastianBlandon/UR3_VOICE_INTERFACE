import UR3 # LIBRERIA PARA CONTROLAR EL ROBOT UR3, ES UN .PY
import vozatexto # LIBRERIA PARA PASAR DE VOZ A TEXTO, EN ESTE ARCHIVO SE IMPORTA LA LIBRERIA speech_recognition, LIBRERIA DE PYTHON
import sintetizador # LIBRERIA PARA DE TEXTO A VOZ, EN ESTE ARCHIVO SE IMPORTA LA LIBRERIA pyttsx3, LIBRERIA DE PYTHON
import time # SE IMPORTA LA LIBRERIA time DE PYTHON PARA HACER USO DE ALGUNOS DELAY O ESPERAS NECASARIAS PARA EL MOVIMIENTO DEL ROBOT EN ALGUNOS CASOS
##from win10toast import ToastNotifier # ESTA LIBRERIA NATIVA DE WINDOWS SIRVE PARA DAR AVISOS, NOTIFICACIONES 

duracion = "3" # ESTA VARIABLE DENOTA EL TIEMPO MAXIMO QUE ESTARÁ ENCENDIDO EL MICROFONO ESCUCHANDO A LA PERSONA QUE USARÁ LA INTERFAZ
#########################################################################################################################################
##             SE INICIALIZA LA POSICIÓN CASA O POSICIÓN INICIAL DEL ROBOT PARA INICIAR LA INTERACCION DE LA INTERFAZ                  ##
#########################################################################################################################################
posHome = ['a', 0, -1.57, -1.57, -1.57, 1.57, 1.57*2, 1, 1]  # VALORES DEL ARRAY[ tipo de move, base, hombro, codo, muñeca 3, muñeca 2, muñeca 1], LOS VALORES DE LAS ARTICULACIONES SE DEBEN PONER EN RADIANES
#########################################################################################################################################
##             SE INICIALIZA LA POSICIÓN DE DESCANSO DEL ROBOT, A ESTA POSICIÓN IRÁ EL ROBOT AL APAGARLO MEDIANTE LA INTERFAZ          ##
#########################################################################################################################################
posSleep = ['a', 0, -1.57, 0, -1.57, 0, 0, 1, 1]

##toaster = ToastNotifier() # INICIALIZACIÓN DEL NOTIFICADOR DE WINDOWS
##toaster.show_toast("Python ", 
##                   "Iniciando interfaz de voz para el UR3",
##                   duration=3) #EN ESTA LINEA ESTÁ EL CONTENIDO DE LA NOTIFICACIÓN QUE SE ENSEÑARÁ
sintetizador.hablar("Iniciando interfaz de voz para el UR3") # SE HACE LLAMADO A LA FUNCIÓN hablar() DE LA LIBRERIA sintetizador, PARA NOTOFICARLE AL USUARIO MEDIANTE VOZ. 
############################################################################################################################################
##      SE INICIALIZA UN ARREGLO DE NUMEROS QUE CONTIENE LA POSICIÓN INICIAL O POSICIÓN CASA EN COORDENADAS [ x, y, z, Rx, Ry, Rz ]       ##
positionHome = [0.2993248689227329, -0.11186165533585493, 0.13892804451129984, 2.2167085626565877, 2.221032408860887, 0.0031349267010936234]
############################################################################################################################################
positionActual = UR3.receive() # SE GUARDA EN UNA VARIABLE LA POSICIÓN REAL DEL ROBOT EN ESE MOMENTO 
if ( round(positionHome[0],3) == round(positionActual[0],3) and round(positionHome[1],3) == round(positionActual[1],3) and round(positionHome[2],3) == round(positionActual[2],3) ):
    sintetizador.hablar("EL robot ya se encuentra en la posición inicial")
else:
    sintetizador.hablar("Me estoy moviendo a la posición de inicio")
    UR3.transmis_move(posHome)
    time.sleep(5)
sintetizador.hablar("Estoy activando el grípperr o pinza")
UR3.activate_Gripper()
UR3.open_Gripper()  
UR3poweroff = 0
cantidad = []
sintetizador.hablar("Esperando los comandos que quieres usar")

while True:
    try:
        texto = ""
        ##toaster.show_toast("Python ",
        ##           "Microfono Activo",
        ##           duration=1.5)
        texto = vozatexto.reconocer(duracion).lower()
        cantidad = [int(temp)for temp in texto.split() if temp.isdigit()]
        if ("un" in texto):
            cantidad = [1]

        ########################################################################################
        ##                         COMANDO: SALIR DE LA INTERFAZ                              ##
        ########################################################################################
        
        if ("salir" in texto and "de" in texto and "la" in texto and "interfaz" in texto):
            sintetizador.hablar("Estoy saliendo de la interfaz gracias por interactuar conmigo")
            if (not UR3poweroff): 
                UR3.transmis_move(posInit)
                time.sleep(5)
            raise SystemExit

        ########################################################################################
        ##                         COMANDO: APAGAR EL ROBOT                                   ##
        ########################################################################################

        if ("apagar" in texto and "robot" in texto):
            sintetizador.hablar("Apagando el robot u r 3 del cap")
            UR3.transmis_move(posSleep)
            time.sleep(5)
            instruction = "powerdown()"
            UR3.transmission(instruction)
            UR3poweroff = 1

        ########################################################################################
        ##                         COMANDO: IR HACIA LA DERECHA                               ##
        ########################################################################################

        if ("derecha" in texto): 
            if not cantidad:
                sintetizador.hablar("repita el comando con la cantidad de centímetros a moverse")
            else:    
                UR3.move(0,cantidad[0],0)

        ########################################################################################
        ##                         COMANDO: IR HACIA LA IZQUIERDA                             ##
        ########################################################################################

        elif ("izquierda" in texto): 
            if not cantidad:
                sintetizador.hablar("repita el comando con la cantidad de centímetros a moverse")
            else:
                UR3.move(0,-cantidad[0],0)            

        ########################################################################################
        ##                         COMANDO: IR HACIA ARRIBA O SUBIR                           ##
        ########################################################################################

        elif ("arriba" in texto or "subir" in texto or "ascender" in texto or "sube" in texto): 
            if not cantidad:
                sintetizador.hablar("repita el comando con la cantidad de centímetros a moverse")
            else:
                UR3.move(0,0,cantidad[0])

        ########################################################################################
        ##                         COMANDO: IR HACIA ABAJO O BAJAR                            ##
        ########################################################################################

        elif ("abajo" in texto or "bajar" in texto): 
            if not cantidad:
                sintetizador.hablar("repita el comando con la cantidad de centímetros a moverse")
            else:
                UR3.move(0,0,-cantidad[0])

        ########################################################################################
        ##                         COMANDO: IR HACIA ATRAS                                    ##
        ########################################################################################

        elif ("atrás" in texto): 
            if not cantidad:
                sintetizador.hablar("repita el comando con la cantidad de centímetros a moverse")
            else:
                UR3.move(-cantidad[0],0,0)

        ########################################################################################
        ##                         COMANDO: IR HACIA DELANTE                                  ##
        ########################################################################################

        elif ("adelante" in texto or "delante" in texto or "frente" in texto): 
            if not cantidad:
                sintetizador.hablar("repita el comando con la cantidad de centímetros a moverse")
            else:
                UR3.move(cantidad[0],0,0)

        ########################################################################################
        ##                         COMANDO: VOLVER A CASA                                     ##
        ########################################################################################

        elif ("volver" in texto and "a" in texto and "casa" in texto): 
            sintetizador.hablar("Estoy volviendo a mi posición inicial o posición home")
            UR3.transmis_move(posHome)

        ########################################################################################
        ##                         COMANDO: ABRIR GRIPPER                                     ##
        ########################################################################################

        elif ("abrir" in texto and ("gripper" in texto or "pinza" in texto or "pinzaS" in texto)): 
            UR3.open_Gripper()
            sintetizador.hablar("Estoy abriendo la pinza o efector final")

        ########################################################################################
        ##                         COMANDO: ABRIR MEDIO EL GRIPPER                            ##
        ########################################################################################

        elif ("medio" in texto and "abrir" in texto and ("gripper" in texto or "pinza" in texto)): 
            UR3.half_Gripper()
            sintetizador.hablar("Estoy abriendo la pinza o efector final")

        ########################################################################################
        ##                         COMANDO: CERRAR GRIPPER                                    ##
        ########################################################################################

        elif ("cerrar" in texto and ("gripper" in texto or "pinza" in texto or "pinzaS" in texto)): 
            UR3.close_Gripper()
            sintetizador.hablar("Estoy cerrando la pinza o efector final")

        ########################################################################################
        ##                         COMANDO: CERRAR MEDIO EL GRIPPER                           ##
        ########################################################################################

        elif ("medio" in texto and "cerrar" in texto and ("gripper" in texto or "pinza" in texto)): 
            UR3.half_Gripper()
            sintetizador.hablar("Estoy cerrando la pinza o efector final")

        ########################################################################################
        ##                         COMANDO: MODO LIBRE (OPCIONAL)                             ##
        ########################################################################################
        # ESTE COMANDO PERMITE PONER AL ROBOT EN MODO FREEDRIVE, PERO EN ESTA VERSION DE LA    #
        # INTERFAZ SE DECIDIÓ NO PONER ESTE COMANDO POR TIEMPO Y PRUEBAS                       #
        ########################################################################################

        # elif ("modo" in texto and ("libre" in texto)): 
        #     sintetizador.hablar("Estoy en modo manejo libre o modo freedrive")
        #     modo_libre = 1
        #     while modo_libre:
        #         instruction = "freedrive_mode()"
        #         UR3.transmission(instruction)
        #         texto = ""
        #         texto = vozatexto.reconocer(duracion).lower()
        #         if "finalizar" in texto:
        #             instruction = "end_freedrive_mode()"
        #             UR3.transmission(instruction)
        #             sintetizador.hablar("El modo manejo libre o modo freedrive ha finalizado")
        #             modo_libre = 0
        # elif ("finalizar" in texto and "modo" in texto and "libre" in texto): 
        #     sintetizador.hablar("El modo manejo libre o modo freedrive ha finalizado")
        #     instruction = "end_freedrive_mode()"
        #     UR3.transmission(instruction)

        #########################################################################################
        ##                AVISO POR SI NO SE DETECTA NINGUN COMANDO ANTERIOR                   ##
        #########################################################################################

        else:
            sintetizador.hablar("No se asocío ningún comando de voz, por favor repita el comando")
    except Exception as e:
        print('Ocurrio un error', e)
