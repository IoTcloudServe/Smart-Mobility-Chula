
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, ofproto_v1_3_parser
from ryu.lib import hub
import time
import os
#Datapath ID of each wireless node
raspi1=1152921504606846977
raspi2=1152921504606846978
raspi3=1152921504606846979
raspi4=1152921504606846980
raspi5=1152921504606846981
raspi6=1152921504606846982
gateway1=255421810004811
gateway2=1152921504606846985

#MAC addresses of each wireless nodes

r1="e8:4e:06:5e:6b:09"
r2="e8:4e:06:5f:47:59"
r3="e8:4e:06:40:d3:7f"
r4 ="e8:4e:06:40:d3:db"
r5="e8:4e:06:5e:6a:b1"
r6="e8:4e:06:40:94:20"
gw2="e8:4e:06:40:d1:c7"
gw1="e8:4e:06:40:d3:4b"
sdncloud="00:26:b9:ce:d3:e1"


#IP addresses of each wireless node
gw1ip="10.0.0.8"
r1ip="10.0.0.1"
r2ip="10.0.0.2"
r3ip="10.0.0.3"
r4ip="10.0.0.4"
r5ip="10.0.0.5"
r6ip="10.0.0.6"
gw2ip="10.0.0.9"
sdncloudip="192.168.1.6"


class node_failure (app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self,*args,**kwargs):
        super(node_failure,self).__init__(*args,**kwargs)
        self.switch_table = {}
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        #require to send configuration request message in every 8 seconds

#Define the funtion to add flow rules 
    def add_flow(self,datapath,table,priority,match,actions,hard):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        mod = parser.OFPFlowMod(datapath=datapath,table_id=table,command=ofproto.OFPFC_ADD,
                                priority=priority,match=match,instructions=inst,hard_timeout=hard)
        datapath.send_msg(mod)

#Define the function to add flow rule with the action of gototable
    def add_gototable(self,datapath,table,n,priority,match,hard): #n is a number of table
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        inst = [parser.OFPInstructionGotoTable(n)]
        mod = parser.OFPFlowMod(datapath=datapath,table_id=table,command=ofproto.OFPFC_ADD,
                                priority=priority,match=match,hard_timeout=hard,instructions=inst)
        datapath.send_msg(mod)

