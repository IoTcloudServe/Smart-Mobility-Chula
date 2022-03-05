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
laninterface="enx00ea4c6d54dd"
gateway1_ip="10.0.0.8"
gateway2_ip="10.0.0.9"
raspi1_ip="10.0.0.1"
raspi2_ip="10.0.0.2"
raspi3_ip="10.0.0.3"
raspi4_ip="10.0.0.4"
raspi5_ip="10.0.0.5"
raspi6_ip="10.0.0.6"
sdncloud_ip="192.168.1.6"

#To install the Primary OpenFlow Rules in Gateway 1
#sudo nano /etc/rc.local
sleep 3
sudo ovs-vsctl --if-exist del-br br0
#Bridge is added to OpenVswitch\
sudo ovs-vsctl add-br br0
#Configure OpenVswitch in Userspace of Linux
sudo ovs-vsctl set bridge br0 datapath_type=netdev
sudo ovs-vsctl set bridge br0 other-config:datapath_id=1000000000000008
#Added wireless interface under bridge in OpenVswitch
sudo ovs-vsctl add-port br0 $interface -- set Interface $interface ofport_request=1
sudo ovs-vsctl add-port br0 $laninterface -- set Interface $laninterface ofport_request=2
sudo ifconfig $interface 0
sudo ifconfig br0 $gateway1_ip netmask 255.0.0.0 up
sudo iptables -A INPUT -i $interface -j DROP #For only OpenVswitch in userspace
sudo iptables -A FORWARD -i $interface -j DROP #For only OpenVswitch in userspace
#Connect to RYU controller
sudo ovs-vsctl set-controller br0 tcp:$sdncloud_ip:6633
sudo ovs-vsctl set controller br0 connection-mode=out-of-band
sudo ovs-vsctl set-fail-mode br0 secure
sudo ovs-vsctl set bridge br0 protocol=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
sudo ovs-vsctl set bridge br0 stp_enable=true
sudo ovs-vsctl set bridge br0 other-config:hwaddr=$gw1
#Receive the incoming traffic to Gateway1 (10.0.0.3) coming from Raspi 1 and Raspi 4
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi1,arp_tpa=$gateway1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi1,nw_dst=$gateway1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi4,nw_dst=$gateway1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi4,arp_tpa=$gateway1_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi1,arp_tpa=$sdncloud_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi1,nw_dst=$sdncloud_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi4,nw_dst=$sdncloud_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi4,arp_tpa=$sdncloud_ip,actions="resubmit(,4)"


sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi2,arp_tpa=$sdncloud_ip,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi2,nw_dst=$sdncloud_ip,actions="resubmit(,4)"



sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=2,nw_dst=$raspi1_ip,actions=mod_dl_dst:$raspi1,"output:1"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=2,nw_dst=$raspi2_ip,actions=mod_dl_dst:$raspi1,"output:1"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=2,nw_dst=$raspi4_ip,actions=mod_dl_dst:$raspi4,"output:1"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=2,arp_tpa=$raspi1_ip,actions=mod_dl_dst:$raspi1,"output:1"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=2,arp_tpa=$raspi2_ip,actions=mod_dl_dst:$raspi1,"output:1"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=2,arp_tpa=$raspi4_ip,actions=mod_dl_dst:$raspi4,"output:1"
#Send the packet from Gateway1 to other wireless node
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_tpa=$raspi4_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_tpa=$raspi5_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_tpa=$raspi6_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=LOCAL,arp_spa=$gateway1_ip,actions="resubmit(,2)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi4_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi5_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi6_ip,actions="resubmit(,3)"
sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=LOCAL,nw_src=$gateway1_ip,actions="resubmit(,2)"

sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_tpa=$raspi2_ip,actions="resubmit(,2)"
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,nw_dst=$raspi2_ip,actions="resubmit(,2)"


#Table 2 is to rewrite the destination MAC address into Raspi 1's MAC address
sudo ovs-ofctl add-flow br0 table=2,actions=mod_dl_dst:$raspi1,"resubmit(,6)"
#Table 3 is to rewrite the destination MAC address into Raspi 4's MAC address
sudo ovs-ofctl add-flow br0 table=3,actions=mod_dl_dst:$raspi4,"resubmit(,6)"
#Table 4 is to rewrite the destination MAC address into SDN Cloud' MAC address
sudo ovs-ofctl add-flow br0 table=4,actions=mod_dl_dst:$sdncloud,"resubmit(,5)"
#Table 5 is to forward to ethernet interface
sudo ovs-ofctl add-flow br0 table=5,actions=output:2
#Table 6 is to forward to wireless interface
sudo ovs-ofctl add-flow br0 table=6,actions=output:1
#To prevent the infinite loop
sudo ovs-ofctl add-flow br0 priority=1,in_port=1,actions=drop
sudo sysctl -p
