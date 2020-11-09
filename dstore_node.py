from xmlrpc.server import SimpleXMLRPCServer
from dstore_services import DStoreServices
from sync_protocols import SyncProtocols
from xmlrpc.client import ServerProxy
import time
import queue
import threading



datastore = {}
dstore_queue = queue.Queue()
proxy = ServerProxy("http://localhost:8000")

def node_start():

    

    while True:
        sync_services.handle_request()
        if not dstore_queue.empty():
            rpc = dstore_queue.get()
            if rpc == "CREATE" or "UPDATE":
                print(dstore_queue.get())
    pass

#class ServerNode(SimpleXMLRPCServer):
    def serve_forever(self):
        self.quit = 0
        while not self.quit:
            print("Manejando algun request\n")
            self.handle_request()


def kill():
    server.quit = 1
    return True

app_services = SimpleXMLRPCServer(("localhost", 8000), logRequests=True)
#app_services = ServerNode(("localhost", 8000), logRequests=True)
app_services.register_instance(DStoreServices(datastore, dstore_queue))

sync_services = SimpleXMLRPCServer(("localhost", 8080), logRequests=True)
sync_services.register_instance(SyncProtocols(dstore_queue))


network_thread = threading.Thread(target=node_start)

if __name__ == "__main__":
    try:

        network_thread.start()
        print("serving...")

        while True:
            app_services.handle_request()
    except KeyboardInterrupt:
        print("Exiting")