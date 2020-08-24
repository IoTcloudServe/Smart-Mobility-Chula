sudo ovs-ofctl add-flow br1 arp,priority=100,in_port=2,dl_src=24:fd:52:27:9a:cf,arp_tpa=192.168.0.5,actions=LOCAL
sudo ovs-ofctl add-flow br1 ip,priority=100,in_port=2,dl_src=24:fd:52:27:9a:cf,nw_dst=192.168.0.5,actions=LOCAL
sudo ovs-ofctl add-flow br1 arp,priority=100,in_port=LOCAL,actions=output:2
sudo ovs-ofctl add-flow br1 ip,priority=100,in_port=LOCAL,actions=output:2
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=e8:4e:06:40:d2:cd,arp_tpa=10.0.0.5,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=e8:4e:06:40:d2:cd,nw_dst=10.0.0.5,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=1,dl_src=e8:4e:06:5e:67:11,arp_tpa=10.0.0.5,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=1,dl_src=e8:4e:06:5e:67:11,nw_dst=10.0.0.5,actions=LOCAL
sudo ovs-ofctl add-flow br0 arp,priority=100,in_port=LOCAL,actions=output:1
sudo ovs-ofctl add-flow br0 ip,priority=100,in_port=LOCAL,actions=output:1
sudo ovs-ofctl add-flow br0 arp,priority=80,in_port=LOCAL,dl_src=e8:4e:06:5e:67:4d,arp_tpa=192.168.0.6,actions=output:4
sudo ovs-ofctl add-flow br0 ip,priority=80,in_port=LOCAL,dl_src=e8:4e:06:5e:67:4d,nw_dst=192.168.0.6,actions=output:4
sudo ovs-ofctl add-flow br1 arp,priority=80,in_port=3,dl_src=24:fd:52:27:9c:0c,arp_tpa=192.168.0.6,actions="resubmit(,2)"
sudo ovs-ofctl add-flow br1 ip,priority=80,in_port=3,dl_src=24:fd:52:27:9c:0c,nw_dst=192.168.0.6,actions="resubmit(,2)"
sudo ovs-ofctl add-flow br1 table=2,actions=mod_dl_dst:24:fd:52:27:9a:cf,"load:0->OXM_OF_IN_PORT[],resubmit(,3)"
sudo ovs-ofctl add-flow br1 table=3,actions=output:2
sudo ovs-ofctl add-flow br1 arp,priority=80,in_port=2,dl_src=24:fd:52:27:9a:cf,arp_tpa=10.0.0.5,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br1 ip,priority=80,in_port=2,dl_src=24:fd:52:27:9a:cf,nw_dst=10.0.0.5,actions="resubmit(,4)"
sudo ovs-ofctl add-flow br1 table=4,actions=mod_dl_dst:e8:4e:06:5e:67:4d,"load:0->OXM_OF_IN_PORT[],resubmit(,5)"
sudo ovs-ofctl add-flow br1 table=5,actions=output:3
sudo ovs-ofctl add-flow br0 arp,priority=80,in_port=4,actions=LOCAL
sudo ovs-ofctl add-flow br0 ip,priority=80,in_port=4,actions=LOCAL