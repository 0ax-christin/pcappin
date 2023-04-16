from scapy.all import *
from collections import Counter
from prettytable import PrettyTable
import plotly
import plotly.express as px
import os
import re
import basedir
import sys
import pickle
subnet_interface = {
    "vmx0" : '^192\.168\.4\.([1-9]?\d|[12]\d\d)$',
    "vmx1" : '^192\.168\.0\.([1-9]?\d|[12]\d\d)$',
    "vmx2" : '^192\.168\.5\.([1-9]?\d|[12]\d\d)$',
    "vmx3" : '^192\.168\.6\.([1-9]?\d|[12]\d\d)$',
    #"vmx4" : '172.16.2.1',
    "vmx5" : '^192\.168\.2\.([1-9]?\d|[12]\d\d)$',
    #"vmx6" : '192.168.1.71'
    }
#https://stackoverflow.com/questions/2578022/python-2-5-2-trying-to-open-files-recursively

# Given a directory to search, find all filenames and return back the list of full filepaths
def generateFilePathList(walk_dir):
    filePaths = {}
    for dir in os.listdir(walk_dir):
        filePaths[dir] = []
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            currentDirFile = os.path.join(root, filename)
            currentDir = os.path.basename(os.path.dirname(currentDirFile))
            if currentDir in filePaths:
                filePaths[currentDir].append(currentDirFile)
    return filePaths

# Given a list of files, read them with scapy and append these files into a list to be returned
def generatedOpenedFileList(filePaths):
    scapy_file_opened = {}
    for file in filePaths:
        for directory, filename in file:
            scapy_file_opened[directory] = rdpcap(file)
    return scapy_file_opened

# Given a list of files opened by scapy, iterate through each files individual packets, note down src IPs into a dictionary key.
# As dictionary keys must be unique, repitition of same src IP is avoided. Each packets src IP is checked to see if it already exists
# If it does, the value of the dictionary key of that IP is incremented
# If not, it is initialized
def generateSrcIPCount(scapy_file_opened):
    srcIPCount = {}
    for packetList in scapy_file_opened:
        for packet in packetList:
            if IP in packet:
                try:
                    if packet[IP].src in srcIPCount:
                        srcIPCount[packet[IP].src] += 1
                    else:
                        srcIPCount[packet[IP].src] = 0
                except:
                    pass
    return srcIPCount

#Given a dictionary with keys of src IP and values of count of packets, split into multiple keys of a dictionary based on router interface
# and the associated subnet of that interface
def createVmxSrcList(srcIPCountDict, interface):
    vmxSrcList = {
        interface: {}
    }
    print(vmxSrcList)
    for key, value in srcIPCountDict.items():
        if re.search(subnet_interface['vmx0'], key) != None and interface == 'vmx0':
            vmxSrcList['vmx0'][key] = value
        elif re.search(subnet_interface['vmx1'], key) != None and interface == 'vmx1':
            vmxSrcList['vmx1'][key] = value
        elif re.search(subnet_interface['vmx2'], key) != None and interface == 'vmx2':
            vmxSrcList['vmx2'][key] = value
        elif re.search(subnet_interface['vmx3'], key) != None and interface == 'vmx3':
            print(key, value, interface)
            vmxSrcList[interface][key] = value
        elif re.search(subnet_interface['vmx5'], key) != None and interface == 'vmx5':
            vmxSrcList['vmx5'][key] = value
    return vmxSrcList

# for key, value in srcIPCount.items():
#     if re.search(subnet_interface["vmx0"], key) or re.search(subnet_interface["vmx1"], key) or re.search(subnet_interface["vmx2"], key) or re.search(subnet_interface["vmx3"], key) or re.search(subnet_interface["vmx5"], key) == None:
#         srcIPCount.pop(key)

# Creating Plots with plotly per Subnet
# Requires a dictionary where keys are router interfaces and values are the associated subnet src IP counts
def createBarGraph(vmxSrcList):
    for vmxKey in vmxSrcList.keys():
        xData = []
        yData = []
        for key, value in vmxSrcList[vmxKey].items():
            xData.append(key)
            yData.append(value)
        plotly.offline.plot(
            {
                "data": [plotly.graph_objs.Bar(x=xData, y=yData)],
            },
            filename = "{}/files/{}_srcIP_summary.html".format(basedir.fileWriteDir, vmxKey)
        )

def createScatterPlot(vmxSrcList):
    for vmxKey in vmxSrcList.keys():
        xData = []
        yData = []
        for key, value in vmxSrcList[vmxKey].items():
            xData.append(key)
            yData.append(value)
        # plot = px.scatter(xData, yData)
        # plot.show()
        plotly.offline.plot(
            {
                "data": [plotly.graph_objs.Scatter(x=xData, y=yData)],
            },
            filename = "{}/files/{}_srcIP_scatter.html".format(basedir.fileWriteDir, vmxKey)
        )

def clearEmptyDictListValues(dicte):
    for interface in dicte.copy().keys():
        if not dicte[interface]:
            dicte.pop(interface)
    return dicte

def main():
    walk_dir = '{}/Router/'.format(basedir.baseDir)
    fileOpenedPaths = generateFilePathList(walk_dir)
    fileOpenedPaths = clearEmptyDictListValues(fileOpenedPaths)
    print(fileOpenedPaths)
    for interface in fileOpenedPaths.keys():
        opened_files = []

        for fileNames in fileOpenedPaths[interface]:
            opened_files.append(rdpcap(fileNames))
        srcIPCount = generateSrcIPCount(opened_files)
        vmxSrcList = createVmxSrcList(srcIPCount, interface)
        createBarGraph(vmxSrcList)
        #createScatterPlot(vmxSrcList)
    # srcIPCount = generateSrcIPCount(scapy_file_opened)
    # vmxSrcList = createVmxSrcList(srcIPCount)
    # with open("vmxSrcList.pickle", "wb") as outfile:    
    #     pickle.dump(vmxSrcList, outfile)
    # with open("test.pickle", "rb") as infile:
    #     vmxSrcList_dict_reconstructed = pickle.load(infile)
    
    #screateBarGraph(vmxSrcList)

if __name__ == "__main__":
    main()