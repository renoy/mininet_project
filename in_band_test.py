#!/usr/bin/python

"""
-Build a network of desired depth and fanout.
-In-band controller.
-All the hosts start sending traffic to a particular host.
-Traffic consists of certain # of data packets of a specified packet size and then a packet to generate a control traffic.
-Latency for the new packet to reach the destination host after the flow table being populated to the respective OVSs.
- % Packet Loss
- Iperf between the host and the controller
"""

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import Node, OVSSwitch, Controller, RemoteController
from mininet.link import Link
from mininet.log import setLogLevel, info
from mininet.topolib import TreeNet, TreeTopo
from time import sleep
import struct, socket

class InbandController( RemoteController ):

    def checkListening( self ):
        "Overridden to do nothing."
        return

def topo_init():
	myTopo = TreeTopo( depth=3, fanout=3 )
	global net 
	net = Mininet( topo=myTopo, switch=OVSSwitch, build=False )

	"Creating Controller"
	c0 = net.addController( 'c0', controller=InbandController, ip='10.0.0.100' )
	net.start()

	"Adding a host for changing to controller"
	server = net.addHost( 'server', ip='10.0.0.100')	
	s1 = net.get('s1')
	link = net.addLink( server, s1 )
	s1.attach( link.intf2 )
	net.configHosts()
	
	"Hosts list and the total # of hosts"
	global hosts_list 
	hosts_list = net.hosts
	global num_hosts
	num_hosts = len( hosts_list )
        
	"Assigning IP addresses to switches in the network"
	"TODO: Automate assigning of IP addresses"
	ip = hosts_list[-2].IP()

        "Assigning IP addresses to switches in the network"
        switch_list = net.switches
        n = len(switch_list)
        ip = hosts_list[-2].IP()

        for i in range(1,n+1):

                ip2int = lambda ipstr: struct.unpack( '!I', socket.inet_aton(ipstr))[0]
                int_ip = ip2int(ip)
                int_ip+=1
                int2ip = lambda n: socket.inet_ntoa(struct.pack('!I', n))
                ip = int2ip(int_ip)

                s = net.get('s%d' % i)
                s.cmd( 'ifconfig s%d %s ' % (i, ip) )
        """
	s1 = net.get('s1')
        s1.cmd( 'ifconfig s1 10.0.0.50' )
	s2 = net.get('s2')
	s2.cmd( 'ifconfig s2 10.0.0.51' )
	s3 = net.get('s3')
        s3.cmd( 'ifconfig s3 10.0.0.52' )
	s4 = net.get('s4')
        s4.cmd( 'ifconfig s4 10.0.0.53' )
	s5 = net.get('s5')
        s5.cmd( 'ifconfig s5 10.0.0.54' )
	s6 = net.get('s6')
        s6.cmd( 'ifconfig s6 10.0.0.55' )
	s7 = net.get('s7')
        s7.cmd( 'ifconfig s7 10.0.0.56' )
	s8 = net.get('s8')
        s8.cmd( 'ifconfig s8 10.0.0.57' )
	s9 = net.get('s9')
        s9.cmd( 'ifconfig s9 10.0.0.58' )
	s10 = net.get('s10')
        s10.cmd( 'ifconfig s10 10.0.0.59' )
	s11 = net.get('s11')
        s11.cmd( 'ifconfig s11 10.0.0.60' )
	s12 = net.get('s12')
        s12.cmd( 'ifconfig s12 10.0.0.61' )
	s13 = net.get('s13')
        s13.cmd( 'ifconfig s13 10.0.0.62' )
	"""

	"Start the controller in 'server' host"
	global controller_host 
	controller_host = hosts_list[-1]
	#info( controller_host.cmd( 'controller -v ptcp:6633 &' ) )

	"Fetch the listener host in the network"
	global server_host 
	server_host = hosts_list[-2]
	server_host.cmd( 'pwd' )

	"Start the listener script in the listener host"
	#info( server_host.cmd( './listener.sh &' ) )
	#server_host.cmd( 'while true; do nc -l -p 2222; done > /home/mininet/mininet/custom/dump.txt &' )

	"Start the sender script in the remaining hosts"
	#del hosts_list [0]
	#num_sender_hosts = num_hosts-2
	#print num_sender_hosts
	#for n in hosts_list[:num_sender_hosts]:
		#server_host.cmd( 'while true; do nc -l -p 2222; done > /home/mininet/mininet/custom/dump.txt &' )
		#info( n.cmd( 'ifconfig | grep inet' ) )
		#n.cmd( './sender.sh &' )

	#CLI( net )
	#net.stop()

def test_run():
	num_sender_hosts = num_hosts-2
	print num_sender_hosts
	print controller_host
	controller_host.cmd( 'cd ~' )
	#info( controller_host.cmd( 'pwd' ) )
	controller_host.cmd( '*nohup controller -v ptcp:6633 &' ) 
	#print server_host
	#server_host.cmd( 'nohup ncat -l 2222 --keep-open >> /home/mininet/mininet/custom/dump.txt &' )
	#net.pingAll()

	CLI( net )	
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	topo_init()
	test_run()	

