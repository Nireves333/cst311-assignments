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
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf


def myNetwork():
    # Create mininet object with network configuration
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/24')

    # Add a controller to the network
    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    # Add switches to the network
    info('*** Add switches\n')
    # Reordered in sequential order (s1 then s2) and moved addSwitch lines to instantiate switches before the routers
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    # Add routers to the network and enable IP forwarding
    # Re-ordered router instantiation in sequential order to r3, r4, then r5
    # Added IP address(s) for each router, per assignment rules 1 - 4.
    r3 = net.addHost('r3', cls=Node, ip='10.0.1.1/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip=['192.168.1.2/30', '192.168.1.5/30'])
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='10.0.2.1/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Use the intfName and params, because you cannot assign IP addresses to legacy routers in MiniEdit.
    # This allows us to assign an IP address to the indicated interface and which node of the pair.
    # Add router-switch links that are in the same subnet
    net.addLink(s1, r3, intfName2='r3-eth0', params2={'ip': '10.0.1.1/24'})
    net.addLink(s2, r5, intfName2='r5-eth0', params2={'ip': '10.0.2.1/24'})

    # Add router-router link for the router-router connection
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

    # Add hosts to the network
    info('*** Add hosts\n')
    # Updated IP for each host per assignment rules 1 -2.
    # Hosts h1 and h2 and the router r3 interface connected to s1 will be on a
    # 254-host network with the private IPv4 address of 10.0.x.0/24. (You choose the value of x.)
    # Hosts h3 and h4 and the router r5 interface connected to s2 will be on a network with the
    # private IPv4 address of 10.0.y.0/24. (You choose the value of y.)
    # For each host, added default route specified as connected router (h1 and h2 with r3; h3 and h4 with r5)
    h1 = net.addHost('h1', ip='10.0.1.50/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.1.100/24', defaultRoute='via 10.0.1.1')
    h3 = net.addHost('h3', ip='10.0.2.50/24', defaultRoute='via 10.0.2.1')
    h4 = net.addHost('h4', ip='10.0.2.100/24', defaultRoute='via 10.0.2.1')

    # Add host-switch links
    info('*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)

    # Add routing for reaching networks that aren't directly connected
    # Static routes for each router in order to make the network work by
    # defining a path that a packet must travel through from a router to get to a certain destination
    net['r3'].cmd("ip route add 10.0.2.0/24 via 192.168.1.2 dev r3-eth1")
    net['r3'].cmd("ip route add 192.168.1.0/24 via 192.168.1.2 dev r3-eth1")

    net['r4'].cmd("ip route add 10.0.1.0/24 via 192.168.1.1 dev r4-eth0")
    net['r4'].cmd("ip route add 10.0.2.0/24 via 192.168.1.6 dev r4-eth1")

    net['r5'].cmd("ip route add 10.0.1.0/24 via 192.168.1.5 dev r5-eth1")
    net['r5'].cmd("ip route add 192.168.1.0/30 via 192.168.1.5 dev r5-eth1")

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info('*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
