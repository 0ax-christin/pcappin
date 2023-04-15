from scapy.all import *

packets = rdpcap('greyteam-tcpdump_2023-03-27_16-04-50.pcap')

src_ips = set()
for pkt in packets:
    if IP in pkt:
        try:
            src_ips.add(pkt[IP].src)
        except:
            pass

print(src_ips)