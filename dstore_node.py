from xmlrpc.server import SimpleXMLRPCServer
from dstore_services import DStoreServices
import time

datastore = {}

class ServerNode(SimpleXMLRPCServer):

    def serve_forever(self):
        self.quit = 0
        while not self.quit:
            self.handle_request()

def kill():
    server.quit = 1
    return True

#server = SimpleXMLRPCServer(("localhost", 3000), logRequests=True)
server = ServerNode(("localhost", 3000))
server.register_instance(DStoreServices(datastore))

if __name__ == "__main__":
    try:
        print("serving...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")


datastore["prueba"] = "test"
