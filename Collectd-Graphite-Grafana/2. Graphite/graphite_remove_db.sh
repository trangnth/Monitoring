#!/bin/bash

# -- MedieTechJSC --
# Description: Delete VMs deleted in whisper database
# Requirement: Openstack version Mitaka
# Authur: trangnth
# Date: 14/08/2019


IP_CONTROLLER='192.168.40.81'
SSL='http'
USERNAME='admin'
PASSWORD='trang1234'

LIST_COM=(compute1 compute2)
WHISPER_PATH='/var/lib/carbon/whisper/collectd/'

logger -t delete-vm -i Start check VMs deleted for Graphite

# ssh -o 'StrictHostKeyChecking no' -i /root/.ssh/$IP_CONTROLLER.key root@$IP_CONTROLLER openstack server list  --all-project  --os-username $USERNAME --os-password $PASSWORD --os-auth-url http://$IP_CONTROLLER:5000/v2.0 --os-tenant-name admin --os-region-name RegionOne -c ID -f value

# List uuid VMs alive
i=0
while IFS= read -r line
do
        LIST_VM_ALIVE[$i]=$line
        i=+1
done < <(ssh -o 'StrictHostKeyChecking no' -i /root/.ssh/$IP_CONTROLLER.key root@$IP_CONTROLLER openstack server list  --all-project  --os-username $USERNAME --os-password $PASSWORD --os-auth-url http://$IP_CONTROLLER:5000/v2.0 --os-tenant-name admin --os-region-name RegionOne -c ID -f value)

#echo ${LIST_VM_ALIVE[@]}


for COM in ${LIST_COM[*]}
do
        #echo $COM
        PATH_COM=$WHISPER_PATH$COM
        #echo $PATH_COM

        # List All VM on Graphite server
        LIST_VM=()
        i=0
        while IFS= read -r line
        do
                LIST_VM[$i]=$line
                i=`expr $i + 1`

        done < <(ls -l $PATH_COM | grep "^d" | cut -d " " -f 9)
#        echo ${LIST_VM[@]}

        DIFF=()
        for i in "${LIST_VM[@]}"; do
                skip=
                for j in "${LIST_VM_ALIVE[@]}"; do
                    [[ $i == $j ]] && { skip=1; break; }
                done
                [[ -n $skip ]] || DIFF+=("$i")
        done
#        declare -p DIFF
        #echo ${DIFF[*]}

        # Deleting metric of deleted VMs
        for i in "${DIFF[@]}"; do
                rm -rf $PATH_COM/$i
                echo Deleted $i
                logger -t delete-vm -i Deleted $i
        done
done

logger -t delete-vm -i Successfully checked!