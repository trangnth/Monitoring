## Đẩy dữ liệu từ Check_mk sang mysql 

## Trên cả hai node

Trên cả hai node đều thực hiện một số các cấu hình sau:

### Cài đặt mariadb

Định nghĩa một repo cho mariadb:

```sh
$ vim /etc/yum.repos.d/mariadb.repo

[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.2/centos73-amd64/
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
```

Cài đặt Mariadb:

	yum install -y mariadb mariadb-server mariadb-devel
	yum install gcc glibc glibc-common gd gd-devel make net-snmp openssl-devel xinetd unzip httpd php php-fpm curl vim -y
	systemctl start mariadb.service
	systemctl enable mariadb.service

### Cấu hình:

```sh
cp /etc/sysctl.conf /etc/sysctl.conf_backup
sed -i '/msgmnb/d' /etc/sysctl.conf
sed -i '/msgmax/d' /etc/sysctl.conf
sed -i '/shmmax/d' /etc/sysctl.conf
sed -i '/shmall/d' /etc/sysctl.conf
printf "\n\nkernel.msgmnb = 131072000\n" >> /etc/sysctl.conf
printf "kernel.msgmax = 131072000\n" >> /etc/sysctl.conf
printf "kernel.shmmax = 4294967295\n" >> /etc/sysctl.conf
printf "kernel.shmall = 268435456\n" >> /etc/sysctl.conf
sysctl -e -p /etc/sysctl.conf
```

## Trên node DB

Đặt pass 

	/usr/bin/mysqladmin -u root password 'trang1234'

Tạo DB:

```sh
mysql -u root -p'trang1234'
CREATE DATABASE nagios DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'ndoutils'@'%' IDENTIFIED BY 'trang1234';
GRANT USAGE ON *.* TO 'ndoutils'@'%' IDENTIFIED BY 'trang1234' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0 ;
GRANT ALL PRIVILEGES ON nagios.* TO 'ndoutils'@'%' WITH GRANT OPTION ;
\q
```

## Trên node check_mk

Tải gói và giải nén:

```sh
cd /tmp
wget -O ndoutils.tar.gz https://github.com/NagiosEnterprises/ndoutils/releases/download/ndoutils-2.1.3/ndoutils-2.1.3.tar.gz
tar xzf ndoutils.tar.gz
cd /tmp/ndoutils-2.1.3/



./configure --prefix=/omd/sites/monitoring/usr/local/nagios/ --enable-mysql --with-ndo2db-user=monitoring -with-ndo2db-group=monitoring --with-mysql=/usr/lib64/mysql
```


## Tham khảo

[1] https://support.nagios.com/kb/article.php?id=406






