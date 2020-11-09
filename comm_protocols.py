import xml.etree.ElementTree as ET
import queue
import os
import socket
import re

def ping(address):
    return not os.system("ping %s -n 1 -w 2000" % (address,))

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
                print(self.nodestatus[address])


    def active_conn(self):

        active_connections = []

        self.search_conn()

        for address in self.nodestatus:
            print(self.nodestatus[address])
            if self.nodestatus[address]:
                active_connections.append(address)
                print(address)
        
        return active_connections

    
        

#print(ping("10.0.0.110"))

#CommProtocols().search_conn()

CommProtocols().active_conn()
