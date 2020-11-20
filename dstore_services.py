import time
import threading
import uuid
from datetime import datetime

lock = threading.Lock()


class DStoreServices:

    #Se inicializa con una cola para mensajes dstore_q
    #Y con una estructura tipo diccionario para base de dato datastore
    def __init__(self, datastore, dstore_q):
        self.localdict = datastore
        self.localq = dstore_q


    def dstoreSet(self, name, value, rpc_id):

        if name in self.localdict:
            with lock:
                self.localdict[name] = value
                #Se coloca en cola los parametros a insertar, id de correspondiente invocacion y estado
                self.localq.put(((name, value, rpc_id), "UPDATED"))
            return True
        else:
            # Objeto no existe en el diccionario
            with lock:
                self.localdict[name] = value
                self.localq.put(((name, value, rpc_id), "CREATED"))
            return True

    def dstoreGet(self, name):
        if name in self.localdict:
            return self.localdict[name]

    def dstoreInc(self, name, rpc_id):

        if name in self.localdict:
            currVal = self.localdict[name]
            if currVal.isnumeric():
                with lock:
                    self.localdict[name] = str(int(currVal) + 1)
                    self.localq.put(((name, None, rpc_id), "INCREMENTED"))
                return True
            else:
                print("[ERROR] El objeto no es un numero.")
                return False
        else:
            return "Objeto no encontrado"

    def dstoreExp(self, name, seg, rpc_id):

        if name in self.localdict:
            with lock:
                self.localq.put(((name, seg, rpc_id), "EXPIRING"))
                time.sleep(seg)
                self.localdict.pop(name)
            return True
        else:
            return "Objeto no encontrado"

    def dstoreDel(self, name, rpc_id):

        if name in self.localdict:
            with lock:
                self.localdict.pop(name)
                self.localq.put(((name, None, rpc_id), "EXPIRED"))
            return True
        else:
            return "Objeto no encontrado"
