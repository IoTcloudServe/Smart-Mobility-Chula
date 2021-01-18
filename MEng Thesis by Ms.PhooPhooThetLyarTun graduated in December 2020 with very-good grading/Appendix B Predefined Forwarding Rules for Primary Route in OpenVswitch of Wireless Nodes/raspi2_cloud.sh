raspi1="e8:4e:06:5e:6b:09"
raspi2="e8:4e:06:5f:47:59"
raspi3="e8:4e:06:40:d3:7f"
raspi4="e8:4e:06:40:d3:db"
raspi5="e8:4e:06:40:dc:62"
raspi6="e8:4e:06:40:94:20"
gw2="e8:4e:06:40:d1:c7"
gw1="e8:4e:06:40:d3:4b"
sdncloud="00:26:b9:ce:d3:e1"
broadcast="ff:ff:ff:ff:ff:ff"
interface="wlan0"
#laninterface="enx00ea4c6d58ef"
controller_ip="10.0.0.8"
gateway1_ip="10.0.0.8"
gateway2_ip="10.0.0.9"
raspi1_ip="10.0.0.1"
raspi2_ip="10.0.0.2"
raspi3_ip="10.0.0.3"
raspi4_ip="10.0.0.4"
raspi5_ip="10.0.0.5"
raspi6_ip="10.0.0.6"
sdncloud_ip="161.200.90.120"
sleep 3
sudo ovs-vsctl --if-exist del-br br0
#bridge is added to OpenVswitch
sudo ovs-vsctl add-br br0
sudo ovs-vsctl set bridge br0 other-config:datapath-id=1000000000000002
#Configure OpenVswitch in Userspace of Linux
sudo ovs-vsctl set bridge br0 datapath_type=netdev
#added wireless interface under bridge in OpenVswitch
sudo ovs-vsctl add-port br0 $interface -- set Interface $interface ofport_request=1
sudo ifconfig $interface 0
sudo ifconfig br0 $raspi2_ip netmask 255.0.0.0 up
sudo iptables -A INPUT -i $interface -j DROP #Required to do only OpenVswitch in userspace mode
sudo iptables -A FORWARD -i $interface -j DROP #Required to do only OpenVswitch in userspace mode
#Connect to RYU controller
sudo ovs-vsctl set-controller br0 tcp:$sdncloud_ip:6633
sudo ovs-vsctl set controller br0 connection-mode=out-of-band
sudo ovs-vsctl set-fail-mode br0 secure
sudo ovs-vsctl set bridge br0 stp_enable=true
#Receive the incoming traffic to Raspi 2 (10.0.0.2) from Raspi 1, Raspi 5 and Raspi 3
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi5,arp_tpa=$raspi2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi1,arp_tpa=$raspi2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi3,arp_tpa=$raspi2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi5,nw_dst=$raspi2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi1,nw_dst=$raspi2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi3,nw_dst=$raspi2_ip,actions=LOCAL
#Send the packet from Raspi 2 to other wireless node
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_spa=$raspi2_ip,actions="resubmit(,1)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi1_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi3_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi5_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=LOCAL,nw_src=$raspi2_ip,actions="resubmit(,1)"
#Relay the incoming traffic to other wireless nodes not to Raspi 2
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi3,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi1,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi3,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi1,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi3,nw_dst=$gateway1_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi1,nw_dst=$raspi3_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi1,nw_dst=$gateway2_ip,actions="resubmit(,4)"
#Table 1 is to rewrite the destination MAC address into broadcast MAC address
sudo ovs-ofctl add-flow br0 table=1,actions=mod_dl_dst:$broadcast,"resubmit(,5)"
#Table 2 is to rewrite the destination MAC address into Raspi 5's MAC address
sudo ovs-ofctl add-flow br0 table=2,actions=mod_dl_dst:$raspi5,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 3 is to rewrite the destination MAC address into Raspi 1's MAC address
sudo ovs-ofctl add-flow br0 table=3,actions=mod_dl_dst:$raspi1,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 4 is to rewrite the destination MAC address into Raspi 3's MAC address
sudo ovs-ofctl add-flow br0 table=4,actions=mod_dl_dst:$raspi3,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 5 is to forward to wireless interface
sudo ovs-ofctl add-flow br0 table=5,actions=output:1
#To prevent the infinite loop
sudo ovs-ofctl add-flow br0 priority=1,in_port=1,actions=drop
sudo route add -host $sdncloud_ip gw $raspi5_ip
sudo sysctl -p
