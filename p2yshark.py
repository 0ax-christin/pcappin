import pyshark

def print_highest_layer(pkt):
    print(pkt.highest_layer)

cap = pyshark.FileCapture('greyteam-tcpdump_2023-03-27_16-04-50.pcap')

src_ips = set()
src_ips.add(packet.ip.src for packet in cap)

print(src_ips)