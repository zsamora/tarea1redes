# -*- coding: utf-8 -*-
import os
import socket
import json
import argparse
import numpy as np
import time
import subprocess
import threading

# Recibe input del usuario
option = input('Eliga uno de los siguientes formatos:\n1. Comando: nombre1 direccion1 puerto1 ... nombreN direcciónN puertoN \n2. JSON: [{"nombre": "N1","direccion": "localhost","puerto": 8086},...]\n')
option = int(option)
if (option == 1):
    # Esteban
    time.sleep(5)
    #sleep(5)
if (option == 2):
    jsoninput = input('Ingrese el JSON: ')
    # Estilo JSON para server
    #[{"nombre": "N1","direccion": "localhost","puerto": 8100},{"nombre": "N2","direccion": "localhost","puerto": 8101}]
    #[{"nombre": "N1","direccion": "localhost","puerto": 8120}]
    x = json.loads(jsoninput)
    servers = {}
    for i in range(0,len(x)):
        nombre =  x[i]['nombre']
        direccion = x[i]['direccion']
        puerto = str(x[i]['puerto'])
        #serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #args = ('./server/server', puerto)
        #servers[nombre] = puerto
        #subprocess.call(cmd)
        args = ('telnet', direccion, puerto)
         #= subprocess.Popen(args, stdout=subprocess.PIPE)
        #t = threading.Thread(target=subprocess.Popen, args=(args,))#stdout=subprocess.PIPE,))
        servers[nombre] = threading.Thread(target=subprocess.Popen, args=(args,))
        #popen.wait()
        #output = popen.stdout.read()
        #print(popen.stdout)
        #print (popen.socket(socket.AF_INET, socket.SOCK_STREAM))
        #time.sleep(5)
        # Setea el socket como Non-Blocking
        #serversocket.setblocking(0)
        # Creamos un socket visible para direccion en el puerto indicado
        # Visible para el exterior en puerto X -> serversocket.bind((socket.gethostname(), X))
        # Visible para ambos en puerto X       -> s.bind(('', X))
        #serversocket.bind((direccion, puerto))
        # Volvemos al socket un server socket de 5 conexiones
        #serversocket.listen(5)
        # TODO: condicion de nombres iguales

# Loop del server
while True:
    # Obtenemos los mensajes de la conexion y la direccion
    #print(servers)
    cmd = input("Comando: ")
    cmds = cmd.split()
    if (len(cmds) <= 1):
        print("Ingrese un comando válido")
    else:
        if (cmds[0] != "ls"):
            print("Comando invalido, ingrese nuevamente")
        else:
            if (cmds[1] == "all"):
                print("Hablar a todes")
            else:
                for c in cmds[1:]:
                    print(servers[nombre].start())
                    #subprocess.Popen(('ls'), stdout=subprocess.PIPE)
                    #result = subprocess.run(['telnet','localhost',servers[c]], stdout=subprocess.PIPE)
                    #tcon = "telnet localhost " + servers[c]
                    #os.popen(tcon)
                    #result = os.popen(cmds[0])
                    #print(result.stdout)

    #print(cmd)
        #connection, address = servers[s].accept()
        #buf = connection.recv(64)
        #if len(buf) > 0:
            # mostramos lo que nos llegó y salimos del loop
        #    print(buf)
    # Obtenemos los datos recibidos en el buffer (64 bits)
    #ct = client_thread(clientsocket)
    #ct.run()
        #ready_to_read, ready_to_write, in_error = \
           #select.select(
              #potential_readers,
              #potential_writers,
              #potential_errs,
              #timeout)

    ## Condicion para cerrar el server (close)
