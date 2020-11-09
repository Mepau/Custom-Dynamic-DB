from comm_protocols import CommProtocols, ping

class SyncProtocols():

    def __init__(self, dstore_q):
        self.local_q = dstore_q

    def update(self, name, value, magic_num):
        self.local_q.put((name,value)) 
