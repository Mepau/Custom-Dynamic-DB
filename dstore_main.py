from xmlrpc.server import SimpleXMLRPCServer
from dstore_services import DStoreServices
from comm_protocols import CommProtocols
from sync_protocols import SyncProtocols
from xmlrpc.client import ServerProxy
import time
import queue
import threading
from dotenv import load_dotenv
import os
import socket
import xml.etree.ElementTree as ET
import select
import sys

load_dotenv()

Header = 64
Format = "utf-8"
magic_num = 1962
app_port = 8000
node_port = 8080
DisconnectMsg = "!CLOSE"

datastore = {}
dstore_queue = queue.Queue()

app_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app_server.bind((os.getenv("HOSTNAME"), app_port))
app_server.listen()

node_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
node_server.setblocking(0)
node_server.bind((os.getenv("HOSTNAME"), node_port))
node_server.listen(5)


def parse_xml(stringed_xml):

    tree = ET.fromstring(stringed_xml)
    method_name = tree.find("./methodName").text
    name_param = tree.find(".//param[@name='nombre']/value/string").text
    value_param = tree.find(".//param[@name='valor']/value/string").text

    if tree.find(".//param[@name='valor']/value").tag == "int":
        value_param = int(value_param)

    return (method_name, name_param, value_param)


def app_handler(conn, addr, app_api):

    connected = True

    while connected:
        msg_length = conn.recv(Header).decode(Format)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(Format)
            print(msg)
            if msg == DisconnectMsg:
                connected = False
            else:
                method_name, name, value = parse_xml(msg)
                if method_name == "Set":
                    conn.sendall(bytes(str(app_api.dstoreSet(name, value)), "utf-8"))
                elif method_name == "Get":
                    conn.sendall(bytes(str(app_api.dstoreGet(name)), "utf-8"))
                elif method_name == "Inc":
                    conn.sendall(bytes(str(app_api.dstoreInc(name)), "utf-8"))
                elif method_name == "Expire":
                    conn.sendall(bytes(str(app_api.dstoreExp(name, value)), "utf-8"))
                elif method_name == "Delete":
                    conn.sendall(bytes(str(app_api.dstoreDel(name)), "utf-8"))


def node_handler(dstore_queue, node_api):

    # Sockets from which we expect to read
    inputs = [node_server]
    # Sockets to which we expect to write
    outputs = []
    # Outgoing message queues (socket:Queue)
    # message_queues = {}

    while inputs:
        # Wait for at least one of the sockets to be ready for processing
        print(sys.stderr, "\nwaiting for the next event")
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is node_server:
                conn, addr = s.accept()
                conn.setblocking(0)
                inputs.append(conn)
                outputs.append(conn)
            else:
                data = s.recv(1024)
                if data:
                    # Extraer data del xml
                    method_name, name, value = parse_xml(data)
                    print(method_name, name, value)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

        if not dstore_queue.empty():

            next_msg = dstore_queue.get()
            for s in writable:
                try:
                    s.send(next_msg)
                except socket.error as exc:
                    print(exc)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()


if __name__ == "__main__":

    try:
        print("serving...")
        app_api = DStoreServices(datastore, dstore_queue)
        node_api = SyncProtocols(dstore_queue)

        node_thread = threading.Thread(
            target=node_handler, args=(dstore_queue, node_api)
        )

        print("Starting Node server")
        node_thread.start()

        while True:
            conn, addr = app_server.accept()
            thread = threading.Thread(target=app_handler, args=(conn, addr, app_api))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")

    except KeyboardInterrupt:
        print("Exiting")