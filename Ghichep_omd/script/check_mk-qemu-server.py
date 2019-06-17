#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +-----------------------------------------------------------------+
# |                                                                 |
# |        (  ___ \     | \    /\|\     /||\     /|( (    /|        |
# |        | (   ) )    |  \  / /| )   ( || )   ( ||  \  ( |        |
# |        | (__/ /     |  (_/ / | |   | || (___) ||   \ | |        |
# |        |  __ (      |   _ (  | |   | ||  ___  || (\ \) |        |
# |        | (  \ \     |  ( \ \ | |   | || (   ) || | \   |        |
# |        | )___) )_   |  /  \ \| (___) || )   ( || )  \  |        |
# |        |/ \___/(_)  |_/    \/(_______)|/     \||/    )_)        |
# |                                                                 |
# | Copyright Bastian Kuhn 2018                mail@bastian-kuhn.de |
# +-----------------------------------------------------------------+
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Example output from agent:
# <<<qemu>>>
# 4 i-4B9008BE running 2048 4.0 2.7
# 5 i-44F608B6 running 2048 0.0 0.7


#
# Edited by Trangnth
# Date 06/2019
# File is placed on server. Path to file: `/omd/sites/monitoring/local/share/check_mk/checks/qemu`
#

#
# Output agent
#

"""
<<<qemu>>>
2 hungnt-ctl2 running 8192 40 11.8 vnet2:rx-75446:tx-0(kb/s) vnet3:rx-52883343:tx-58044108(kb/s)
3 hungnt-ctl3 running 8192 30 9.0 vnet4:rx-75446:tx-0(kb/s) vnet5:rx-37723528:tx-35451318(kb/s)
4 hungnt-com1 running 4096 65.6 6.0 vnet6:rx-197735:tx-25257(kb/s) vnet7:rx-97841321:tx-163960354(kb/s)
5 hungnt-com2 running 4096 20 5.8 vnet8:rx-205315:tx-14746(kb/s) vnet9:rx-31932441:tx-51946406(kb/s)
13 hungnt-ceph1 running 4096 0 5.9 vnet19:rx-130546679:tx-155102214(kb/s) vnet20:rx-96268868:tx-53922557(kb/s)
"""

#
# Output server 
#

"""
OMD[monitoring]:~$ check_mk --debug -nv --checks=qemu kvm36
Check_MK version 1.5.0p16
+ FETCHING DATA
 [agent] Execute data source
 [piggyback] Execute data source
VM hungnt-ceph1      OK - Status: running, id: 13, CPU: 0%, Memory: (assined: 4096 MB, used: 6%), vnet19:rx-130526078:tx-155059787(kb/s), vnet20:rx-96244490:tx-53868619(kb/s)
VM hungnt-ceph2      OK - Status: running, id: 14, CPU: 3%, Memory: (assined: 4096 MB, used: 6%), vnet21:rx-130589086:tx-154942005(kb/s), vnet22:rx-95663446:tx-21560872(kb/s)
VM hungnt-ceph3      OK - Status: running, id: 15, CPU: 3%, Memory: (assined: 4096 MB, used: 6%), vnet23:rx-155036924:tx-105887318(kb/s), vnet24:rx-76689761:tx-23123045(kb/s)
VM hungnt-com1       WARN - Status: running, id: 4, CPU: 63%, Memory: (assined: 4096 MB, used: 6%), vnet6:rx-197727:tx-25256(kb/s), vnet7:rx-97723666:tx-163919715(kb/s)
VM hungnt-com2       OK - Status: running, id: 5, CPU: 50%, Memory: (assined: 4096 MB, used: 6%), vnet8:rx-205307:tx-14744(kb/s), vnet9:rx-31925300:tx-51942964(kb/s)
"""


def qemu_fix_vmname(name):
    # Reason for this not clear yet
    if name.startswith("instance"):
        name.replace("instance", "i")
    return name


def inventory_qemu(info):
    for line in info:
        if line[2] == "running":
            vm = qemu_fix_vmname(line[1])
            yield vm, {}

def check_qemu(item, params, info):
    perfdata = []
#    print "%s" % (info)
    for line in info:
        #print "%s" % (line)
        vm = qemu_fix_vmname(line[1])
        if vm == item:
            status = line[2]
            assigned_mem = line[3]
            infotext = ["Status: %s, id: %s" % (status, line[0])]
            state = 2
            if status == "running":
                state = 0
                current_cpu = int(round(float(line[4])))
                infotext.append("CPU: %s%%" % (current_cpu))

                current_mem = int(round(float(line[5])))
                infotext.append("Memory: (assined: %s MB, used: %s%%)" % (assigned_mem, current_mem))

                # Network
                x=0
                for net_line in line:
                    if x > 5:
                        current_net = str(line[x])
                        infotext.append("%s" % (current_net))
                    x+=1

                perfdata.append(("cpu_util", current_cpu))
                perfdata.append(("memory_usage", current_mem))

                if params:
                    cpu_state = 0
                    mem_state = 0
                    if params.get('cpu'):
                        cpu_warn, cpu_crit = params['cpu']
                        if current_cpu >= cpu_crit:
                            cpu_state = 2
                        elif current_cpu >= cpu_warn:
                            cpu_state = 1

                    if params.get('mem'):
                        mem_warn, mem_crit = params['mem']
                        if current_mem >= mem_crit:
                            mem_state = 2
                        elif current_cpu >= mem_warn:
                            mem_state = 1
                    state = max(mem_state, cpu_state)

            return  state, ", ".join(infotext), perfdata

check_info["qemu"] = {
    "check_function" : check_qemu,
    "inventory_function" : inventory_qemu,
    "service_description" : "VM %s",
    "has_perfdata" : True,
    "group" : "qemu",
}
