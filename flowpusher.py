from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, task
from twisted.application.internet import TimerService
import csv
import os
import threading
import time

protocol = None


def watch():
    global protocol
    if protocol is not None:
        protocol.message("hello!!")

class ReadThread(threading.Thread):
    def run(self):
        while True:
            time.sleep(2)
            if protocol is not None:
                reactor.callFromThread(self.dispatch)
    def dispatch(self):
        global protocol
        protocol.message("hello!!")

class FlowPush(Protocol):

    def connectionMade(self):
        global protocol
        self.factory.clients.append(self)
        protocol = self
        print "clients are ", self.factory.clients

    def startProtocol(self):
        print "In start protocol!"
        self._call = task.LoopingCall(self.message("hello"))
        self._loop = self._call.start(2)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
	a = data.split(":")
       	print a
      	if len(a) > 1:
		command = a[0]
              	content = a[1]
                msg = ""
                if command == "iam":
                	self.name = content
                        msg = self.name + "has joined"

                elif command == "msg":
                        msg = self.name + ": " +  content
                        print msg

                for c in self.factory.clients:
                        c.message(msg)

    def message(self,message):
        print ("sending message!");
        self.transport.write(message + '\n')

def aLongMethod(filename, file, sp, protocol):
    import time
    time.sleep(2)
    protocol.message(b"hello!!!")
    #flen = os.path.getsize(filename)
    #if sp > 0 and sp < flen:
    #    myfile.seek(sp+1)
    #    for line in myfile:
    #       protocol.send(line);
    #    myfile.seek(0, os.SEEK_END)
    #    sp = myfile.tell()
    reactor.callInThread(aLongMethod, filename, file, sp, protocol)

factory = Factory()
factory.clients = []
factory.protocol = FlowPush
s = TimerService(2, watch)
s.startService()
reactor.listenTCP(8080, factory)

#other = ReadThread()
#other.start()

print "Flowpussh server started!"
FLOWFILE = "/root/flows.txt"
myfile = open(FLOWFILE, "rt")
sp = os.path.getsize(FLOWFILE)
#reactor.callInThread(aLongMethod, FLOWFILE, myfile, sp, factory.protocol)
reactor.run()

