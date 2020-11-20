import xml.etree.ElementTree as ET
import queue
import os
import socket
import re
import platform

#Funcion wrapper para utilizar el comando ping de los SO Windows o Linux
def ping(address):

    if platform.system() == "Linux":
        return not os.system("ping -c 1 -W 1500 %s" % (address,))
    elif platform.system() == "Windows":
        return not os.system("ping %s -n 1 -w 1500" % (address,))

#Verificar que el parametro tiene el formato valido de ip
def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False

#Clase para contener y automatizar la captura de valores en el archivo config.xml
class CommProtocols:
    def __init__(self):
        self.addrlist = []
        self.nodestatus = {}

        #Al instanciarse se debe realizar la lectura y captura de informacion en config.xml
        self.retrieve_config()

        # Inicializar estado del estado de direcciones ip de los nodos vecinos
        for address in self.addrlist:
            if address not in self.nodestatus:
                self.nodestatus[address] = False

    #Funcion para lectura de archivo utilizando libreria ElementTree
    def retrieve_config(self):

        root_config = ET.parse("config.xml")
        for neighbor in root_config.iter("neighbor"):
            # Confirmar si en el atributo ip existe un formato de ip valido
            if valid_ip(neighbor.attrib["ip"]):
                # En caso de que se especifique un puerto
                if "port" in neighbor.attrib:
                    self.addrlist.append(
                        (neighbor.attrib["ip"], int(neighbor.attrib["port"]))
                    )
                else:
                    self.addrlist.append(neighbor.attrib["ip"])

    #Funcion para automatizar los comandos pings a las direcciones ip encontradas
    #De ser efectuosos modificar su estado a disponibles
    def search_conn(self):

        for address in self.nodestatus:
            # En caso de ser haberse especificado un puerto
            if isinstance(address, tuple):
                if ping(address[0]):
                    self.nodestatus[address] = True
            else:
                if ping(address):
                    self.nodestatus[address] = True

    #Funcion para retornar las direcciones validas que pueden ser alcanzadas via pings
    #Y se encuentran en archivo config.xml
    def active_conn(self):

        active_connections = []

        self.search_conn()

        for address in self.nodestatus:
            if self.nodestatus[address]:
                active_connections.append(address)

        return active_connections
