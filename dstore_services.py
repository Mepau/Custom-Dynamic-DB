import time

class DStoreServices():

    def __init__(self, datastore):
        self.localdict = datastore


    def dstoreSet(self, nombre, valor):

        if nombre:
            #Si objeto existe en el diccionario
            if nombre in self.localdict:
                self.localdict[nombre] = valor
                return True
            else:
                #Objeto no existe en el diccionario
                self.localdict[nombre] = valor
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
                return self.localdict[nombre]
            else:
                print("[ERROR] El objeto no es un numero.")
                return False

        return True



    def dstoreExp(self, nombre, seg):

        if nombre in self.localdict:
            time.sleep(seg)
            self.localdict.pop(nombre)
            return True
        return False


    def dstoreDel(self, nombre):
        if nombre in self.localdict:
            self.localdict.pop(nombre)
            return True
        return False
