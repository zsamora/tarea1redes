# -*- coding: utf-8 -*-
import socket
import json
import argparse
import numpy as np
import time
import threading
import subprocess
import telnetlib

class myThread (threading.Thread):
    def __init__(self, name, direccion="", puerto=""):
        threading.Thread.__init__(self)
        self.name = name
        self.direccion = direccion
        self.puerto = puerto
        self.tn = 0

    def connect(self,direccion,puerto):
        print ("Starting communication with: " + self.name)
        self.tn = telnetlib.Telnet(self.direccion, self.puerto)
        #self.tn.timeout = 10
        #self.tn.read_until(b"Comando: ")
        #threadLock.acquire()
        #i = self.tn.expect(PromptLogin)
        #print (i)
        #self.conn = subprocess.run(["telnet", direccion, puerto], stdout=subprocess.PIPE)
        #print (self.conn.stdout.decode('utf-8'))
        #threadLock.release()

    def sendls(self):
        print ("Sending ls to: " + self.name)
        #threadLock.acquire()
        ## Escribe ls al thread
        self.tn.write(b"ls")
        #print ("Exiting " + self.name)
        #threadLock.release()
    def receivemsg(self):
        ## Cuando este listo imprima
        print("")

#def connectto(threadName, direccion, puerto):
    #return subprocess.call(["telnet", direccion, puerto])

def getcommand(threadName):
    return input("Comando: ")
    #threadName.exit()
    #print ("%s: %s" % (threadName, time.ctime(time.time())))

threadLock = threading.Lock()
threads = {}
threadc = myThread("Comando")

# Recibe input del usuario   [{"nombre": "N1","direccion": "localhost","puerto": 8120}]
option = input('Eliga uno de los siguientes formatos:\n1. Comando: nombre1 direccion1 puerto1 ... nombreN direcciónN puertoN \n2. JSON: [{"nombre": "N1","direccion": "localhost","puerto": 8086},...]\n')
option = int(option)

if (option == 1):
    info_servidores = input('Ingresar comando: ')
    lista_servidores = info_servidores.split(' ')
    for i in range (0, len(lista_servidores), 3):
        nombre = str(lista_servidores[i])
        direccion = str(lista_servidores[i+1])
        puerto = str(lista_servidores[i+2])
        threads[nombre] = myThread(nombre, direccion, puerto)
if (option == 2):
    jsoninput = input('Ingrese el JSON: ')
    #[{"nombre": "N1","direccion": "localhost","puerto": 8100},{"nombre": "N2","direccion": "localhost","puerto": 8101}]
    #[{"nombre": "N1","direccion": "localhost","puerto": 8120}]
    x = json.loads(jsoninput)
    for i in range(0,len(x)):
        nombre =  x[i]['nombre']
        direccion = x[i]['direccion']
        puerto = str(x[i]['puerto'])
        threads[nombre] = myThread(nombre, direccion, puerto)

for t in threads:
    threads[t].connect()
    #threads[t].join()

# Loop del server
while True:
    # Obtenemos los mensajes de la conexion y la direccion
    
    cmds = cmd.split()
    if (len(cmds) <= 1):
        print("Ingrese un comando válido")
    else:
        if (cmds[0] == "ls"):
            if (cmds[1] == "all"):
                for t in threads:
                    threads[t].sendls()
            else:
                for c in cmds[1:]:
                    threads[c].sendls()
        elif (cmds[0] == "echo"):
            if (cmds[1] == "all"):
                for t in threads:
                    threads[t].sendecho()
            else:
                for c in cmds[1:]:
                    threads[c].sendecho()
        elif (cmds[0] == "cat"):
            if (cmds[1] == "all"):
                for t in threads:
                    threads[t].sendcat()
            else:
                for c in cmds[1:]:
                    threads[c].sendcat()
        elif (cmds[0] == "help"):
            if (cmds[1] == "all"):
                for t in threads:
                    threads[t].sendhelp()
            else:
                for c in cmds[1:]:
                    threads[c].sendhelp()
        elif (cmds[0] == "exit"):
            if (cmds[1] == "all"):
                for t in threads:
                    threads[t].sendexit()
            else:
                for c in cmds[1:]:
                    threads[c].sendexit()
        else:
            print("Comando invalido, ingrese nuevamente")
