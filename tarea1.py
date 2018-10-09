# -*- coding: utf-8 -*-
import json
import time
import threading
import subprocess
import telnetlib

minicial = 0

class myThreadServer (threading.Thread):
    def __init__(self, name, direccion, puerto):
        threading.Thread.__init__(self)
        self.tn = telnetlib.Telnet(direccion, puerto)
        self.name = name

    def run(self):
        self.initialmsg()
        self.readmsg()

    def initialmsg(self):
        print (self.tn.read_until(b"'help'").decode('utf-8'))
        print (self.tn.read_until(b"\n").decode('utf-8'))
        print (self.tn.read_until(b"\n").decode('utf-8'))

    def readmsg(self):
        while True:
            print (self.tn.read_until(b"\n").decode('utf-8'))
            time.sleep(2)

class myThreadCommand (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def send(self, t, c, arg=0):
        if (not arg):
            print ("Sending " + c + " to: " + t)
            threads[t].tn.write(str.encode(c))
        else:
            print ("esteban")
            threads[t].tn.write(str.encode(c+arg))


threads = {}
# N1 localhost 8120 N2 localhost 8121
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
        threads[nombre] = myThreadServer(nombre, direccion, puerto)

if (option == 2):
    jsoninput = input('Ingrese el JSON: ')
    #[{"nombre": "N1","direccion": "localhost","puerto": 8100},{"nombre": "N2","direccion": "localhost","puerto": 8101}]
    #[{"nombre": "N1","direccion": "localhost","puerto": 8120}]
    x = json.loads(jsoninput)
    for i in range(0,len(x)):
        nombre =  x[i]['nombre']
        direccion = x[i]['direccion']
        puerto = str(x[i]['puerto'])
        threads[nombre] = myThreadServer(nombre, direccion, puerto)

for t in threads:
    threads[t].start()

threadc = myThreadCommand()
time.sleep(0.5)
# Loop del server
while True:
    # Obtenemos los mensajes de la conexion y la direccion
    cmd = input("Comando: ")
    cmds = cmd.split()
    if (len(cmds) <= 1):
        print("Ingrese un comando válido")
    else:
        if (cmds[0] == "ls"):
            if (cmds[1] == "all"):
                for t in threads:
                    threadc.send(t,"ls")
            else:
                for c in cmds[1:]:
                    threadc.send(c,"ls")

        elif (cmds[0] == "echo"):
            if (cmds[1] == "all"):
                for t in threads:
                    threadc.send(t,"echo")
            else:
                for c in cmds[1:]:
                    threadc.send(c,"echo")

        elif (cmds[0] == "cat"):
            if (cmds[1] == "all"):
                for t in threads:
                    threadc.send(t,"cat")
            else:
                for c in cmds[1:]:
                    threadc.send(c,"cat")

        elif (cmds[0] == "help"):
            if (cmds[1] == "all"):
                for t in threads:
                    threadc.send(t,"help")
            else:
                for c in cmds[1:]:
                    threadc.send(c,"help")

        elif (cmds[0] == "exit"):
            if (cmds[1] == "all"):
                for t in threads:
                    threadc.send(t,"exit")
            else:
                for c in cmds[1:]:
                    threadc.send(c,"exit")

        else:
            print("Comando invalido, ingrese nuevamente")
