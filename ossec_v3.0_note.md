# Installations requirements 

yum install mysql-devel postgresql-devel -y
yum install sqlite-devel -y 
sudo yum groupinstall 'Development Tools' -y 
yum install -y gcc inotify-tools
yum install -y mariadb-server httpd
yum install php php-common php-opcache php-mcrypt php-cli php-gd php-curl php-mysqlnd -y

# Manager/Agent Installation

cd /opt
wget -U ossec https://bintray.com/artifact/download/ossec/ossec-hids/ossec-hids-2.8.3.tar.gz
wget -U ossec https://raw.githubusercontent.com/ossec/ossec-docs/master/docs/whatsnew/checksums/2.8.3/ossec-hids-2.8.3.tar.gz.sha256
cat ossec-hids-2.8.3.tar.gz.sha256
sha256sum -c  ossec-hids-2.8.3.tar.gz.sha256 ossec-hids-2.8.3.tar.gz
tar -zxvf ossec-hids-2.8.3.tar.gz
cd ossec-hids-2.8.3
./install.sh

# Start Ossec

/var/ossec/bin/ossec-control start
/var/ossec/bin/ossec-control enable database


# Config web-ui

cd /var/www/html/
wget https://github.com/ossec/ossec-wui/archive/master.zip
unzip master.zip
mv ossec-wui-master/ ossec/

mkdir ossec/tmp/
chown www-data: -R ossec/
chmod 666 /var/www/html/ossec/tmp
apachectl restart





## Tham khảo

[1] https://www.vultr.com/docs/how-to-install-ossec-hids-on-a-centos-7-server
