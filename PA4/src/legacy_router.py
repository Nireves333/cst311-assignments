#!env python

from mininet.net import Mininet
from mininet.node import Host, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNetwork():
  
  net = Mininet( topo=None,
                 build=False,
                 ipBase='10.0.0.0/8')
  
  info( '*** Adding controller\n' )
  info( '*** Add switches\n')
  r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
  r1.cmd('sysctl -w net.ipv4.ip_forward=1')
  
  info( '*** Add hosts\n')
  h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
  h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
  
  info( '*** Add links\n')
  net.addLink(h1, r1)
  net.addLink(h2, r1)
  
  info( '*** Starting network\n')
  net.build()
  
  CLI(net)
  net.stop()

if __name__ == '__main__':
  setLogLevel( 'info' )
myNetwork()