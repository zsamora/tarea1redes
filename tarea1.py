# -*- coding: utf-8 -*-
import json
import time
import threading
import telnetlib

# Clase Thread para la lectura de los mensajes enviados por los servers (hereda de clase Thread)
class myThreadServer (threading.Thread):
    def __init__(self, name, direccion, puerto):
        threading.Thread.__init__(self)
        self.tn = telnetlib.Telnet(direccion, puerto)
        self.name = name

    def run(self):
        print ("Iniciando comunicacion con: " + self.name)
        self.initialmsg() # Mensaje de bienvenida del server
        self.readmsg()    # Lectura de mensajes

    def initialmsg(self):
        print (self.tn.read_until(b"'help'").decode('utf-8'))
        print (self.tn.read_until(b"\n").decode('utf-8'))
        print (self.tn.read_until(b"\n").decode('utf-8'))

    def readmsg(self):
        print (self.tn.read_all().decode('utf-8'))
        print ("Comunicacion terminada con: " + self.name)

class myThreadCommand (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def send(self, t, c, arg=""):
        print ("Enviando comando " + c + " " + arg + "a: " + t)
        if t in threads:
            threads[t].tn.write(str.encode(c+" "+arg))
            if (c=="exit"):
                del threads[t]
        else:
            print("Comunicacion inexistente con "+ t)


threads = {}
# Recibe opcion elegida por el usuario
option = input('Eliga uno de los siguientes formatos:\n1. Comando: nombre1 direccion1 puerto1 ... nombreN direcciónN puertoN \n2. JSON: [{"nombre": "N1","direccion": "localhost","puerto": 8086},...]\n')
option = int(option)
# Ej: N1 localhost 8120 N2 localhost 8121
if (option == 1):
    info_servidores = input('Ingresar comando: ')
    lista_servidores = info_servidores.split(' ')
    for i in range (0, len(lista_servidores), 3):
        nombre = str(lista_servidores[i])
        direccion = str(lista_servidores[i+1])
        puerto = str(lista_servidores[i+2])
        ## Si se ingresan dos servidores con el mismo nombre, se considera el ultimo como valido
        if nombre in threads:
            print("Nombre repetido en servidor " + nombre + ", se utilizara el ultimo valor")
        threads[nombre] = myThreadServer(nombre, direccion, puerto)
# Ej: [{"nombre": "N1","direccion": "localhost","puerto": 8100},{"nombre": "N2","direccion": "localhost","puerto": 8101}]
#     [{"nombre": "N1","direccion": "localhost","puerto": 8120}]
if (option == 2):
    jsoninput = input('Ingrese el JSON: ')
    x = json.loads(jsoninput)
    for i in range(0,len(x)):
        nombre =  x[i]['nombre']
        direccion = x[i]['direccion']
        puerto = str(x[i]['puerto'])
        ## Si se ingresan dos servidores con el mismo nombre, se considera el ultimo como valido
        if nombre in threads:
            print("Nombre repetido en servidor " + nombre + ", se utilizara el ultimo valor")
        threads[nombre] = myThreadServer(nombre, direccion, puerto)

for t in threads:
    threads[t].start()

threadc = myThreadCommand()
time.sleep(0.5) ## Delay para que el input "Comando: " aparezca después de los mensajes de bienvenida
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

        else:
            print("Comando invalido, ingrese nuevamente")
