# Read username, output from non-empty factory, drop connections
from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import basic

class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        d = self.factory.getUser(user)
        
        def onError(err):
            return "Internal Error"
        
        d.addErrback(onError)
        
        def writeResponse(message):
            self.transport.write(message+"\r\n")
            self.transport.loseConnection()
        
        d.addCallback(writeResponse)

class FingerFactory(protocol.ServerFactory):
    
    protocol = FingerProtocol
    
    def __init__(self, **kwargs):
        self.users = kwargs
        
    def getUser(self, user):
        #return utils.getProcessOutput("finger", [user])
        return defer.succeed(self.users.get(user, "No such user"))

application = service.Application('finger', uid=1, gid=1)
factory = FingerFactory(moshez='Happy and well')
internet.TCPServer(79, factory).setServiceParent(service.IServiceCollection(application))
#reactor.listenTCP(1079, FingerFactory(moshez='Happy and well', tlodge='happy too'))
#reactor.run()