from scapy.all import *
from scapy.contrib.gtp import GTP_U_Header

data= "OpenairInterface Software Alliance - downlink"

sendp(Ether(src="02:42:c0:a8:40:c6",dst="00:0c:29:46:1f:53")/
	IP(src="192.168.64.198",dst="20.20.20.20",version=4)/
	UDP()/data, iface="sgi")
