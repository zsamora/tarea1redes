# -*- coding: utf-8 -*-
import socket
import json
import argparse
import numpy as np
import time
import threading
import subprocess


class myThread (threading.Thread):
    def __init__(self, threadID, name, direccion, puerto):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.direccion = direccion
        self.puerto = puerto
    def run(self):
        print ("Starting communication with: " + self.name)
        threadLock.acquire()
        connectto(self.name, self.direccion, self.puerto)
        print ("Exiting communicaction with: " + self.name)
        threadLock.release()

    def runcomm(self):
        #print ("Starting " + self.name)
        threadLock.acquire()
        getcommand(self.name)
        #print ("Exiting " + self.name)
        threadLock.release()

def connectto(threadName, direccion, puerto):
    return subprocess.call(["telnet", direccion, puerto])

def getcommand(threadName):
    return input("Comando: ")
    #threadName.exit()
    #print ("%s: %s" % (threadName, time.ctime(time.time())))

threadLock = threading.Lock()
threads = {}

# Recibe input del usuario[{"nombre": "N1","direccion": "localhost","puerto": 8120}]
option = input('Eliga uno de los siguientes formatos:\n1. Comando: nombre1 direccion1 puerto1 ... nombreN direcciónN puertoN \n2. JSON: [{"nombre": "N1","direccion": "localhost","puerto": 8086},...]\n')
option = int(option)

if (option == 1):
    # Esteban
    time.sleep(5)

if (option == 2):
    jsoninput = input('Ingrese el JSON: ')
    #[{"nombre": "N1","direccion": "localhost","puerto": 8100},{"nombre": "N2","direccion": "localhost","puerto": 8101}]
    #[{"nombre": "N1","direccion": "localhost","puerto": 8120}]
    x = json.loads(jsoninput)
    for i in range(0,len(x)):
        nombre =  x[i]['nombre']
        direccion = x[i]['direccion']
        puerto = str(x[i]['puerto'])
        threads[nombre] = myThread(i+2, nombre, direccion, puerto)

# Loop del server
while True:
    # Obtenemos los mensajes de la conexion y la direccion
    #print(servers)
    #cmd = threadc.runcomm()
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
                    print(threads[nombre].start())
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
