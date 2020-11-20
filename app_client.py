import socket, os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

#Script para cliente de app de base de datos
#Solo es necesario modificar los valores de parametros como se comenta mas abajo linea 28

# Valor de configuracion de envio de datos
Header = 64
Port = 9002
Format = "utf-8"
Server = os.getenv("HOSTNAME")
Address = (Server, Port)

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.settimeout(10)

try:
    Client.connect(Address)
except socket.error as exc:
    print(exc)

addr, port = Client.getsockname()
tree = ET.parse("methodCall.xml")

#Solo es necesario modificar estos campos de manera que coincidan como solicitado en el pdf
tree.find("methodName").text = "Get"
tree.find(".//param[@name='nombre']/value/string").text = "valor"
tree.find(".//param[@name='valor']/value/string").text = "4"

tree = tree.getroot()
msg = ET.tostring(tree)

try:
    Client.sendall(msg)
except socket.error as exc:
    print(exc)

try:
    data = Client.recv(1024)
    print(data)
except socket.error as exc:
    print(exc)

try:
    Client.sendall(b"!CLOSE")
except socket.error as exc:
    print(exc)
