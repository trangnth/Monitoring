# updated formating:
# Bastian Kuhn 08/2018

# updated by
# MinhKMA 06/2019

#
# Updated by Trangnth
# Date 06/2019
#

#
# File is placed on agent. Use command `check_mk_agent | head` to check
#

yum install -y vnstat

if which virsh >/dev/null; then
    echo '<<<qemu>>>'
    virsh list | grep -v 'State' | grep -v '^--' | grep -v '^$' | while read L
    do
            ID=$(echo $L | awk '{print $1}')
            NAME=$(echo $L | awk '{print $2}')
            STATE=$(echo $L | awk '{print $3}')
            NUM_VCPU=$(virsh dominfo $NAME | grep 'CPU(s)' | awk '{print $2}')
            MEM=$(virsh dominfo $NAME | grep 'Used memory' | awk '{print $3}')
            let MEM=MEM/1024
            PID=$(ps aux | grep kvm | grep $NAME | awk '{print $2}')
            if [ $PID -gt 0 ]; then
                    DATA=$(top -p $PID -n 1 -b | tail -1  | awk -- '{print $9" "$10}')
                    CPU=$(top -p $PID -n 1 -b | tail -1  | awk -- '{print $9}')
                    AVG_CPU=$(awk -v CPU=$CPU -v NUM_VCPU=$NUM_VCPU 'BEGIN { print  ( CPU / NUM_VCPU ) }')
                    RAM=$(top -p $PID -n 1 -b | tail -1  | awk -- '{print $10}')

                    # kB/s
                    VNET=$(virsh dumpxml $NAME | grep "target dev='vnet" | cut -d "'" -f 2)
                    NET=""
                    for x in $VNET; do
                        RX=`expr $(virsh domifstat $NAME $x | grep 'rx_bytes' | awk '{print $3}') / 1000`   # rx_bytes
                        TX=`expr $(virsh domifstat $NAME $x | grep 'tx_bytes' | awk '{print $3}') / 1000`  # tx_bytes
                        # sleep 5
                        # RX2=`expr $(virsh domifstat $NAME $x | grep 'rx_bytes' | awk '{print $3}') / 1000`   # rx_bytes
                        # TX2=`expr $(virsh domifstat $NAME $x | grep 'tx_bytes' | awk '{print $3}') / 1000`  # tx_bytes

                        # RX=`expr $(($RX1 - $RX2)) / 60`
                        # TX=`expr $(($TX1 - $TX2)) / 60`

                        # export RX2=$RX1
                        # export TX2=$TX1

                        NET=$NET" $x:rx-$RX:tx-$TX(kb)"
                    done
                    

                    # bytes/s
                    VDISK=$(virsh domblklist trang-com1 | egrep -v "hda|Target|--|^$" | awk '{print $1}')
                    DISK=""
                    for x in $VDISK;do
                        RD=`expr $(virsh domblkstat $NAME $x | grep "rd_bytes" | awk '{print $3}') \* 1000000000 / $(virsh domblkstat $NAME $x | grep "rd_total_times" | awk '{print $3}')`
                        WR=`expr $(virsh domblkstat $NAME $x | grep "wr_bytes" | awk '{print $3}') \* 1000000000 / $(virsh domblkstat $NAME $x | grep "wr_total_times" | awk '{print $3}')`
                        DISK=$DISK" $x:rd-$RD:wr-$WR(bytes/s)"
                    done

                    echo $ID" "$NAME" "$STATE" "$MEM" "$AVG_CPU" "$RAM$NET$DISK
            else
                    DATA=""
                    AVG_CPU=""
                    RAM=""
                    NET=""
                    DISK=""
                    echo $ID" "$NAME" "$STATE" "$MEM" "$AVG_CPU" "$RAM$NET$DISK
            fi

    done
fi