#Define the function to detect when wireless nodes connect to RYU controller or leave from RYU controller
    @set_ev_cls(ofp_event.EventOFPStateChange,[MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        current_time = time.asctime(time.localtime(time.time()))
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.logger.info("(Switch ID %s),IP address is connected %s in %s,1",datapath.id,datapath.address,current_time)
                self.datapaths[datapath.id] = datapath
                self.logger.info("Current Conneced Switches to RYU controller are %s",self.datapaths.keys())
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                self.logger.info("(Switch ID %s),IP address is leaved %s in %s,0", datapath.id, datapath.address,current_time)
                del self.datapaths[datapath.id]
                self.logger.info("Current Conneced Switches to RYU controller are %s", self.datapaths.keys())


###ForTestingPurpose

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        self.logger.info("Switch_ID %s (IP address %s) is connected,1",dp.id,dp.address)
####This One Is Working ####
        if dp.id == gateway1:
            match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_dst = gw1ip)
            actions= [parser.OFPActionSetField(eth_src=r1),parser.OFPActionOutput(4)]
            self.add_flow(datapath,9,35,match,actions,100)
                
                
#Define the function to send configuraion request message in every second
    def _monitor(self):
        while True:
            #To send configuration request message only when one of the wireless mesh nodes leave from RYU controller
            if (raspi1 not in self.datapaths or raspi2 not in self.datapaths or raspi3 not in self.datapaths or
                raspi4 not in self.datapaths or raspi5 not in self.datapaths or raspi6 not in self.datapaths):
                for datapath in self.datapaths.values():
                    self.send_get_config_request(datapath)
            hub.sleep(8)

#Define the function for configuration request message
    def send_get_config_request(self, datapath):
        ofp_parser = datapath.ofproto_parser
        req = ofp_parser.OFPGetConfigRequest(datapath)
        datapath.send_msg(req)

#Define the function to add flow rules with configuration request message
    @set_ev_cls(ofp_event.EventOFPGetConfigReply, MAIN_DISPATCHER)
    def get_config_reply_handler(self,ev):
        current_time = time.asctime(time.localtime(time.time()))
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        self.logger.info('IP address %s sends OFPConfigReply message in %s', datapath.address, current_time)
        if ((raspi1 not in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths and raspi4 in self.datapaths
             and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
            or (raspi1 not in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths and raspi4 in self.datapaths
                and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)
            or (raspi1 not in self.datapaths and raspi2 not in self.datapaths and raspi3 in self.datapaths and raspi4 in self.datapaths
                and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
            or (raspi1 not in self.datapaths and raspi2 not in self.datapaths and raspi3 in self.datapaths and raspi4 in self.datapaths
                and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)
            or (raspi1 not in self.datapaths and raspi2 not in self.datapaths and raspi3 not in self.datapaths and raspi4 in self.datapaths
                and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
            or (raspi1 not in self.datapaths and raspi2 not in self.datapaths and raspi3 not in self.datapaths and raspi4 in self.datapaths
                and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)):
####Now Work
            self.logger.info("case1_Raspi1_Is_Disconnected_With_RYU_Controller")

            local = datapath.ofproto.OFPP_LOCAL
            if datapath.id == raspi5:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2, arp_tpa = gw1ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay to Raspi 4

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_dst = gw1ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay to Raspi 4
                #These two rules make the route Raspi 2 to Raspi 4 from Raspi 5 Raspi 2 - Raspi 5 - Raspi 4 - GW1
###NewRules###
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2, arp_spa=r2ip, arp_tpa = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)
#Table 4 is to relay to Raspi 4

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_src=r2ip, ipv4_dst = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)
                #These two rules make the route Raspi 2 to Raspi 4 from Raspi 5 Raspi 2 - Raspi 5 - Raspi 4 - GW1 - SDNCLOUD
###NewRules###                
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r4, arp_tpa = r2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 4 is to relay to Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r4, ipv4_dst = r2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 4 is to relay to Raspi 2
                #These two rules make the route GW1 to Raspi 2 through the route GW1 - Raspi 4 - Raspi 5 - Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r4,arp_spa=sdncloudip, arp_tpa=r2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 3 is to relay to Gateway 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r4,ipv4_src=sdncloudip, ipv4_dst=r2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 3 is to relay to Gateway 1

            if datapath.id == raspi4:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5,arp_spa=r2ip, arp_tpa=sdncloudip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay to Gateway 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5,ipv4_src=r2ip, ipv4_dst=sdncloudip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay to Gateway 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=gw1,arp_spa=sdncloudip, arp_tpa=r2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay to Gateway 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=gw1,ipv4_src=sdncloudip, ipv4_dst=r2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay to Gateway 1


            if datapath.id == raspi2:
                match = parser.OFPMatch(in_port=local, eth_type=0x0806, eth_src=r2,arp_spa=r2ip, arp_tpa=sdncloudip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 3 is to relay to Gateway 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800, eth_src=r2,ipv4_src=r2ip, ipv4_dst=sdncloudip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 3 is to relay to Gateway 1

#                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=gw1,arp_spa=sdncloudip, arp_tpa=r2ip)
 #               self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay to Gateway 1

  #              match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=gw1,ipv4_src=sdncloudip, ipv4_dst=r2ip)
   #             self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay to Gateway 1





            if datapath.id == gateway1: #Gateway1
                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r2ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10) #Table 3 is to relay Raspi 4

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r2ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10) #Table 3 is to relay Raspi 4

                match = parser.OFPMatch(in_port=local, eth_type=0x0806, arp_tpa=r2ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)  # Table 3 is to relay Raspi 4

                match = parser.OFPMatch(in_port=local, eth_type=0x0800, ipv4_dst=r2ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)  # Table 3 is to relay Raspi 4
###NewRules####
                match = parser.OFPMatch(in_port=2, eth_type=0x0800,eth_src=sdncloud,ipv4_src=sdncloudip,ipv4_dst=r2ip)
                actions= [parser.OFPActionSetField(eth_dst=r4),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)
                
                match = parser.OFPMatch(in_port=2, eth_type=0x0806,eth_src=sdncloud,arp_spa=sdncloudip,arp_tpa=r2ip)
                actions= [parser.OFPActionSetField(eth_dst=r4),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)


                match = parser.OFPMatch(in_port=1, eth_type=0x0800,eth_src=r4,ipv4_src=r2ip,ipv4_dst=sdncloudip)
                actions= [parser.OFPActionSetField(eth_dst=sdncloud),parser.OFPActionOutput(2)]
                self.add_flow(datapath,0,160,match,actions,10)

                match = parser.OFPMatch(in_port=1, eth_type=0x0806,eth_src=r4,arp_spa=r2ip,arp_tpa=sdncloudip)
                actions= [parser.OFPActionSetField(eth_dst=sdncloud),parser.OFPActionOutput(2)]
                self.add_flow(datapath,0,160,match,actions,10)


                match = parser.OFPMatch(in_port=1, eth_type=0x0800,eth_src=r1,ipv4_src=r2ip,ipv4_dst=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)
                
                match = parser.OFPMatch(in_port=1, eth_type=0x0806,eth_src=r1,arp_spa=r2ip,arp_tpa=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)
####NewRules###

        elif ((raspi2 not in self.datapaths and raspi3 in self.datapaths and raspi1 in self.datapaths and raspi4 in self.datapaths
               and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
              or (raspi2 not in self.datapaths and raspi3 in self.datapaths and raspi1 in self.datapaths and raspi4 in self.datapaths
                  and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)
              or (raspi2 not in self.datapaths and raspi3 not in self.datapaths and raspi1 in self.datapaths and raspi4 in self.datapaths
                  and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
              or (raspi2 not in self.datapaths and raspi3 not in self.datapaths and raspi1 in self.datapaths and raspi4 in self.datapaths
                  and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)):
####NowWork
            self.logger.info("Case 2_Raspi2_Is_Disconnected_From_RYU_Controller")
            self.logger.info("No_Rerouting_Is_Required")

            local = datapath.ofproto.OFPP_LOCAL
            if datapath.id == raspi6:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r3, arp_tpa=gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay to Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r3, ipv4_dst=gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay to Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa=r3ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)# Table 2 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst=r3ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)# Table 2 is to relay Raspi 3


            if ev.msg.datapath.id == gateway1: #Gateway1
                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r3ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10) #Table 3 is to relay Raspi 4

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r3ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10) #Table 3 is to relay Raspi 4

        elif ((raspi3 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths and raspi4 in self.datapaths
              and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
              or (raspi3 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths and raspi4 in self.datapaths
            and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)):

            self.logger.info("Case 3_Raspi3_is_Disconnected_With_RYU_Controller")
            self.logger.info("No_Rerouting_Process_Is_Required")
###IsNowWork###            

        elif ((raspi4 not in self.datapaths and raspi5 in self.datapaths and raspi6 in self.datapaths and raspi1 in self.datapaths
               and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 in self.datapaths)
              or (raspi4 not in self.datapaths and raspi5 in self.datapaths and raspi6 in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 not in self.datapaths)
              or (raspi4 not in self.datapaths and raspi5 not in self.datapaths and raspi6 in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 in self.datapaths)
              or (raspi4 not in self.datapaths and raspi5 not in self.datapaths and raspi6 in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 not in self.datapaths)
              or (raspi4 not in self.datapaths and raspi5 not in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 in self.datapaths)
              or (raspi4 not in self.datapaths and raspi5 not in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 not in self.datapaths)):
            self.logger.info("Case 4_Raspi4_is_Disconnected_With_RYU_Controller")
            self.logger.info("No_Rerouting_Process_Is_Required")
            
            local = datapath.ofproto.OFPP_LOCAL
            if datapath.id == raspi2:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r1, arp_tpa = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r1, ipv4_dst = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, arp_spa=gw2ip, arp_tpa=r5ip)
                self.add_flow(datapath, 0, 160, match, [], 10)

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, ipv4_src=gw2ip, ipv4_dst=r5ip)
                self.add_flow(datapath, 0, 160, match, [], 10)

            if datapath.id == raspi3:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r6, arp_tpa = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r6, ipv4_dst = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2, arp_tpa = r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 6

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_dst = r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 6

            if datapath.id == gateway1:
                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

        elif ((raspi4 not in self.datapaths and raspi5 in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths
              and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 in self.datapaths)
              or (raspi4 not in self.datapaths and raspi5 in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi3 in self.datapaths and gateway2 not in self.datapaths)):

            self.logger.info("Case 4_Raspi4_and_Raspi6_Are_Disconnected_From_RYU_Controller")