```sh
==================user root==================
OS: centos7
----------install check_mk-------------
yum -y update
yum install -y epel-release wget
wget https://mathias-kettner.de/support/1.4.0p17/check-mk-raw-1.4.0p17-el7-64.x86_64.rpm
yum install -y check-mk-raw-1.4.0p17-el7-64.x86_64.rpm
vi /etc/sysconfig/selinux
SELINUX=enforcing thành SELINUX=disabled
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --reload
omd create hanoi
6pg37Nl3
omd start hanoi
----------install mariadb--------------
yum install -y mariadb mariadb-server mariadb-devel
yum install gcc glibc glibc-common gd gd-devel make net-snmp openssl-devel xinetd unzip httpd php php-fpm curl vim -y
yum install net-tools -y
systemctl start mariadb.service
systemctl enable mariadb.service
/usr/bin/mysqladmin -u root password 'tan124'
vim ~/.my.cnf
==>
[client]
user = root
password = tan124
mysql
CREATE DATABASE nagios DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'monitoring'@'localhost' IDENTIFIED BY 'tan124';
grant all privileges on nagios.* to 'monitoring'@localhost identified by "tan124" with grant option;
flush privileges;
quit
-------------install ndo2db------------------
cd /tmp
wget http://downloads.sourceforge.net/project/nagios/ndoutils-1.x/ndoutils-1.5.2/ndoutils-1.5.2.tar.gz
tar xvf ndoutils-1.5.2.tar.gz
cd ndoutils-1.5.2
./configure --prefix=/omd/sites/hanoi/usr/local/nagios/ --enable-mysql --disable-pgsql --with-ndo2db-user=hanoi -with-ndo2db-group=hanoi --with-mysql-lib=/usr/lib/mysql
make
make all
make install-config
cd /tmp/ndoutils-1.5.2/db
./installdb -u monitoring -p tan124 -h localhost -d nagios
chown -R hanoi. /omd/sites/hanoi/usr/local/
chmod 766 /tmp/ndoutils-1.5.2/config/ndo2db.cfg-sample
chmod 766 /tmp/ndoutils-1.5.2/config/ndomod.cfg-sample
chmod 766 /tmp/ndoutils-1.5.2/daemon-init
==========user hanoi==============
su hanoi
mkdir -p ~/usr/local/nagios/bin
mkdir -p ~/usr/local/nagios/etc
mkdir -p ~/usr/local/nagios/var
cp /tmp/ndoutils-1.5.2/src/ndomod-3x.o ~/usr/local/nagios/bin/ndomod.o
cp /tmp/ndoutils-1.5.2/src/ndo2db-3x ~/usr/local/nagios/bin/ndo2db
chmod 0744 ~/usr/local/nagios/bin/ndo*
cp /tmp/ndoutils-1.5.2/config/ndo2db.cfg-sample ~/usr/local/nagios/etc/ndo2db.cfg
cp /tmp/ndoutils-1.5.2/config/ndomod.cfg-sample ~/usr/local/nagios/etc/ndomod.cfg
cp /tmp/ndoutils-1.5.2/daemon-init ~/etc/init.d/ndo2db
chmod +x ~/etc/init.d/ndo2db
vim /omd/sites/hanoi/usr/local/nagios/etc/ndo2db.cfg
==> 
db_user=monitoring
db_pass=tan124
mkdir -p ~/var/lock/subsys
vim ~/etc/init.d/ndo2db
==>
Ndo2dbLockDir=var/lock/subsys
Ndo2dbUser=hanoi
Ndo2dbGroup=hanoi
trong function start ndo2db cua file ~/etc/init.d/ndo2db ta them dong remove socket "usr/local/nagios/var/ndo.sock" nhu sau:
start)
        status_ndo2db
        if [ $? -eq 0 ]; then
            echo "$servicename already started..."
            exit 1
        fi
        echo -n "Starting $servicename:"
        rm -rf usr/local/nagios/var/ndo.sock
        touch $Ndo2dbRunFile
        chown $Ndo2dbUser:$Ndo2dbGroup $Ndo2dbRunFile
        $Ndo2dbBin -c $Ndo2dbCfgFile
        if [ -d $Ndo2dbLockDir ]; then touch $Ndo2dbLockDir/$Ndo2dbLockFile; fi
        echo " done."
        exit 0
        ;;
printf "\n\n# NDOUtils Broker Module\n" >> /omd/sites/hanoi/etc/nagios/nagios.cfg
printf "broker_module=/omd/sites/hanoi/usr/local/nagios/bin/ndomod.o\n" >> /omd/sites/hanoi/etc/nagios/nagios.cfg
printf "config_file=/omd/sites/hanoi/usr/local/nagios/etc/ndomod.cfg\n" >> /omd/sites/hanoi/etc/nagios/nagios.cfg
cd /omd/sites/hanoi/etc/rc.d
ln -s ../init.d/ndo2db 81-ndo2db
=============root===========
omd restart hanoi
tail -f /omd/sites/hanoi/var/log/nagios.log
==> if OK
[1510629049] ndomod: Successfully reconnected to data sink!  0 items lost, 124 queued items to flush.
[1510629049] ndomod: Successfully flushed 124 queued items to data sink.
==> if not OK
[1510569392] ndomod: Still unable to connect to data sink.  0 items lost, 278 queued items to flush.
[1510569408] ndomod: Still unable to connect to data sink.  0 items lost, 392 queued items to flush.
==============================================
```


