import psutil
import socket  # For AF_INET
from ipaddress import IPv4Address, IPv4Network
import logging

def guess_own_iface(match_ips):
    if len(match_ips) == 0:
        return None

    for iface, addrs in psutil.net_if_addrs().items():
        # Get the MAC address (psutil gives it directly without needing AF_PACKET)
        mac = None
        ipv4_addr = None
        netmask = None

        for addr in addrs:
            # Check for MAC address
            if addr.family == psutil.AF_LINK:  # For Unix-like systems, AF_LINK is provided by psutil
                mac = addr.address

            # Check for IPv4 addresses
            if addr.family == socket.AF_INET:  # Use socket.AF_INET for IPv4 addresses
                ipv4_addr = addr.address
                netmask = addr.netmask

        if mac is None:
            logging.debug(f"{iface} has no MAC address, skipped.")
            continue

        if ipv4_addr is None or netmask is None:
            logging.warning(f"{iface} has no IPv4 address or netmask")
            continue

        logging.debug(f"Checking interface {iface}: {ipv4_addr}/{netmask}, MAC: {mac}")

        # Check if the IP address is in the specified networks
        net = IPv4Network(f"{ipv4_addr}/{netmask}", strict=False)
        if any(IPv4Address(ip) in net for ip in match_ips):
            return iface, ipv4_addr, netmask, mac

    return None