####IsNowWork#####
            local = datapath.ofproto.OFPP_LOCAL
            if datapath.id == raspi2:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 1

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r1, arp_tpa = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r1, ipv4_dst = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3
#################
#NewRules
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3
#NewRules
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r3, arp_tpa = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r3, ipv4_dst = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

            if datapath.id == raspi3:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r6, arp_tpa = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r6, ipv4_dst = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2, arp_tpa = r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 6

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_dst = r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 6

            if datapath.id == gateway1:
                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to rleay Raspi 1
###NewRules
            if datapath.id == gateway2:

                match = parser.OFPMatch(in_port=2, eth_type=0x0800,ipv4_dst=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)
                
                match = parser.OFPMatch(in_port=2, eth_type=0x0806,arp_tpa=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r6,ipv4_src=r5ip,ipv4_dst=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r6,arp_spa=r5ip,arp_tpa=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)
###NewRules
        elif ((raspi5 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths
               and raspi4 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
              or (raspi5 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths
                  and raspi4 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)
              or (raspi5 not in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths
                  and raspi3 in self.datapaths and raspi4 in self.datapaths and gateway2 in self.datapaths)
              or (raspi5 not in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths
                  and raspi3 in self.datapaths and raspi4 in self.datapaths and gateway2 not in self.datapaths)):
########NowWork#####
            self.logger.info("Case 5_Raspi5_Is_Disconnected_With_RYU_Controller")

            local = datapath.ofproto.OFPP_LOCAL
            if datapath.id == raspi3:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r6, arp_tpa = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r6, ipv4_dst = gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2, arp_tpa = r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 6

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_dst = r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 6

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2,arp_spa=r5ip, arp_tpa = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2,ipv4_src=r5ip, ipv4_dst = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay Raspi 2

            if datapath.id == raspi2:
#####NewRules####
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r3, arp_tpa = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r3, ipv4_dst = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5
                
#################
            if datapath.id == gateway1:

                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1
###NewRules
            if datapath.id == gateway2:

                match = parser.OFPMatch(in_port=2, eth_type=0x0800,ipv4_dst=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)
                
                match = parser.OFPMatch(in_port=2, eth_type=0x0806,arp_tpa=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r6,ipv4_src=r5ip,ipv4_dst=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r6,arp_spa=r5ip,arp_tpa=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)

#################

        elif ((raspi6 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths
               and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 not in self.datapaths)
              or (raspi6 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths
                  and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 in self.datapaths)) :

            self.logger.info("Raspi6_Is_Disconnected_With_RYU_Controller")

            if datapath.id == raspi3:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2,arp_spa=r5ip, arp_tpa = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2,ipv4_src=r5ip, ipv4_dst = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 3 is to relay Raspi 2

            if datapath.id == raspi2:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

###NewRules
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst = sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3
#################
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r3, arp_tpa = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r3, ipv4_dst = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5
###NewRules
            if datapath.id == gateway2:

                match = parser.OFPMatch(in_port=2, eth_type=0x0800,ipv4_dst=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)
                
                match = parser.OFPMatch(in_port=2, eth_type=0x0806,arp_tpa=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r6,ipv4_src=r5ip,ipv4_dst=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r6,arp_spa=r5ip,arp_tpa=sdncloudip)
                self.add_flow(datapath,0,160,match,[],10)
#################

        elif ((raspi1 not in self.datapaths and raspi6 not in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths
               and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 in self.datapaths)
              or (raspi1 not in self.datapaths and raspi6 not in self.datapaths and raspi2 in self.datapaths and raspi3 in self.datapaths
                  and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 not in self.datapaths) or (raspi1 not in self.datapaths and raspi2 not in self.datapaths and raspi3 not in self.datapaths and raspi6 not in self.datapaths and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 in self.datapaths) or (raspi1 not in self.datapaths and raspi2 not in self.datapaths and raspi3 not in self.datapaths and raspi6 not in self.datapaths and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 not in self.datapaths) or (raspi1 not in self.datapaths and raspi3 not in self.datapaths and raspi6 not in self.datapaths and raspi2 in self.datapaths and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 in self.datapaths) or (raspi1 not in self.datapaths and raspi3 not in self.datapaths and raspi6 not in self.datapaths and raspi2 in self.datapaths and raspi4 in self.datapaths and raspi5 in self.datapaths and gateway2 not in self.datapaths)):

            local = datapath.ofproto.OFPP_LOCAL

            self.logger.info("Case 6_Raspi1_And_Raspi6_Are_Disconnected_With_RYU Controller")
            self.logger.info("Cannot_Reroute_In_This_Version")
            
            if ev.msg.datapath.id == raspi2:  # Raspi2 To assign the flow rules at Raspi2 to reroute the control packet from raspi3 and gateway2 to gateway1
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r3, arp_tpa=gw1ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r3, ipv4_dst=gw1ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa=r3ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst=r3ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa=gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst=gw2ip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

###New_Rules###
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r5, arp_tpa=sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r5, ipv4_dst=sdncloudip)
                self.add_gototable(datapath, 0, 4, 160, match, 10)#Table 4 is to relay Raspi 3
