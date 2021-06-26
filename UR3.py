import socket
import time
import struct
import codecs
import sintetizador

def transmission_f(instruction):
  # Echo client program
  HOST = "192.168.0.100" # ip del robot
  PORT = 30002 # puerto en el que el robot recibe
  PORT_30003 = 30003
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crear un socket
  s.connect((HOST, PORT)) #iniciar la comunicacion

  co =  str.encode(instruction)+b"\n"
  s.send (co)
  data = s.recv(1024)
  s.close()

def transmission(instruction):
  transmission_f(instruction)
  #print(instruction)

def transmis_move(pos):
  """
  https://matthew-brett.github.io/teaching/string_formatting.html
  """
  if (pos[0] != 'p'):
    string="movej([{},{},{},{},{},{}],a={},v={})".format(pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7],pos[8])
  else:
    string="movej(p[{},{},{},{},{},{}],a={},v={})".format(pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7],pos[8])
  transmission(string)

def receive_f():
  # -*- coding: utf-8 -*-
  # Echo client program
  HOST = "192.168.0.100" # ip del robot
  PORT = 30002 # puerto en el que el robot recibe
  PORT_30003 = 30003
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crear un socket
  s.connect((HOST, PORT)) #iniciar la comunicacion
  count = 0
  home_status = 0
  program_run = 0
  while (count<1):
    if program_run == 0:
      try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((HOST, PORT_30003))
        time.sleep(1.00)
        #print ""
        packet_1 = s.recv(4)
        packet_2 = s.recv(8)
        packet_3 = s.recv(48)
        packet_4 = s.recv(48)
        packet_5 = s.recv(48)
        packet_6 = s.recv(48)
        packet_7 = s.recv(48) 
        packet_8 = s.recv(48)
        packet_9 = s.recv(48)
        packet_10 = s.recv(48)
        packet_11 = s.recv(48)
        
        packet_12 = s.recv(8)
        x = struct.unpack('!d',packet_12)[0]
        #print ("X = ", x * 1000)
        
        packet_13 = s.recv(8)
        y = struct.unpack('!d', packet_13)[0]
        #print ("Y = ", y * 1000)
        
        packet_14 = s.recv(8)
        z = struct.unpack('!d', packet_14)[0]
        #print ("Z = ", z * 1000)
        
        packet_15 = s.recv(8)
        Rx = struct.unpack('!d', packet_15)[0]
        #print ("Rx = ", Rx)
        
        packet_16 = s.recv(8)
        Ry = struct.unpack('!d', packet_16)[0]
        #print ("Ry = ", Ry)
        
        packet_17 = s.recv(8)
        Rz = struct.unpack('!d', packet_17)[0]
        #print ("Rz = ", Rz)
        
        home_status = 1
        program_run = 0
        s.close()
      except socket.error as socketerror:
        print("Error: ", socketerror)
      #print ("received{count}: \t x={x},y={y},z={z},Rx={Rx},Ry={Ry},Rz={Rz}")
      count=count+1
  return [x,y,z,Rx,Ry,Rz]

def receive():
  return receive_f() #unquote for real receive

def move(x,y,z):
  print(receive())
  #time.sleep(1)
  punto=receive()
  curve=['p','x','y','z','Rx','Ry','Rz', 1, 1]
  curve[1]=punto[0]+x*0.01       # BACK (-x) FRONT (+x)  convierte a milimetros
  curve[2]=punto[1]+y*0.01       # RIGHT (+y) LEFT (-y)
  curve[3]=punto[2]+z*0.01       # UP (+z) DOWN (-z)
  curve[4]=punto[3]       # 1° = 0.017444444
  curve[5]=punto[4]
  curve[6]=punto[5]
  
  if ( curve[1]<0.100 or curve[1]>0.450 or curve[2]<-0.292 or curve[2]>0.307 or curve[3]<0.088 or curve[3]>0.288 ):
    sintetizador.hablar("El punto solicitado está por fuera del área de trabajo, por favor ingresar un movimiento dentro del área de trabajo")
  else:
    transmis_move(curve.copy())
    time.sleep(2)
    curve = receive()
    if ( round(punto[0],3) == round(curve[0],3) and round(punto[1],3) == round(curve[1],3) and round(punto[2],3) == round(curve[2],3) ):
      sintetizador.hablar("Movimiento inválido, por favor ingresar un movimiento válido")
    else:  
      if x>0:
        if x == 1:
          sintetizador.hablar("Me moví hacia adelante un centímetro")
        else:
          sintetizador.hablar("Me moví hacia adelante "+str(x)+"cm")
      if x<0:
        if x == -1:
          sintetizador.hablar("Me moví hacia atrás un centímetro")
        else:
          sintetizador.hablar("Me moví hacia atrás "+str(abs(x))+"cm")
      if y>0:
        if y == 1:
          sintetizador.hablar("Me moví hacia tu derecha un centímetro")
        else:
          sintetizador.hablar("Me moví hacia tu derecha "+str(y)+"cm")
      if y<0:
        if y == -1:
          sintetizador.hablar("Me moví hacia tu izquierda un centímetro")
        else:
          sintetizador.hablar("Me moví hacia tu izquierda "+str(abs(y))+"cm")
      if z>0:
        if z == 1:
          sintetizador.hablar("Me moví hacia arriba un centímetro")
        else:
          sintetizador.hablar("Me moví hacia arriba "+str(z)+"cm")
      if z<0:
        if z == -1:
          sintetizador.hablar("Me moví hacia abajo un centímetro")
        else:
          sintetizador.hablar("Me moví hacia abajo "+str(abs(z))+"cm")
  #print("Exit Detect")
  #time.sleep(4)
  print(receive())

def open_Gripper():
  HOST = "192.168.0.100" # The UR IP address
  PORT = 30002 # UR secondary client
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))

  f = open ("Gripper.open", "rb")   #Robotiq Gripper

  l = f.read(1024)
  while (l):
      s.send(l)
      l = f.read(1024)
  s.close()

def close_Gripper():
  HOST = "192.168.0.100" # The UR IP address
  PORT = 30002 # UR secondary client
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))

  f = open ("Gripper.close", "rb")   #Robotiq Gripper

  l = f.read(1024)
  while (l):
      s.send(l)
      l = f.read(1024)
  s.close()

def half_Gripper():
  HOST = "192.168.0.100" # The UR IP address
  PORT = 30002 # UR secondary client
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))

  f = open ("Gripper.half", "rb")   #Robotiq Gripper

  l = f.read(1024)
  while (l):
      s.send(l)
      l = f.read(1024)
  s.close()

def activate_Gripper():
  HOST = "192.168.0.100" # The UR IP address
  PORT = 30002 # UR secondary client
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))

  f = open ("Gripper.activate", "rb")   #Robotiq Gripper

  l = f.read(1024)
  while (l):
      s.send(l)
      l = f.read(1024)
  s.close()
