
class SyncProtocols:

    #Inicializar con una estructura de base de dato tipo diccionario
    def __init__(self, history):
        self.history = history
        pass

    #Funcion que retorno booleano en caso de que un id haya sido encontrado en diccionario
    def check_history(self, rpc_id):

        if rpc_id in self.history:
            return True
        else:
            return False

    #Funcion para retornar la data correspondiente a un identificador
    def get_history(self, rpc_id):

        if rpc_id in self.history:
            return self.history[rpc_id]
        else:
            return False

    def add_history(self, rpc_id, timestamp, origin, address):

        #Cada identificador tiene como valor un diccionario 
        #para contener los diferentes campos de data
        self.history[rpc_id] = {}
        self.history[rpc_id]["timestamp"] = timestamp
        self.history[rpc_id]["origin"] = origin
        self.history[rpc_id]["sender"] = f"{address[0]}:{address[1]}"