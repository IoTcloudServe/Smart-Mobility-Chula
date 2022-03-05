raspi1="e8:4e:06:5e:6b:09"
raspi2="e8:4e:06:5f:47:59"
raspi3="e8:4e:06:40:d3:7f"
raspi4="e8:4e:06:40:d3:db"
raspi5="e8:4e:06:5e:6a:b1"
raspi6="e8:4e:06:40:94:20"
gw2="e8:4e:06:40:d1:c7"
#gw2="e8:4e:06:40:dc:62"
gw1="e8:4e:06:40:d3:4b"
sdncloud="00:26:b9:ce:d3:e1"
broadcast="ff:ff:ff:ff:ff:ff"
interface="wlan0"
laninterface="enx00ea4c6d58ef"
gateway1_ip="10.0.0.8"
gateway2_ip="10.0.0.9"
raspi1_ip="10.0.0.1"
raspi2_ip="10.0.0.2"
raspi3_ip="10.0.0.3"
raspi4_ip="10.0.0.4"
raspi5_ip="10.0.0.5"
raspi6_ip="10.0.0.6"
sdncloud_ip="192.168.1.6"
sleep 3
sudo ovs-vsctl --if-exists del-br br0
#Bridge is added to OpenVswitch
sudo ovs-vsctl add-br br0
sudo ovs-vsctl set bridge br0 other-config:datapath-id=1000000000000003
#Configure OpenVswitch in Userspace of Linux
sudo ovs-vsctl set bridge br0 datapath_type=netdev
#Added wireless interface under bridge in OpenVswitch
sudo ovs-vsctl add-port br0 $interface -- set Interface $interface ofport_request=1
sudo ifconfig $interface 0
sudo iptables -A INPUT -i $interface -j DROP #For only OpenVswitch in userspace
sudo iptables -A FORWARD -i $interface -j DROP #For only OpenVswitch in userspace
sudo ifconfig br0 $raspi3_ip netmask 255.0.0.0 up
#Connect to RYU controller
sudo ovs-vsctl set-controller br0 tcp:$sdncloud_ip:6633
sudo ovs-vsctl set controller br0 connection-mode=out-of-band
sudo ovs-vsctl set-fail-mode br0 secure
sudo ovs-vsctl set bridge br0 protocol=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
#Receive the incoming traffic to Raspi 3 (10.0.0.3) from Raspi 2, Raspi 6 and Gateway 2
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi2,arp_tpa=$raspi3_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi6,arp_tpa=$raspi3_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$gw2,arp_tpa=$raspi3_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi2,nw_dst=$raspi3_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi6,nw_dst=$raspi3_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$gw2,nw_dst=$raspi3_ip,actions=LOCAL
#Send the packet from Raspi 3 to other wireless node
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_spa=$raspi3_ip,actions="resubmit(,1)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$gateway2_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi6_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi2_ip,actions=output:1
sudo ovs-ofctl add-flow br0 arp,priority=96,in_port=LOCAL,arp_tpa=$sdncloud_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=96,in_port=LOCAL,nw_dst=$sdncloud_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=LOCAL,nw_src=$raspi3_ip,actions="resubmit(,3)"
#To prevent duplicate message from Gateway 2 to Gateway 1
sudo ovs-ofctl add-flow br0 arp,priority=95,in_port=1,dl_src=$gw2,arp_tpa=$gateway1_ip,actions=drop
sudo ovs-ofctl add-flow br0 ip,priority=95,in_port=1,dl_src=$gw2,nw_dst=$gateway1_ip,actions=drop
#Relay the incoming traffic to other wireless nodes not to Raspi 3
sudo ovs-ofctl add-flow br0 ip,priority=110,in_port=1,dl_src=$raspi2,nw_dst=$sdncloud_ip,actions=drop
sudo ovs-ofctl add-flow br0 arp,priority=110,in_port=1,dl_src=$raspi2,arp_tpa=$sdncloud_ip,actions=drop
sudo ovs-ofctl add-flow br0 arp,priority=80,in_port=1,dl_src=$raspi2,nw_dst=$gateway2_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=80,in_port=1,dl_src=$raspi2,arp_tpa=$gateway2_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 arp,priority=80,in_port=1,dl_src=$gw2,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=80,in_port=1,dl_src=$gw2,actions="resubmit(,3)"
#Table 1 is to rewrite the destination MAC address into broadcast MAC address
sudo ovs-ofctl add-flow br0 table=1,actions=mod_dl_dst:ff:ff:ff:ff:ff:ff,"resubmit(,5)"
#Table 2 is to rewrite the destination MAC address into Raspi 6's MAC address
sudo ovs-ofctl add-flow br0 table=2,actions=mod_dl_dst:$raspi6,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 3 is to rewrite the destination MAC address into Raspi 2's MAC address
sudo ovs-ofctl add-flow br0 table=3,actions=mod_dl_dst:$raspi2,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 4 is to rewrite the destination MAC address into Gateway 2's MAC address
sudo ovs-ofctl add-flow br0 table=4,actions=mod_dl_dst:$gw2,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 5 is to forward to wireless interface
sudo ovs-ofctl add-flow br0 table=5,actions=output:1
#To prevent the infinite loop
sudo ovs-ofctl add-flow br0 priority=1,in_port=1,actions=drop
sudo route add default gw $gateway2_ip
#sudo route add -host $sdncloud_ip gw $gateway2_ip
sudo sysctl -p
