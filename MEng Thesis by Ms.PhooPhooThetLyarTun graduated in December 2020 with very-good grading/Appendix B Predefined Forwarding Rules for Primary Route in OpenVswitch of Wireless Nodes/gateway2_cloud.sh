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

sudo ovs-vsctl --if-exist del-br br0
sudo ovs-vsctl add-br br0
sudo ovs-vsctl set bridge br0 other-config:datapath-id=1000000000000009
sudo ovs-vsctl set bridge br0 datapath_type=netdev
sudo ovs-vsctl add-port br0 $interface -- set Interface wlan0 ofport_request=1
#sudo ovs-vsctl add-port br0 $laninterface -- set Interface wlan0 ofport_request=1
sudo iptables -A INPUT -i $interface -j DROP
sudo iptables -A FORWARD -i $interface -j DROP
sudo ifconfig $interface 0
sudo ifconfig br0 $gateway2_ip netmask 255.0.0.0 up
sudo ovs-vsctl set-controller br0 tcp:$sdncloud_ip:6633
sudo ovs-vsctl set controller br0 connection-mode=out-of-band
sudo ovs-vsctl set-fail-mode br0 secure
sudo ovs-vsctl set bridge br0 other-config:hwaddr=$gw2
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi3,arp_tpa=$gateway2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=$raspi6,arp_tpa=$gateway2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi6,nw_dst=$gateway2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=$raspi3,nw_dst=$gateway2_ip,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_tpa=$gateway2_ip,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$gateway2_ip,actions=output:1


#sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi3_ip,actions=output:1
#sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,nw_dst=$raspi6_ip,actions=output:1
#sudo ovs-ofctl add-flow br0 ip,priority=95,in_port=LOCAL,nw_src=$gateway2_ip,actions="resubmit(,2)"
#sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,arp_spa=$gateway2_ip,actions="resubmit(,2)"
#sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi3,arp_tpa=$sdncloud_ip,actions="resubmit(,3)"
#sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi3,nw_dst=$sdncloud_ip,actions="resubmit(,3)"
#sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=1,dl_src=$raspi6,nw_dst=$sdncloud_ip,actions="resubmit(,3)"
#sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=1,dl_src=$raspi6,arp_tpa=$sdncloud_ip,actions="resubmit(,3)"


#sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=2,arp_tpa=$raspi6_ip,actions=mod_dl_dst:$raspi6,"output:1"
#sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=2,arp_tpa=$raspi5_ip,actions=mod_dl_dst:$raspi6,"output:1"
#sudo ovs-ofctl add-flow br0 arp,priority=90,in_port=2,arp_tpa=$raspi3_ip,actions=mod_dl_dst:$raspi3,"output:1"
#sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=2,nw_dst=$raspi6_ip,actions=mod_dl_dst:$raspi6,"output:1"
#sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=2,nw_dst=$raspi5_ip,actions=mod_dl_dst:$raspi6,"output:1"
#sudo ovs-ofctl add-flow br0 ip,priority=90,in_port=2,nw_dst=$raspi3_ip,actions=mod_dl_dst:$raspi3,"output:1"
#Table 4 is to rewrite the destination MAC address into SDN Cloud' MAC address
#sudo ovs-ofctl add-flow br0 table=2,actions=mod_dl_dst:$broadcast,"resubmit(,4)"
#sudo ovs-ofctl add-flow br0 table=3,actions=mod_dl_dst:$sdncloud,"resubmit(,5)"
#sudo ovs-ofctl add-flow br0 table=4,actions=output:1
#sudo ovs-ofctl add-flow br0 table=5,actions=output:2
sudo ovs-ofctl add-flow br0 priority=1,in_port=1,actions=drop

