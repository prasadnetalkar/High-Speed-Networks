from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import time
import threading
import datetime

class MyTopo(Topo):
    
     def build(self):

	Topo.__init__( self)
 
        host1 = self.addHost('h1',mac='00:00:00:00:ff:01')
        host2 = self.addHost('h2',mac='00:00:00:00:ff:02')
        host3 = self.addHost('h3',mac='00:00:00:00:ff:03')
        host4 = self.addHost('h4',mac='00:00:00:00:ff:04')
        switchA = self.addSwitch('s1')
        switchB = self.addSwitch('s2')
        

        self.addLink(host1, switchA,cls=TCLink,bw=10, delay='2ms')
        self.addLink(host2, switchA,cls=TCLink,bw=20, delay='10ms')
        self.addLink(host3, switchB,cls=TCLink,bw=10, delay='2ms')
        self.addLink(host4, switchB,cls=TCLink,bw=20, delay='10ms')
        self.addLink(switchA, switchB,cls=TCLink,bw=20, delay='2ms',loss=10)
    
	
def mytest():
   topo=MyTopo(Topo)  
   topo.build()
   global net
   net=Mininet(topo=topo,link=TCLink)
   net.start()
   print "Dumping Host connections"
   dumpNodeConnections(net.hosts)
   print "Testing connectivity"
   net.pingAll()
  
def test1():
   h1,h3 = net.get('h1','h3')
   h3.cmd('iperf -s -i 0.5 > a.txt &') #taking iperf results from server side
   h1.cmd('iperf -c 10.0.0.3 -t 20')
   print "Testing bandwidth between h1 and h3"
   f=open('/home/prasad/Desktop/a.txt')
   for line in f.readlines():
       print '%s' %(line.strip())
   f.close()

def test2():
   h2,h4 = net.get('h2','h4')
   h4.cmd('iperf -s -i 0.5 > b.txt &') #taking iperf results from server side
   time.sleep(10) 
   h2.cmd('iperf -c 10.0.0.4 -t 20')
   print "Testing bandwidth between h2 and h4"
   f=open('/home/prasad/Desktop/b.txt')
   for line in f.readlines():
       print '%s' %(line.strip())
   f.close()
   net.stop()
if __name__ == '__main__':
        setLogLevel('info')
	mytest()
        thread1 = threading.Thread(target=test1, args=())
	thread2 = threading.Thread(target=test2, args=())
	print datetime.datetime.now()
	thread1.start()
	thread2.start()
        thread1.join()
	thread2.join()
	print datetime.datetime.now()
        

   

