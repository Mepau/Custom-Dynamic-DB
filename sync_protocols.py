from comm_protocols import CommProtocols, ping

magic_num = 1962

class SyncProtocols():

    def __init__(self, dstore_q):
        self.local_q = dstore_q

    def update(self, name, value, m_num):

        if m_num == magic_num:
            self.local_q.put((name,value), "UPDATE")
            return True        
        return False


    
