from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ether
from ryu.ofproto import inet
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        # arp table: for searching
        self.arp_table={}
        #the table for arp searching
        self.arp_table["10.0.0.1"] = "00:00:00:00:00:01";
        self.arp_table["10.0.0.2"] = "00:00:00:00:00:02";

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER) #decorator
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto #protocol of ryu and switch
        parser = datapath.ofproto_parser

        #Static rule default rule
        match = parser.OFPMatch() 
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_nw_flow(datapath, 0, match, actions)

   
    def add_nw_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]  #action instruction

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,  #modify flow table, done by controller
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg #represents packet_in Data structure
        datapath = msg.datapath #represents switch
        ofproto = datapath.ofproto #represents open flow protocols that switch and ryu will negotiate 
        parser = datapath.ofproto_parser 

        in_port = msg.match['in_port'] #match in_port for the incoming packet
        pkt = packet.Packet(msg.data)#Create packet class instance with the raw data
        eth = pkt.get_protocol(ethernet.ethernet)#extract ethernet header protocol
        ethertype = eth.ethertype
	dp_id = datapath.id #switch number

        # process ARP  
        if ethertype == ether.ETH_TYPE_ARP:
            self.arp_pkt_handler(datapath, in_port, pkt)
            return

        if ethertype == ether.ETH_TYPE_IP:  #process IP
       
           if dp_id == 1: # switch S1
              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_TCP,
                                       ipv4_src = '10.0.0.1',
                                       ipv4_dst = '10.0.0.2')
              actions = [parser.OFPActionOutput(2)]
              self.add_nw_flow(datapath, 10, match, actions)
 
              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_TCP,
                                      ipv4_src = '10.0.0.2',
                                      ipv4_dst = '10.0.0.1')
              actions = [parser.OFPActionOutput(1)]
              self.add_nw_flow(datapath, 10, match, actions)

              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_ICMP,
                                       ipv4_src = '10.0.0.1',
                                       ipv4_dst = '10.0.0.2')
              actions = [parser.OFPActionOutput(2)]
              self.add_nw_flow(datapath, 10, match, actions)
 
              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_ICMP,
                                      ipv4_src = '10.0.0.2',
                                      ipv4_dst = '10.0.0.1')
              actions = [parser.OFPActionOutput(1)]
              self.add_nw_flow(datapath, 10, match, actions)

           elif dp_id == 2: # switch S2

              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_TCP,
                                      ipv4_src = '10.0.0.1',
                                      ipv4_dst = '10.0.0.2')
              actions = [parser.OFPActionOutput(2)]
              self.add_nw_flow(datapath, 10, match, actions)
 
              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_TCP,
                                      ipv4_src = '10.0.0.2',
                                      ipv4_dst = '10.0.0.1')
              actions = [parser.OFPActionOutput(1)]
              self.add_nw_flow(datapath, 10, match, actions)

              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_ICMP,
                                      ipv4_src = '10.0.0.1',
                                      ipv4_dst = '10.0.0.2')
              actions = [parser.OFPActionOutput(2)]
              self.add_nw_flow(datapath, 10, match, actions)
 
              match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto=inet.IPPROTO_ICMP,
                                      ipv4_src = '10.0.0.2',
                                      ipv4_dst = '10.0.0.1')
              actions = [parser.OFPActionOutput(1)]
              self.add_nw_flow(datapath, 10, match, actions)
        return

    def arp_pkt_handler(self, datapath, in_port, pkt):  #ARP packets
        ofproto = datapath.ofproto  
        parser = datapath.ofproto_parser

        # parse out the ethernet and arp packet
        eth_pkt = pkt.get_protocol(ethernet.ethernet)#ethernet protocol
        arp_pkt = pkt.get_protocol(arp.arp)#arp protocol
        # obtain the MAC of dst IP  
        arp_resolv_mac = self.arp_table[arp_pkt.dst_ip]

        ### the packet library section
        ether_hd = ethernet.ethernet(dst = eth_pkt.src,src = arp_resolv_mac,ethertype = ether.ETH_TYPE_ARP) #ethernet header
        arp_hd = arp.arp(hwtype = 1, proto = 0x0800, hlen = 6, plen = 4, opcode= 2,src_mac = arp_resolv_mac, src_ip = arp_pkt.dst_ip,
                         dst_mac = eth_pkt.src, dst_ip = arp_pkt.src_ip) #arp header

        arp_reply = packet.Packet() #generating arp_reply packet
        arp_reply.add_protocol(ether_hd) #adding header
        arp_reply.add_protocol(arp_hd)
        arp_reply.serialize() #send arp reply
        
        # send the Packet Out mst to back to the host who is initilaizing the ARP
        actions = [parser.OFPActionOutput(in_port)];
        out = parser.OFPPacketOut(datapath, ofproto.OFP_NO_BUFFER, 
                                  ofproto.OFPP_CONTROLLER, actions,
                                  arp_reply.data)
        datapath.send_msg(out)


       
