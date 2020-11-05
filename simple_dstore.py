import time


localdict = {}

def dstoreSet(nombre, valor):

    if nombre:
        #Si objeto existe en el diccionario
        if nombre in localdict:
            localdict[nombre] = valor
        else:
            #Objeto no existe en el diccionario
            localdict[nombre] = valor
    pass

def dstoreGet(nombre):

    if nombre:
        if nombre in localdict:
            return localdict[nombre]

def dstoreInc(nombre, valor):

    if nombre in localdict:
        currVal = localdict[nombre]
        if currVal.isnumeric():
            localdict[nombre] = str(int(currVal) + valor)
        else:
            print("[ERROR] El objeto no es un numero.")

def dstoreExp(nombre, seg):
    
    if nombre in localdict:
        time.sleep(seg)
        localdict.pop(nombre)

 


def dstoreDel(nombre):
    if nombre in localdict:
        localdict.pop(nombre)



print(localdict)
dstoreSet("cosa","otrovalor")
print(dstoreGet("otra"))

dstoreSet("num","5")

print(dstoreGet("num"))
dstoreInc("num",4)
print(dstoreGet("num"))

dstoreDel("num")
print(localdict)