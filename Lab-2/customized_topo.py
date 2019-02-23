from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink


class MyTopo(Topo):
    
     def __init__(self):

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

topos = { 'mytopo': ( lambda: MyTopo() ) }

