import time


class DStoreServices():

    def __init__(self, datastore, dstore_q):
        self.localdict = datastore
        self.localq = dstore_q


    def dstoreSet(self, nombre, valor):

        if nombre:
            #Si objeto existe en el diccionario
            if nombre in self.localdict:
                self.localdict[nombre] = valor
                self.localq.put((nombre,"UPDATED"))
                return True
            else:
                #Objeto no existe en el diccionario
                self.localdict[nombre] = valor
                self.localq.put((nombre,"CREATED"))
                return True

        return False


    def dstoreGet(self, nombre):

        if nombre:
            if nombre in self.localdict:
                return self.localdict[nombre]


    def dstoreInc(self, nombre, valor):

        if nombre in self.localdict:
            currVal = self.localdict[nombre]
            if currVal.isnumeric():
                localdict[nombre] = str(int(currVal) + valor)
                self.localq.put((nombre,"INCREMENT"))
                return self.localdict[nombre]
            else:
                print("[ERROR] El objeto no es un numero.")
                return False

        return True

    def dstoreExp(self, nombre, seg):

        if nombre in self.localdict:
            self.localq.put((nombre,"EXPIRING"))
            time.sleep(seg)
            self.localdict.pop(nombre)
            self.localq.put((nombre,"EXPIRED"))
            return True
        return False


    def dstoreDel(self, nombre):
        if nombre in self.localdict:
            self.localdict.pop(nombre)
            self.localq.put((nombre,"EXPIRED"))
            return True
        return False
