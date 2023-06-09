"""Legacy network for CST311 Programming Assignment 4"""
__author__ = "Team 3"
__credits__ = [
  "Andi Cameron",
  "Michelle Brown",
  "Nathan Simpson",
  "Severin Light"
]

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    # Moved addSwitch lines for instantiating switches before the routers, and changed order to s1, then s2
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Re-ordered router instantiation to r3, r4, then r5. Also assigned the IP address of the first node for each router.
    r3 = net.addHost('r3', cls=Node, ip='10.0.1.1/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    # r4 = net.addHost('r4', cls=Node, ip='192.168.1.2/30')
    r4 = net.addHost('r4', cls=Node, ip=['192.168.1.2/30', '192.168.1.5/30'])
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='10.0.2.1/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Add host-switch links in the same subnet
    net.addLink(s1,
                 r3,
                 intfName2='r3-eth0',
                 params2={'ip': '10.0.1.1/24'})

    net.addLink(s2,
                 r5,
                 intfName2='r5-eth0',
                 params2={'ip': '10.0.2.1/24'})

    # Add router-router link in a new subnet for the router-router connection
    net.addLink(r3,
                 r4,
                 intfName1='r3-eth1',
                 intfName2='r4-eth0',
                 params1={'ip': '192.168.1.1/30'},
                 params2={'ip': '192.168.1.2/30'})

    net.addLink(r4,
                 r5,
                 intfName1='r4-eth1',
                 intfName2='r5-eth1',
                 params1={'ip': '192.168.1.5/30'},
                 params2={'ip': '192.168.1.6/30'})

    # Adding hosts specifying the default route
    info('*** Add hosts\n')
    # Updated IP -
    # Hosts h1 and h2 and the router r3 interface connected to s1 will be on a
    # 254-host network with the private IPv4 address of 10.0.x.0/24. (You choose the value of x.)
    h1 = net.addHost('h1', ip='10.0.1.50/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.1.100/24', defaultRoute='via 10.0.1.1')
    # Hosts h3 and h4 and the router r5 interface connected to s2 will be on a network with the
    # private IPv4 address of 10.0.y.0/24. (You choose the value of y.)
    h3 = net.addHost('h3', ip='10.0.2.50/24', defaultRoute='via 10.0.2.1')
    h4 = net.addHost('h4', ip='10.0.2.100/24', defaultRoute='via 10.0.2.1')

    # Add host-switch links
    info('*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)

    # Add routing for reaching networks that aren't directly connected
    net['r3'].cmd("ip route add 10.0.1.0/24 via 10.0.1.1 dev r3-eth0")
    net['r3'].cmd("ip route add 10.0.2.0/24 via 192.168.1.2 dev r3-eth1")
    net['r3'].cmd("ip route add 192.168.1.0/24 via 192.168.1.2 dev r3-eth1")

    net['r4'].cmd("ip route add 10.0.1.0/24 via 192.168.1.1 dev r4-eth0")
    net['r4'].cmd("ip route add 10.0.2.0/24 via 192.168.1.6 dev r4-eth1")

    net['r5'].cmd("ip route add 10.0.2.0/24 via 10.0.2.1 dev r5-eth0")
    net['r5'].cmd("ip route add 10.0.1.0/24 via 192.168.1.5 dev r5-eth1")
    net['r5'].cmd("ip route add 192.168.1.0/30 via 192.168.1.5 dev r5-eth1")
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    
    # DELETE COMMENT LATER - ANDI ADDED - Code to run other parts (I think)
    # Create and issue certificate
    # h2.cmd('python3 /home/mininet/CST311/???.py')
    # Start h1, h2, h3, h4 terminals
    # makeTerm(h1, title='Client host 1', term='xterm', display=None, cmd='python3 /home/mininet/CST311/???.py')
    # makeTerm(h2, title='TLS-enabled webserver', term='xterm', display=None, cmd='python3 /home/mininet/CST311/???.py')
    # makeTerm(h3, title='Client host 2', term='xterm', display=None, cmd='python3 /home/mininet/CST311/???.py')
    # makeTerm(h4, title='TLS-enabled chat server', term='xterm', display=None, cmd='python3 /home/mininet/CST311/???.py')


    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
