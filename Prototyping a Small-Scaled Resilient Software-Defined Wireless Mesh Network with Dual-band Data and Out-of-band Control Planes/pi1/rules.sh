sudo ovs-ofctl add-flow br1 arp,priority=100,in_port=2,dl_src=24:fd:52:27:9a:47,arp_tpa=192.168.0.1,actions=LOCAL
sudo ovs-ofctl add-flow br1 ip,priority=100,in_port=2,dl_src=24:fd:52:27:9a:47,nw_dst=192.168.0.1,actions=LOCAL
sudo ovs-ofctl add-flow br1 arp,priority=100,in_port=2,dl_src=24:fd:52:27:9a:f8,arp_tpa=192.168.0.1,actions=LOCAL
sudo ovs-ofctl add-flow br1 ip,priority=100,in_port=2,dl_src=24:fd:52:27:9a:f8,nw_dst=192.168.0.1,actions=LOCAL
sudo ovs-ofctl add-flow br1 arp,priority=100,in_port=LOCAL,actions=output:2
sudo ovs-ofctl add-flow br1 ip,priority=100,in_port=LOCAL,actions=output:2

