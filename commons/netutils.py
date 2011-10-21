#!/usr/bin/env python
import pdb
import socket
import platform
import web

# http://en.wikipedia.org/wiki/IP_address

__all__ = ['IANA_RESERVED_NETWORK_RANGES',
           'get_lan_ip',
           'get_default_network_range',
           'ip_in_network_range', 'ip_in_network_ranges',
           ]

IANA_RESERVED_NETWORK_RANGES = ("10.0.0.0/24", "172.16.0.0/20", "192.168.0.0/16")

def get_lan_ip():
    """ Return LAN IP address.
    http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

    TODO:
    fix issue - it doesn't works when connect to network via PPPoE(it returns WAN IP)
    """
    if platform.system() == "Darwin":
        return _get_lan_ip_on_mac()
    elif platform.system() == "Linux":
        return _get_lan_ip_on_linux

def _get_lan_ip_on_mac():
    """ Return LAN IP address, it works on box that behinds router/firewall.
    """
    return socket.gethostbyname(socket.gethostname())

def _get_lan_ip_on_linux():
    """ Return LAN IP address, it works on box that behinds router/firewall.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("baidu.com", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def get_default_network_range(lan_ip=None):
    """ Return IANA reserved private network range(such as '192.168.0.0/16') if your box behinds router or firewall,
    else return '127.0.0.1'.

    >>> get_default_network_range('192.168.0.123')
    '192.168.0.0/16'
    >>> get_default_network_range('10.1.2.3')
    '10.0.0.0/24'
    >>> get_default_network_range('172.16.0.40')
    '172.16.0.0/20'
    """

    if not lan_ip:
        lan_ip = get_lan_ip()

    ip_is_in_reserved = False

    for i in IANA_RESERVED_NETWORK_RANGES:
        if ip_in_network_range(lan_ip, i):
            ip_is_in_reserved = True

    network_range = None
    if ip_is_in_reserved:
        if lan_ip.startswith("10."):
            network_range = "10.0.0.0/24"
        elif lan_ip.startswith("172.16."):
            network_range = "172.16.0.0/20"
        elif lan_ip.startswith("192.168."):
            network_range = "192.168.0.0/16"
    else:
        network_range = '127.0.0.1'

    return network_range

def ip_in_network_ranges(ip, network=None):
    """ Return True if `ip` is part of the network specify in network
    http://www.netfilter.org/documentation/HOWTO//networking-concepts-HOWTO-4.html

    >>> ip_in_network_ranges('127.0.0.1')
    True
    >>> ip_in_network_ranges('192.168.0.1')
    True
    >>> ip_in_network_ranges('10.0.0.1')
    True
    >>> ip_in_network_ranges('444.444.0.0')
    False
    >>> ip_in_network_ranges('192.168.0.1', network=('192.168.0.0/8',))
    True
    >>> ip_in_network_ranges('121.33.140.181', network=('192.168.0.0/8',))
    False
    """
    if not web.net.validipaddr(ip):
        return False

    if not network:
        network = ("0.0.0.0",)

    if network == ("0.0.0.0",):
        return True

    if ip == "127.0.0.1":
        return True

    for i in network:
        if not ip_in_network_range(ip, i):
            return False

    return True

def ip_in_network_range(ip, network_range):
    netmask = None
    if network_range.find('/') != -1:
        splits = network_range.split('/')
        netmask = int(splits[1])
        network_ip = splits[0]
    else:
        network_ip = network_range

    if netmask:
        subnet_class_prefix_parts = network_ip.split('.')[:-(netmask / 8)]
        if not ip.startswith("172."):
            if not ip.startswith('.'.join(subnet_class_prefix_parts)):
                return False
        else:
            pass

        parts_a = network_ip.split('.')[netmask/8 : ]
        parts_b = ip.split('.')[netmask/8 : ]

        for i in xrange(len(parts_b)):
            if len(parts_b) != i + 1:
                if int(parts_a[i]) != int(parts_b[i]):
                    return False
            else:
                a = int(parts_b[i])
                end = 255

                if netmask % 8 != 0:
                    start = 255 - eval('0b' + (32 - netmask) % 8 * '1')
                else:
                    start = 0

                if a > end or a < start:
                    return False

        return True

    elif ip == network_ip:
        return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
