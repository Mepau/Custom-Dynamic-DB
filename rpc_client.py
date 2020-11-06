from xmlrpc.client import ServerProxy

proxy = ServerProxy("http://localhost:3000")

proxy.dstoreSet("otro","valor")
print(proxy.dstoreGet("otro")) 
