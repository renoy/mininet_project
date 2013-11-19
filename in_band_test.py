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

	"Start the controller in 'server' host"
	global controller_host 
	controller_host = hosts_list[-1]

	"Fetch the listener host in the network"
	global server_host 
	server_host = hosts_list[-2]

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
	controller_host.cmd( 'controller -v ptcp:6633 >controller.txt 2>&1 &' ) 
	print server_host
	server_host.cmd( 'ncat -l 2222 --keep-open > /home/mininet/mininet/custom/dump.txt 2>&1 &' )
	
        for n in hosts_list[:num_sender_hosts]:
                n.popen( './sender.sh 100 10.0.0.27 192.168.1.1 >sender.txt 2>&1 &' )
                #server_hosl.cmd( 'while true; do nc -l -p 2222; done > /home/mininet/mininet/custom/dump.txt &' )
	
	#net.pingAll()

	CLI( net )

	controller_host.cmd( 'pkill controller' )
		
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	topo_init()
	test_run()	

