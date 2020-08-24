sudo ovs-vsctl --if-exist del-br br1
sudo ovs-vsctl add-br br1
sudo ovs-vsctl set bridge br1 other-config:datapath-id=2000000000000001
sudo ovs-vsctl add-port br1 wlx485d602a5392 -- set interface wlx485d602a5392 ofport_request=2
#sudo ovs-vsctl set-controller br1 tcp:203.237.53.88
sudo ovs-vsctl set-controller br1 mode=out-of-band
sudo ovs-vsctl set-fail-mode br1 secure
sudo ovs-vsctl set bridge br1 protocol=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
sudo ovs-vsctl set bridge br1 stp_enable=true
sudo ovs-vsctl set-controller br1 tcp:203.237.53.88
