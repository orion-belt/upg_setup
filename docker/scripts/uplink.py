from scapy.all import *
from scapy.contrib.gtp import GTP_U_Header

data= "OpenairInterface Software Alliance"

sendp(Ether(src="02:42:c0:a8:3e:c6",dst="00:0c:29:46:1f:55")/
	IP(src="192.168.62.198",dst="192.168.62.201")/
	UDP(dport=2152)/GTP_U_Header(teid=9689)/
	IP(src="10.10.10.10",dst="192.168.64.198",version=4)/
	UDP()/data, iface="access")

