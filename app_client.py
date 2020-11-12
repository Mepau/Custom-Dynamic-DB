import socket, os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

# Valor de configuracion de envio de datos
Header = 64
Port = 8080
Format = "utf-8"
Server = os.getenv("HOSTNAME")
Address = ("10.0.0.123", Port)

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect(Address)


#def send(msg):
#
#    if type(msg) == bytes:
#        message = msg
#    if type(msg) is not bytes:
#        message = msg.encode(Format)
#
#    MsgLength = len(message)
#    SendLength = str(MsgLength).encode(Format)
#    SendLength += b" " * (Header - len(SendLength))
#    Client.send(SendLength)
#    Client.send(message)

tree = ET.parse('methodCall.xml')
tree2 = ET.parse('methodResponse.xml')

tree.find("methodName").text = "Get"
tree.find(".//param[@name='nombre']/value/string").text = "num"
tree.find(".//param[@name='valor']/value/string").text = "123"

tree = tree.getroot()

msg = ET.tostring(tree)
print(msg)
Client.sendall(msg)
data = Client.recv(1024)
print(data)
send("!CLOSE")
