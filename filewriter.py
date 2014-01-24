import sys
import os
import time
from threading import Timer

def awrite(proto, saddr, sport, daddr, dport, npkts, nbytes,timestamp):
        tmpFile = "/tmp/flows.txt"
        myFile  = "/Users/tlodge/twisted/flows.txt"
        print "%d %s %d %s %d %d %d %d" % (proto, saddr, sport, daddr, dport, npkts, nbytes, timestamp)
        f = open(myFile, 'a')
        f.write("%d %s %d %s %d %d %d %d\n" % (proto, saddr, sport, daddr, dport, npkts, nbytes, timestamp))
        f.flush()
        os.fsync(f.fileno())
        f.close()     
        t = Timer(1, awrite, [11, "127.0.0.1", 80, "128.234.56.67", 90, 10, 100, 1234567891])  
        t.start()
        #os.rename(tmpFile, myFile)


awrite(11, "127.0.0.1", 80, "128.234.56.67", 90, 10, 100, 1234567891)