###New_Rules###
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r3, arp_tpa = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r3, ipv4_dst = r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 5


            elif ev.msg.datapath.id == raspi5:
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2, arp_tpa=gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 4

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_dst=gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 4

###NewRules###
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r2, arp_tpa=sdncloudip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 4

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r2, ipv4_dst=sdncloudip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 4
###NewRules###
                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r4, arp_tpa=r2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r4, ipv4_dst=r2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r4, arp_tpa=r3ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 2 

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r4, ipv4_dst=r3ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0806, eth_src=r4, arp_tpa=gw2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 2

                match = parser.OFPMatch(in_port=1, eth_type=0x0800, eth_src=r4, ipv4_dst=gw2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 2

            elif ev.msg.datapath.id == gateway1:  # Gateway1
                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r1ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800,ipv4_dst=r1ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10) #Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local,eth_type=0x0806)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 4

                match = parser.OFPMatch(in_port=local, eth_type=0x0800)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi
###NewRules####
                match = parser.OFPMatch(in_port=3, eth_type=0x0800,ipv4_dst =r2ip)
                actions= [parser.OFPActionSetField(eth_dst=r4),parser.OFPActionOutput(2)]
                self.add_flow(datapath,0,160,match,actions,10)
                

                match = parser.OFPMatch(in_port=3, eth_type=0x0806,arp_tpa =r2ip)
                actions= [parser.OFPActionSetField(eth_dst=r4),parser.OFPActionOutput(2)]
                self.add_flow(datapath,0,160,match,actions,10)
