from scapy.utils import rdpcap, wrpcap
from scapy.utils import PcapReader, PcapWriter
from scapy.layers.inet import IP, TCP, UDP  # import needed!
import trimpcap
import sys, os
import basedir
from pathlib import Path

def generateFileList(walk_dir):
    fileList = []
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            currentDirFile = os.path.join(root, filename)
            currentDir = os.path.basename(os.path.dirname(currentDirFile))
            fileList.append(currentDirFile)
    return fileList

def removed_payload(file):
    packets = PcapReader(file)
    new_packets = []
    for packet in packets:
        if packet.haslayer("IP"):
            if packet.haslayer("TCP"):
                packet["IP"]["TCP"].remove_payload()
            elif packet.haslayer("UDP"):
                packet["IP"]["UDP"].remove_payload()
        new_packets.append(packet)
    return new_packets

def main():
    walk_dir = '{}/'.format(basedir.baseDir)
    fileList = generateFileList(walk_dir)
    print(fileList)
    for file in fileList:
        packetWrite = removed_payload(file)
        currentDir = os.path.dirname(file)
        dirBaseName = os.path.basename(currentDir)
        fileName = os.path.basename(file)
        Path(f"{currentDir}/stripped_pcaps").mkdir(parents=True, exist_ok=True)
        PcapWriter(f"{currentDir}/stripped_pcaps/{fileName}", packetWrite)

if __name__ == "__main__":
    main()