from xmlrpc.server import SimpleXMLRPCServer
from dstore_services import DStoreServices
from comm_protocols import CommProtocols
from xmlrpc.client import ServerProxy
from xml_helpers import parse_from_xml, parse_to_xml, retrv_xml_meta
from sync_protocols import SyncProtocols
import time
import queue
import threading
import os
import socket
import select
import sys
import uuid
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()

Header = 64
Format = "utf-8"
magic_num = 1962
app_port = 9002
node_port = 9202
DisconnectMsg = b"!CLOSE"

server_ip = os.getenv("HOSTNAME")

# Estructuras de datos para cbase de dato, historia y cola de comunicacion
datastore = {}
history = {}
dstore_queue = queue.Queue()


app_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
app_server.bind((server_ip, app_port))
app_server.listen()

node_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
node_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
node_server.setblocking(0)
node_server.bind((server_ip, node_port))
node_server.listen(5)

# Funcion principal del thread inicial para llamadas XMLRPC desde la app
def app_handler(conn, addr, store_api, sync_api):

    connected = True
    print(conn.getsockname())

    while connected:
        data = conn.recv(1024)

        if data:
            if data == DisconnectMsg:
                connected = False
            else:
                proc_call, name, val = parse_from_xml(data)

                new_id = str(uuid.uuid1())
                ts = datetime.timestamp(datetime.now())

                sync_api.add_history(
                    new_id, ts, f"{server_ip}:{node_port}", (server_ip, node_port)
                )

                if proc_call == "Set":
                    conn.sendall(
                        bytes(str(store_api.dstoreSet(name, val, new_id)), "utf-8")
                    )
                elif proc_call == "Get":
                    conn.sendall(bytes(str(store_api.dstoreGet(name)), "utf-8"))
                elif proc_call == "Inc":
                    conn.sendall(bytes(str(store_api.dstoreInc(name, new_id)), "utf-8"))
                elif proc_call == "Expire":
                    conn.sendall(
                        bytes(str(store_api.dstoreExp(name, val, new_id)), "utf-8")
                    )
                elif proc_call == "Delete":
                    conn.sendall(bytes(str(store_api.dstoreDel(name, new_id)), "utf-8"))


# Funcion principal del thread inicial para llamadas XMLRPC desde y para otros nodos
def node_handler(dstore_queue, store_api, sync_api):

    # Socket que se esperan recibir data
    inputs = [node_server]
    # Lista con socket de los demas nodos
    outputs = []

    # Obtener informacion sobre conectividad y latencia con otros nodos listado en el config.xml
    # Por ahora solo via pings
    active_server = CommProtocols().active_conn()

    for addr in active_server:
        Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Client.settimeout(3)

        # Si es una tupla se ha especificado otro puerto en el archivo config.xml
        if isinstance(addr, tuple):
            address = (addr[0], addr[1])
            try:
                # Efectuar conexion y agregar a puertos que estaran escuchados por el SO via select
                Client.connect(address)
                inputs.append(Client)
                outputs.append(Client)
            except socket.error as exc:
                print(exc)
        else:
            address = (addr, node_port)
            try:
                Client.connect(address)
                inputs.append(Client)
                outputs.append(Client)
            except socket.error as exc:
                print(exc)

    # Instancia contenedora de operaciones de sincornizacion gracias a una historia

    print("Starting nodes")

    while inputs:
        # Esperar por la llamada del SO cuando algun socket contenga data
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
                    proc_call, name, val = parse_from_xml(data)
                    meta_data = retrv_xml_meta(data)

                    # Mensaje debe contener un id
                    if meta_data["id"]:
                        if not sync_api.check_history(meta_data["id"]):
                            # De no encontrarse en el historial proceder a registrarlo
                            print(f"Mensaje recibido de: {s.getpeername()}\n {data}")
                            sync_api.add_history(
                                meta_data["id"],
                                meta_data["timestamp"],
                                meta_data["origin"],
                                s.getpeername(),
                            )
                            if proc_call == "Set":
                                store_api.dstoreSet(name, val, meta_data["id"])
                            elif proc_call == "Inc":
                                store_api.dstoreInc(name, meta_data["id"])
                            elif proc_call == "Expire":
                                store_api.dstoreExp(name, val, meta_data["id"])
                            elif proc_call == "Delete":
                                store_api.dstoreDel(name, meta_data["id"])
                    else:
                        pass
                else:
                    # Para casos en el que los clientes se desconecten
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

        # Loop para envio de la cola de mensajes
        while not dstore_queue.empty():

            # Obtener mensaje de cola
            params, upd_call = dstore_queue.get()
            # Obtener su historial
            history = sync_api.get_history(params[2])
            # Parsear a un mensaje formato XML
            next_msg = parse_to_xml(params, upd_call, history)

            # Los nodos son identificados via su direccion ip y puerto
            # Identificar el origen del mensaje y de quien fue recibido para ignorar en envio
            tuple_addr, tuple_port = tuple(history["origin"].split(":"))
            origin_tuple = (tuple_addr, int(tuple_port))

            for s in writable:
                if (
                    s.getpeername() == history["sender"]
                    or s.getpeername() == origin_tuple
                ):
                    pass
                else:
                    try:
                        print(f"Mensaje para enviar a: {s.getpeername()}\n {next_msg}")
                        s.sendall(bytes(next_msg))
                    except socket.error as exc:
                        print(exc)

        # Casos de sockets con excepciones
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()


# Entrada desde la terminal
if __name__ == "__main__":

    try:

        print("serving...")
        store_api = DStoreServices(datastore, dstore_queue)
        sync_api = SyncProtocols(history)

        node_thread = threading.Thread(
            target=node_handler, args=(dstore_queue, store_api, sync_api)
        )

        print("Starting Node server")
        node_thread.start()

        while True:
            conn, addr = app_server.accept()
            thread = threading.Thread(
                target=app_handler, args=(conn, addr, store_api, sync_api)
            )
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")

    except KeyboardInterrupt:
        print("Exiting")