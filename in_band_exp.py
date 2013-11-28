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
    myTopo = TreeTopo( depth=2, fanout=8 )
    global net 
    net = Mininet( topo=myTopo, switch=OVSSwitch, build=False )
 
    "Creating Controller"
    c0 = net.addController( 'c0', controller=InbandController, ip='10.100.100.100' )
    net.start()
 
    "Adding a host for changing to controller"
    server = net.addHost( 'server', ip='10.100.100.100')    
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
 
    "Start the controller in 'server' host"
    global controller_host 
    controller_host = hosts_list[-1]

    "Fetch the listener host in the network"
    global server_host 
    server_host = hosts_list[-2]
 
def test_run():
    num_sender_hosts = num_hosts-9
    controller_host.cmd( 'cd ~' )
    controller_host.cmd( 'sudo tshark -w /var/tmp/tshark64_1K 2>&1 &' )
    server_ip = server_host.IP()
    ping_ip = hosts_list[-3].IP()
    controller_host.cmd( 'controller -v ptcp:6633 >>controller.txt 2>&1 &' ) 
    server_host.cmd( 'ncat -l 2222 --keep-open >>dump.txt 2>&1 &' )
    for n in hosts_list[:num_sender_hosts]:
            n.popen( 'sudo bash sender.sh 100 %s %s > sender.txt 2>&1 &' % (server_ip, ping_ip) )
    CLI( net )
 
    controller_host.cmd( 'pkill controller' )
    server_host.cmd( 'pkill ncat' )
    server_host.cmd( 'sudo rm ping.txt dump.txt' )          
    net.stop()
 
if __name__ == '__main__':
    setLogLevel('info')
    topo_init()
    test_run()  
