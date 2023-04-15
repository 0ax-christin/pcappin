from scapy.all import *
from collections import Counter
from prettytable import PrettyTable
import plotly

packets = rdpcap('pcaps/greyteam-tcpdump_2023-03-27_16-04-50.pcap')
#packets = PcapReader('greyteam-tcpdump_2023-03-27_16-04-50.pcap')
srcIP = {}
for packet in packets:
    if IP in packet:
        try:
            if packet[IP].src in srcIP:
                srcIP[packet[IP].src] += 1
            else:
                srcIP[packet[IP].src] = 0
        except:
            pass

print(srcIP)
