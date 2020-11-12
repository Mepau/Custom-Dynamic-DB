import xml.etree.ElementTree as ET
import queue
import os
import socket
import re

def ping(address):
    return not os.system("ping %s -n 1 -w 1500" % (address,))

def valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

class CommProtocols():

    def __init__(self):
        self.addrlist = []
        self.nodestatus = {}

        self.retrieve_config()

        #Inicializar estado del estado de direcciones ip de los nodos vecinos
        for address in self.addrlist:
            if address not in self.nodestatus:
                self.nodestatus[address] = False


    def retrieve_config(self):

        root_config = ET.parse("config.xml")
        for neighbor in root_config.iter("neighbor"):
            if valid_ip(neighbor.attrib["ip"]):
                self.addrlist.append(neighbor.attrib["ip"])
            
    
    def search_conn(self):

        for address in self.nodestatus:
            if ping(address):
                self.nodestatus[address] = True
                print(address)
                


    def active_conn(self):

        active_connections = []

        self.search_conn()

        for address in self.nodestatus:
            
            if self.nodestatus[address]:
                active_connections.append(address)
        
        return active_connections

