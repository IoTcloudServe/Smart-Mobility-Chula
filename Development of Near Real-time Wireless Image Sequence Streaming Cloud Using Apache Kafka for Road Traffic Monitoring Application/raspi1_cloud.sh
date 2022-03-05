raspi1="e8:4e:06:5e:6b:09"
raspi2="e8:4e:06:5f:47:59"
raspi3="e8:4e:06:40:d3:7f"
raspi4="e8:4e:06:40:d3:db"
raspi5="e8:4e:06:5e:6a:b1"
raspi6="e8:4e:06:40:94:20"
gw2="e8:4e:06:40:d1:c7"
gw1="e8:4e:06:40:d3:4b"
sdncloud="00:26:b9:ce:d3:e1"
broadcast="ff:ff:ff:ff:ff:ff"
interface="wlan0"
laninterface="enx00ea4c6d58ef"
#controller_ip="10.0.0.8"
gateway1_ip="10.0.0.8"
gateway2_ip="10.0.0.9"
raspi1_ip="10.0.0.1"
raspi2_ip="10.0.0.2"
raspi3_ip="10.0.0.3"
raspi4_ip="10.0.0.4"
raspi5_ip="10.0.0.5"
raspi6_ip="10.0.0.6"
sdncloud_ip="192.168.1.6"

#sleep 3 #sleep is required to make sure the command line inside the rc.local file execute at the bootstrapping stage
sudo ovs-vsctl --if-exists del-br br0
#bridge is added to OpenVswitch
sudo ovs-vsctl add-br br0
sudo ovs-vsctl set bridge br0 other-config:datapath-id=1000000000000001
#Configure OpenVswitch in Userspace of Linux
sudo ovs-vsctl set bridge br0 datapath_type=netdev #Set OpenVswitch in userspace
#added wireless interface under bridge in OpenVswitch
sudo ovs-vsctl add-port br0 $interface -- set Interface $interface ofport_request=1
sudo ifconfig br0 $raspi1_ip netmask 255.0.0.0 up
sudo ifconfig $interface 0
sudo iptables -A INPUT -i $interface -j DROP #For only OpenVswitch in userspace
sudo iptables -A FORWARD -i $interface -j DROP #For only OpenVswitch in userspace
#Connect to RYU controller
sudo ovs-vsctl set-controller br0 tcp:$sdncloud_ip:6633
sudo ovs-vsctl set controller br0 connection-mode=out-of-band
sudo ovs-vsctl set-fail-mode br0 secure
#Receive the incoming traffic to Raspi 1 (10.0.0.1) from Raspi 2, Raspi 4 and Gateway 1
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$gw1,arp_tpa=$raspi1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi2,arp_tpa=$raspi1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi4,,arp_tpa=$raspi1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$gw1,nw_dst=$raspi1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi2,nw_dst=$raspi1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi4,nw_dst=$raspi1_ip,actions=LOCAL
#Send the packet from Raspi 1 to other wireless node
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_tpa=$gateway1_ip,actions=output:1
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_tpa=$raspi4_ip,actions=output:1
sudo ovs-ofctl add-flow br0 arp,priority=95,in_port=LOCAL,arp_tpa=$sdncloud_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=LOCAL,arp_spa=$raspi1_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$gateway1_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi4_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=95,in_port=LOCAL,nw_dst=$sdncloud_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=LOCAL,nw_src=$raspi1_ip,actions="resubmit(,4)"
#Relay the incoming traffic to other wireless nodes not to Raspi 1
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi2,arp_spa=$raspi2_ip,arp_tpa=$gateway1_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$gw1,arp_spa=$gateway1_ip,arp_tpa=$raspi2_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$gw1,nw_src=$gateway1_ip,nw_dst=$raspi2_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi2,nw_src=$raspi2_ip,nw_dst=$gateway1_ip,actions="resubmit(,3)"

sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi2,arp_spa=$raspi2_ip,arp_tpa=$sdncloud_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi2,nw_src=$raspi2_ip,nw_dst=$sdncloud_ip,actions="resubmit(,3)"

sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$gw1,arp_spa=$sdncloud_ip,arp_tpa=$raspi2_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$gw1,nw_src=$sdncloud_ip,nw_dst=$raspi2_ip,actions="resubmit(,4)"
#Table 3 is to rewrite the destination MAC address into Gateway 1's MAC address
sudo ovs-ofctl add-flow br0 table=3,actions=mod_dl_dst:$gw1,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 4 is to rewrite the destination MAC address into Raspi 2's MAC address
sudo ovs-ofctl add-flow br0 table=4,actions=mod_dl_dst:$raspi2,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
#Table 5 is to forward to wireless interface
sudo ovs-ofctl add-flow br0 table=5,actions=output:1
#To prevent the infinite loop
sudo ovs-ofctl add-flow br0 priority=1,in_port=1,actions=drop
sudo ovs-vsctl set bridge br0 protocol=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
sudo route add default gw $gateway1_ip
#sudo route add -host $sdncloud_ip gw $gateway2_ip
#sudo route add -host $sdncloud_ip gw $gateway1_ip
sudo sysctl -p

