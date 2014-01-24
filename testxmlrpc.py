import xmlrpclib
server = xmlrpclib.Server('http://127.0.0.1:8000/MYRPC')
print server.getUser('tlodge')