## Check_mk Check Tomcat 7

	Version Tomcat 7.0.76-8.el7_5
	OS CentOS 7

### Install Tomcat

Mặc định khi cài đặt trên CentOS 7 sẽ là Tomcat 7

	sudo yum install tomcat 

Thêm dòng sau vào file `/usr/share/tomcat/conf/tomcat.conf`

	JAVA_OPTS="-Djava.security.egd=file:/dev/./urandom -Djava.awt.headless=true -Xmx512m -XX:MaxPermSize=256m -XX:+UseConcMarkSweepGC"

### Install Admin Packages

Cài đặt Tomcat root page mặc định (tomcat_webapps), Tomcat Web Application Manager và Virtual Host Manager (tomcat-admin-webapps):

	sudo yum install tomcat-webapps tomcat-admin-webapps 

Cấu hình Tomcat Web Management Interface trong file:

	vim /usr/share/tomcat/conf/tomcat-users.xml

Ví dụ, muốn thêm user cho phép truy cập vào manager-gui và admin-gui

```sh
<tomcat-users>
...
<role rolename="manager"/>
<role rolename="manager-gui"/>
<role rolename="admin"/>
<role rolename="admin-gui"/>
<role rolename="jolokia"/>
<role rolename="jolokia-gui"/>
<user username="admin" password="password" roles="manager,manager-gui,admin,admin-gui,jolokia,jolokia-gui"/>
...
</tomcat-users>
```

### Jolokia 

Tải file `jolokia.war` vào đường dẫn `/var/lib/tomcat/webapps` có cấu trúc như sau:

```sh
[root@trang-20-56 webapps]# ll
total 344
drwxr-xr-x. 8 tomcat tomcat    127 Dec  4 13:59 examples
drwxr-xr-x. 5 root   tomcat     87 Dec  4 13:59 host-manager
drwxr-xr-x. 4 tomcat tomcat     37 Dec  4 14:06 jolokia
-rw-r--r--. 1 root   root   344230 Dec  4 14:06 jolokia.war
drwxr-xr-x. 5 root   tomcat    103 Dec  4 13:59 manager
drwxr-xr-x. 3 tomcat tomcat   4096 Dec  4 13:59 ROOT
drwxr-xr-x. 5 tomcat tomcat     86 Dec  4 13:59 sample
```

### Start Tomcat

	sudo systemctl start tomcat
	sudo systemctl enable tomcat

Truy cập vào trang web `http://server_IP_address:8080`

### Cấu hình check_mk agent

Tải file `mk_jolokia` trên server về, và đặt tại thư mục `/usr/lib/check_mk_agent/plugins` của agent, file `jolokia.cfg` đặt ở `/etc/check_mk_agent/` (có thể tải trực tiếp trên giao diện web hoặc trong thư mục lưu trữ của server)

Sửa cấu hình file jolokia.cfg như sau:

```sh
# Settings for authentication
protocol = "http"
server   = "127.0.0.1"
user     = "admin"
password = "password"
#mode     = "digest"
# use "basic_preemptive" if server responds with 403 forbidden even
# though user/password are correct
mode     = "basic_preemptive"
suburi   = "jolokia"
instance = None

```

Lên web check_mk discovery các service


## Tham khảo

https://www.digitalocean.com/community/tutorials/how-to-install-apache-tomcat-7-on-centos-7-via-yum