####NewRules###

###NewRules####
            if datapath.id == gateway2:

                match = parser.OFPMatch(in_port=2, eth_type=0x0800,ipv4_dst=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)
                
                match = parser.OFPMatch(in_port=2, eth_type=0x0806,arp_tpa=r5ip)
                actions= [parser.OFPActionSetField(eth_dst=r3),parser.OFPActionOutput(1)]
                self.add_flow(datapath,0,160,match,actions,10)            
#################


####No New Rules####
        elif ((raspi3 not in self.datapaths and raspi4 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths
               and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 in self.datapaths)
              or (raspi3 not in self.datapaths and raspi4 not in self.datapaths and raspi1 in self.datapaths and raspi2 in self.datapaths
                  and raspi5 in self.datapaths and raspi6 in self.datapaths and gateway2 not in self.datapaths)
              or (raspi3 not in self.datapaths and raspi4 not in self.datapaths and raspi5 not in self.datapaths and raspi6 not in self.datapaths
                  and raspi1 in self.datapaths and raspi2 in self.datapaths and gateway2 in self.datapaths)
              or (raspi3 not in self.datapaths and raspi4 not in self.datapaths and raspi5 not in self.datapaths and raspi6 not in self.datapaths
                  and raspi1 in self.datapaths and raspi2 in self.datapaths and gateway2 not in self.datapaths)
              or (raspi3 not in self.datapaths and raspi4 not in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi5 in self.datapaths and gateway2 in self.datapaths)
              or (raspi3 not in self.datapaths and raspi4 not in self.datapaths and raspi6 not in self.datapaths and raspi1 in self.datapaths
                  and raspi2 in self.datapaths and raspi5 in self.datapaths and gateway2 not in self.datapaths)):

            self.logger.info("Case 7_Raspi3_And_Raspi4_Are_Disconnected_With_RYU_Controller")

            local = datapath.ofproto.OFPP_LOCAL
            if ev.msg.datapath.id ==raspi5: #Raspi5 Assign the flow rules at Raspi5 to relay the packet from raspi6 to gateway1
                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r6,arp_tpa=gw1ip) #Table 2 is to relay Raspi 2
                self.add_gototable(datapath,0,2,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r6,ipv4_dst=gw1ip) #Table 2 is to relay Raspi 2
                self.add_gototable(datapath,0,2,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r2,arp_tpa=r6ip) #Table 4 is to relay Raspi 6
                self.add_gototable(datapath,0,4,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r2,ipv4_dst=r6ip) #Table 4 is to relay Raspi 6
                self.add_gototable(datapath,0,4,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r2,arp_tpa=gw2ip) #Table 4 is to relay Raspi 6
                self.add_gototable(datapath,0,4,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r2,ipv4_dst=gw2ip)#Table 4 is to relay Raspi 6
                self.add_gototable(datapath,0,4,160,match,10)

            elif ev.msg.datapath.id == raspi2:
                #Raspi2 To assign the flowrules at raspi2 to relay the control packet from raspi5,raspi6 to gateway1
                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r5,arp_tpa=gw1ip) #Table 3 is to relay Raspi 1
                self.add_gototable(datapath,0,3,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r5,ipv4_dst=gw1ip)#Table 3 is to relay Raspi 1
                self.add_gototable(datapath,0,3,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r1,arp_tpa=r5ip) #Table 2 is to relay Raspi 5
                self.add_gototable(datapath,0,2,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r1,ipv4_dst=r5ip) #Table 2 is to relay Raspi 5
                self.add_gototable(datapath,0,2,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r1,arp_tpa=r6ip) #Table 2 is to relay Raspi 5
                self.add_gototable(datapath,0,2,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r1,ipv4_dst=r6ip)#Table 2 is to relay Raspi 5
                self.add_gototable(datapath,0,2,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r1,arp_tpa=gw2ip)#Table 2 is to relay Raspi 5
                self.add_gototable(datapath,0,2,160,match,10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r1,ipv4_dst=gw2ip)#Table 2 is to relay Raspi 5
                self.add_gototable(datapath,0,2,160,match,10)

            elif ev.msg.datapath.id == raspi6: #Raspi 6
                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=gw2,arp_tpa=gw1ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=gw2,ipv4_dst=gw1ip)

                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 5

                match = parser.OFPMatch(in_port=1,eth_type=0x0806,eth_src=r5,arp_tpa=gw2ip)#Table 3 is to relay Raspi 5
                self.add_gototable(datapath, 0, 3, 160, match, 10)

                match = parser.OFPMatch(in_port=1,eth_type=0x0800,eth_src=r5,ipv4_dst=gw2ip)
                self.add_gototable(datapath, 0, 3, 160, match, 10)#Table 3 is to relay Raspi 5

            elif ev.msg.datapath.id == gateway1: #Gateway1
                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local,eth_type=0x0806,arp_tpa=gw2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800, ipv4_dst=r5ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800, ipv4_dst=r6ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1

                match = parser.OFPMatch(in_port=local, eth_type=0x0800, ipv4_dst=gw2ip)
                self.add_gototable(datapath, 0, 2, 160, match, 10)#Table 2 is to relay Raspi 1
             
            


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):

        msg = ev.msg

        dp = msg.datapath

        ofp = dp.ofproto

        if msg.reason == ofp.OFPR_NO_MATCH:

            reason = 'NO MATCH'

        elif msg.reason == ofp.OFPR_ACTION:

            reason = 'ACTION'

        elif msg.reason == ofp.OFPR_INVALID_TTL:

            reason = 'INVALID TTL'

        else:

            reason = 'unknown'


        self.logger.debug('OFPPacketIn received: '

                      'buffer_id=%x total_len=%d reason=%s '

                      'table_id=%d cookie=%d match=%s data=%s',

                      msg.buffer_id, msg.total_len, reason,

                      msg.table_id, msg.cookie, msg.match,

                      utils.hex_array(msg.data))

 
