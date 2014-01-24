from zope.interface import Interface, implements
from twisted.internet.protocol import Factory, Protocol
from twisted.application import internet, service
from twisted.internet import reactor, task
from twisted.protocols import basic
import sys

class FlowReader(Interface):
    """
    an object that returns lines of data from a file when ready
    """
    
    def getFlows():
        """
        periodically read in new flows.
        """

class FlowProtocol(basic.LineReceiver):
    
    def connectionMade(self):
        self.factory.clients.append(self)
       
    def send(self, message):
         self.transport.write(mesasage, '\r\n')
    

class FlowFileReader:
    """
        read in latest flows from a point in a file
    """
    implements(FlowReader)
    
    def __init__(self, filename):
        self.filename = filename 
        
    def getFlows(self, acallback):
        acallback("some flows for you: %s" % self.filename)
        #write something to the protocol.
        
    
class FlowFactory(Factory):
    
    protocol = FlowProtocol
    clients = []
    
    def __init__(self, flowreader):
        self.flowreader = flowreader
        self.monitorFlows()
        
    def addClient(self,aclient):
        clients.append(aclient)    

    def gotFlows(self,flows):
        print flows
        for c in self.clients:
            c.send(flows)
            
    def monitorFlows(self):
        self._call = task.LoopingCall(self.flowreader.getFlows, self.gotFlows)
        self._loop = self._call.start(2)
         
# class FlowService(service.Service):
#     def __init__(self, fileName):
#         self.fileName = fileName
#         
#     def startService(self):
#         self._port = reactor.listenTCP(8080, FlowFactory(FlowFileReader(fileName)))
#     
#     def stopService(self):
#         return self._port.stopListening()
        
factory = FlowFactory(FlowFileReader("/tmp/test.txt"))
#FlowFactory(FlowFileReader("/tmp/test.txt"))
reactor.listenTCP(8080, factory)
reactor.run()