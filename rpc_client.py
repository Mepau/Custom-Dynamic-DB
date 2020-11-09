from xmlrpc.client import ServerProxy

proxy = ServerProxy("http://localhost:8000")

proxy.dstoreSet("otro","valor")
print(proxy.dstoreGet("otro"))
proxy.dstoreSet("algo","otrovalor")
print(proxy.dstoreGet("algo"))
proxy.dstoreSet("mas","valores")
print(proxy.dstoreGet("mas"))
proxy.dstoreSet("otro","valor")