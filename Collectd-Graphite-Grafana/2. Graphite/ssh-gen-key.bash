#!/bin/bash

# -- MedieTechJSC --
# Description: Generating a new ssh key pair and adding public key on server 
# Authur: trangnth
# Date: 14/08/2019


echo "Checking OS..."

check_distro()
{
    if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
        . /etc/os-release
        os=$ID
        release=$VERSION_ID

        if [ $os != 'centos' ] && [ $release != '7' ]
        then
                echo "Script available to CentOS 7!"
                echo "ERROR: This OS is not compatible" >> /var/log/ssh_gen_key.log
        exit 1
        else
            echo OS-release: $PRETTY_NAME
        fi
    fi
}


ssh_gen_key(){
        echo "Enter IP server: "
        read ip_server
        key_pri=~/.ssh/$ip_server.key
        key_pub=$key_pri.pub
        user=$(logname)
        if [ -f $key_pri ]
        then
                echo "Existed key for server."
                echo "Use ssh -o 'StrictHostKeyChecking no' -i $key_pri your_username@$ip_server to login server."
                exit 0

        else
                echo "Enter username to login: "
                read username
                echo "Enter password for user $username: "
                read password
                echo "Generating key pair..."
                ssh-keygen -t rsa -N "" -f $key_pri -q
                add_key
        fi
}

add_key()
{
        echo "Adding key on server..."

        install_sshpass
        sudo sshpass -p "$password" ssh-copy-id  -o "StrictHostKeyChecking no" -i $key_pub -f $username@$ip_server
        if [ $? -eq 0 ]; then
                sudo rm $key_pub
                echo "Use ssh -o 'StrictHostKeyChecking no' -i $key_pri $username@$ip_server to login server."
                echo "Finished."
        else
                sudo rm $key_pri*
                echo "Don't copy key on server"
        fi
}

install_sshpass()
{
        sshpass -V &> /dev/null
        if [ $? -ne 0 ]
        then
                echo "Installing sshpass ..."
                sudo yum install -y sshpass &> /dev/nul
        fi
}

main()
{
        check_distro
        ssh_gen_key
}

main