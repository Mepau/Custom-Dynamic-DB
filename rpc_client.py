from xmlrpc.client import ServerProxy
from dotenv import load_dotenv
import os

load_dotenv()

port = "8000"

proxy = ServerProxy("http://%s:%s" % (os.getenv("HOSTNAME"), port))

proxy.dstoreSet("otro","valor")
print(proxy.dstoreGet("otro"))
proxy.dstoreSet("algo","otrovalor")
print(proxy.dstoreGet("algo"))
proxy.dstoreSet("mas","valores")
print(proxy.dstoreGet("mas"))