from mininet.topo import Topo
from mininet.node import OVSSwitch

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        switch1 = self.addSwitch( 's1' )
        switch2 = self.addSwitch( 's2' )
     

        # Add links
        self.addLink( host1,switch1,1,1 )
        self.addLink( host2,switch2,1,2 )
        self.addLink( switch1,switch2,2,1 )
      
        
topos = { 'mytopo': ( lambda: MyTopo() ) }

