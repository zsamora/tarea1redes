Tarea 1 Redes: Cliente Multitelnet

Instrucciones:
	- El programa está escrito en Python 3 por lo cual debe correr el comando: python3 tarea1.py
	- Para cerrar el programa debe apretarse Ctrl+Z o Ctrl+C (como cualquier programa en Python)
	- El diseño del programa esta enfocado en que el usuario siga las instrucciones dadas (descritas en cada print), por lo cual no debería haber complicaciones en ese sentido (mientras se sigan las reglas). También se proveen ejemplos dentro del codigo para los dos formatos de ingreso de servers

Pasos a seguir:
	- Primero, debe correr todos los servers que vaya a utilizar (el binario entregado por el equipo docente).
	- Segundo, debe utilizar las direcciones y puertos correspondientes a esos servidores corriendo para poder trabajar.
	- Tercero, las interacciones con los servidores se realizan paralelamente, por lo que para distinguirlas se realiza primero un print indicando el inicio del proceso de envio de los comandos ingresados por el cliente. En cuanto se reciba un mensaje del server, se entrega inmediatamente encapsulado dentro de gatos y el nombre del server (formato de separacion que se auto-explica al utilizar el programa). Esto no altera la capacidad del usuario para ingresar comandos cuando lo desee (podrá ver la inmediatez de su acción por el print indicado anteriormente).
	- Cuarto, al cerrar una conexion con exit, el thread del server (y su conexion por telnet) desaparecen, por lo que es imposible volver a enviarle comandos dentro del mismo programa (debe reiniciar el programa nuevamente ingresando los servers deseados).
	- Quinto, el codigo esta implementado con comentarios en español para una mejor comprensión. Se asume que el usuario ingresara todos los comandos y opciones respetando los formatos descritos en su consola.


