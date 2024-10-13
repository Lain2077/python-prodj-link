import psutil
from ipaddress import IPv4Address, IPv4Network
import logging

def guess_own_iface(match_ips):
    if len(match_ips) == 0:
        return None

    for iface, addrs in psutil.net_if_addrs().items():
        # Get the link layer address (MAC)
        mac = None
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac = addr.address
                break  # Only need the first MAC address

        if mac is None:
            logging.debug("{} has no MAC address, skipped.".format(iface))
            continue

        # Check for IPv4 addresses
        ipv4_addr = None
        netmask = None
        for addr in addrs:
            if addr.family == psutil.AF_INET:
                ipv4_addr = addr.address
                # Try to retrieve the corresponding netmask
                for mask in addrs:
                    if mask.family == psutil.AF_INET and mask.address == ipv4_addr:
                        netmask = mask.netmask
                        break
                break  # Only need the first IPv4 address

        if ipv4_addr is None or netmask is None:
            logging.warning("{} has no IPv4 address or netmask".format(iface))
            continue

        # Check if the IP address is in the specified networks
        net = IPv4Network(f"{ipv4_addr}/{netmask}", strict=False)
        if any(IPv4Address(ip) in net for ip in match_ips):
            return iface, ipv4_addr, netmask, mac

    return None
