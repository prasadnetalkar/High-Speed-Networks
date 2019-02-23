from mininet.topo import Topo
from functools import partial
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import OVSSwitch
from mininet.node import OVSController
import time


class MyTopo( Topo ):

	def __init__(self):
		
            Topo.__init__( self )
            host1 = self.addHost('h1', mac='00:00:00:00:00:01')
	    host2 = self.addHost('h2', mac='00:00:00:00:00:02')
	    switch1 = self.addSwitch('s1')
            switch2 = self.addSwitch('s2')
            self.addLink(host1,switch1,1,1)
            self.addLink(switch1,switch2,2,1)
            self.addLink(switch2,host2,2,1)


def create_topo():
    setLogLevel('info')
    topo=MyTopo()
    net = Mininet(topo=topo, controller=partial(RemoteController,
                                               ip='127.0.0.1',
                                               port=6633))
    net.start()
    dumpNodeConnections(net.hosts)
    return net

def test1(net):
    
    h1=net.get('h1')
    h2=net.get('h2')
    h2.cmd('iperf -s -p 10001 &')
    result=h1.cmd('iperf -c 10.0.0.2 -p 10001')
    print result
    h2.cmd('pkill iperf')

if __name__ == '__main__':
    
    setLogLevel('info')
    net = create_topo()
    time.sleep(20) #just to open wireshark
    test1(net)
    net.stop()

    	

