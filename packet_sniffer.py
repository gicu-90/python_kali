#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http 

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            try:
                if isinstance(load, (bytes, bytearray)):
                    load = load.decode('utf-8')
            except 
            #if "username" in str(load):
            #    print(load)
            print(load)


sniff("eth0")
