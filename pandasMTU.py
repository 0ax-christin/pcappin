from scapy.all import *
import plotly
from datetime import datetime
import pandas as pd

packets = rdpcap('pcaps\greyteam-tcpdump_2023-03-27_16-04-50.pcap')

pktBytes = []
pktTimes = []

for pkt in packets:
    if IP in pkt:
        try:
            pktBytes.append(pkt[IP].len)

            pktTime = datetime.fromtimestamp(pkt.time)
            pktTimes.append(pktTime.strftime("%Y-%m-%d %H:%M:%S.%f"))
        except:
            pass

bytes = pd.Series(pktBytes).astype(int)

times = pd.to_datetime(pd.Series(pktTimes).astype(str), errors='coerce')

df = pd.DataFrame({"Bytes": bytes, "Times": times})

df = df.set_index('Times')
df2 = df.resample('2S').sum()
plotly.offline.plot({
    "data": [plotly.graph_objs.Scatter(x=df2.index, y=df2['Bytes'])],
    "layout": plotly.graph_objs.Layout(title="Bytes over Time", xaxis=dict(title="Time"), yaxis=dict(title="Bytes"))
}, filename="pandasScapy.html")