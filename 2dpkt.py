import dpkt

with open('greyteam-tcpdump_2023-03-27_16-04-50.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)

    # Iterate over the packets
    for ts, buf in pcap:
        # Unpack the Ethernet frame
        eth = dpkt.ethernet.Ethernet(buf)

# Extract the IP packets
ip_packets = [eth.data for eth in eth_packets if isinstance(eth.data, dpkt.ip.IP)]

# Extract the TCP packets
tcp_packets = [ip.data for ip in ip_packets if isinstance(ip.data, dpkt.tcp.TCP)]

src_ips = set()
# Extract the source IP addresses
src_ips.add([ip.src for ip in ip_packets])

print(src_ips)
# Extract the destination ports
#dst_ports = [tcp.dport for tcp in tcp_packets]

# Print the information
#for src, dst in zip(src_ips, dst_ports):
   # print(f'Source IP: {src} Destination Port: {dst}')