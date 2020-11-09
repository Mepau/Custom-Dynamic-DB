import time
import threading

class DStoreServices():

    lock = threading.Lock()

    def __init__(self, datastore, dstore_q):
        self.localdict = datastore
        self.localq = dstore_q


    def dstoreSet(self, name, value):

        if name:
            #Si objeto existe en el diccionario
            if name in self.localdict:
                with lock:
                    self.localdict[name] = value
                    self.localq.put(((name,value),"UPDATED"))
                return True
            else:
                #Objeto no existe en el diccionario
                with lock:
                    self.localdict[name] = value
                    self.localq.put(((name,value),"CREATED"))
                return True

        return False


    def dstoreGet(self, name):

        if name:
            if name in self.localdict:
                return self.localdict[name]


    def dstoreInc(self, name, value):

        if name in self.localdict:
            currVal = self.localdict[name]
            if currVal.isnumeric():
                with lock:
                    localdict[name] = str(int(currVal) + value)
                    self.localq.put(((name,value),"INCREMENT"))
                return self.localdict[name]
            else:
                print("[ERROR] El objeto no es un numero.")
                return False

        return True

    def dstoreExp(self, name, seg):

        if name in self.localdict:
            with lock:
                self.localq.put(((name,seg),"EXPIRING"))
                time.sleep(seg)
                self.localdict.pop(name)
                self.localq.put((name,"EXPIRED"))

            return True
        return False


    def dstoreDel(self, name):
        if name in self.localdict:
            with lock:
                self.localdict.pop(name)
                self.localq.put((name,"EXPIRED"))
            return True
        return False
