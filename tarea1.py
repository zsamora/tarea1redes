# -*- coding: utf-8 -*-
import json
import threading
import telnetlib

# Clase myThreadServer crea threads para la lectura de los mensajes enviados por los servers
class myThreadServer (threading.Thread):
    def __init__(self, name, direccion, puerto):
        threading.Thread.__init__(self)
        self.tn = telnetlib.Telnet(direccion, puerto) # Conexion telnet
        self.name = name # Nombre asignado por el usuario

    def run(self):
        # Mensaje de bienvenida
        print ("\n### Server: " + self.name + " ###\n##################\n" + self.tn.read_until(b"user@CC4303 ~ $").decode('utf-8') + "\n######################\n### Fin mensaje " + self.name + " ###\n")
        try:
            while True:
                # Lectura de mensajes enviados por el servidor
                print ("\n### Server: " + self.name + " ###\n##################\n" + self.tn.read_until(b"user@CC4303 ~ $").decode('utf-8') + "\n######################\n### Fin mensaje " + self.name + " ###\n")
        # Caso de cierre de conexión
        except EOFError:
            print ("Comunicacion terminada con: " + self.name +"\n")
# Clase myThreadCommand es quien envia los comandos ingresados por el cliente a los servers
class myThreadCommand (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threads = {} # Listado de threads de servers

    def send(self, t, c, arg=""):
        # Print para diferenciar el paralelismo (fijarse en el orden de impresion)
        print ("\nEnviando comando [ " + c + " " + arg + "] al server: " + t)
        # Si el thread existe, se envia el comando
        if t in self.threads:
            self.threads[t].tn.write(str.encode(c+" "+arg))
        # Si no existe se indica
        else:
            print("No existe socket de nombre: "+ t)

    def run(self):
        # Recibe opcion elegida por el usuario para el ingreso de servers
        option = input('Eliga uno de los siguientes formatos:\n1. Comando: nombre1 direccion1 puerto1 ... nombreN direcciónN puertoN \n2. JSON: [{"nombre": "N1","direccion": "localhost","puerto": puerto1},...]\n')
        option = int(option)
        # Opcion 1 : Linea de comandos
        # Ej: N1 localhost 8120 N2 localhost 8121 N3 localhost 8122
        if (option == 1):
            info_servidores = input('Ingresar comando: ')
            lista_servidores = info_servidores.split(' ')
            for i in range (0, len(lista_servidores), 3):
                nombre = str(lista_servidores[i])
                direccion = str(lista_servidores[i+1])
                puerto = str(lista_servidores[i+2])
                ## Si se ingresan dos servidores con el mismo nombre, se considera el ultimo como valido
                if nombre in self.threads:
                    print("Nombre repetido en servidor " + nombre + ", se utilizara el ultimo valor")
                self.threads[nombre] = myThreadServer(nombre, direccion, puerto)
        # Opcion 2 : JSON
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
                if nombre in self.threads:
                    print("Nombre repetido en servidor " + nombre + ", se utilizara el ultimo valor")
                self.threads[nombre] = myThreadServer(nombre, direccion, puerto)
        # Iniciar threads de cada server
        for t in self.threads:
            self.threads[t].start()
        # Loop del cliente principal
        while True:
            # Recibe el comando del cliente
            cmd = input("")
            cmds = cmd.split()
            # Si no cumple el formato, se ignora
            if (len(cmds) <= 1):
                print("Ingrese un comando válido")
            else:
                # Comando ls
                if (cmds[0] == "ls"):
                    if (cmds[1] == "all"):
                        for t in self.threads:
                            self.send(t,"ls")
                    else:
                        for c in cmds[1:]:
                            self.send(c,"ls")
                # Comando exit
                elif (cmds[0] == "exit"):
                    if (cmds[1] == "all"):
                        for t in self.threads:
                            self.send(t,"exit")
                        self.threads = {}
                    else:
                        for c in cmds[1:]:
                            self.send(c,"exit")
                            del self.threads[c]
                # Comando help
                elif (cmds[0] == "help"):
                    if (cmds[1] == "all"):
                        for t in self.threads:
                            self.send(t,"help")
                    else:
                        for c in cmds[1:]:
                            self.send(c,"help")
                # Comando echo
                elif (cmds[0] == "echo"):
                    if (cmds[2] == "all"):
                        for t in self.threads:
                            self.send(t,"echo",cmds[1])
                    else:
                        for c in cmds[2:]:
                            self.send(c,"echo",cmds[1])
                # Comando cat
                elif (cmds[0] == "cat"):
                    if (cmds[2] == "all"):
                        for t in self.threads:
                            self.send(t,"cat",cmds[1])
                    else:
                        for c in cmds[2:]:
                            self.send(c,"cat",cmds[1])
                # Comando desconocido, se ignora
                else:
                    print("Comando invalido, ingrese nuevamente")

threadc = myThreadCommand()
threadc.start()
threadc.join()
