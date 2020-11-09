from xmlrpc.server import SimpleXMLRPCServer
from dstore_services import DStoreServices
from sync_protocols import SyncProtocols
from xmlrpc.client import ServerProxy
import time
import queue
import threading
from dotenv import load_dotenv
import os

load_dotenv()

magic_num = 1962

datastore = {}
dstore_queue = queue.Queue()

def queue_handler(dstore_q):

    lock = threading.Lock()

    while True: 
        if not dstore_q.empty():
            rpc = dstore_q.get()
            print (rpc)
            if rpc[1] == "CREATE" or "UPDATED":
                ServerProxy("").update(rpc[0], rpc[1], magic_num)
            elif rpc[1] == "UPDATE":
                with lock:
                    datastore[rpc[0][0]] = rpc[0][1]
 

def network_handler():

    while True:
        sync_services.handle_request()

#class ServerNode(SimpleXMLRPCServer):
    def serve_forever(self):
        self.quit = 0
        while not self.quit:
            print("Manejando algun request\n")
            self.handle_request()


def kill():
    server.quit = 1
    return True

app_services = SimpleXMLRPCServer((os.getenv("HOSTNAME"), 8000), logRequests=True)
#app_services = ServerNode((hostname, 8000), logRequests=True)
app_services.register_instance(DStoreServices(datastore, dstore_queue))

sync_services = SimpleXMLRPCServer((os.getenv("HOSTNAME"), 8080), logRequests=True)
sync_services.register_instance(SyncProtocols(dstore_queue))


queue_thread = threading.Thread(target=queue_handler, args=(dstore_queue,))
network_thread = threading.Thread(target=network_handler)

if __name__ == "__main__":
    try:

        network_thread.start()
        queue_thread.start()
        print("serving...")

        while True:
            app_services.handle_request()
            
    except KeyboardInterrupt:
        print("Exiting")