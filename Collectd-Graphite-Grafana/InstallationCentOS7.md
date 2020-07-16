## Install graphite web on CentOS7

```sh
yum install epel-release -y
yum --enablerepo=epel -y install graphite-web python-carbon

```

Bỏ comment và sửa file `/etc/graphite-web/local_settings.py` ở các dòng sau:

```sh
...
SECRET_KEY = 'UNSAFE_DEFAULT'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
```

File `/etc/httpd/conf.d/graphite-web.conf`

```sh
...
Require local
Require ip 192.168.20.0/24 # Your ip local
...
```

#### Tạo Database

    /usr/lib/python2.7/site-packages/graphite/manage.py syncdb 

Sau đó nhập username và password để quản trị. `root:ITC*123@654`

Một số tùy chọn khác như:

* Thay đổi password cho user 
        
        /usr/lib/python2.7/site-packages/graphite/manage.py changepassword {YOUR_USERNAME}

* Tạo một username mới:

        /usr/lib/python2.7/site-packages/graphite/manage.py createsuperuser

Khởi động dịch vụ:

```sh
chown -R apache. /var/lib/graphite-web 
systemctl start carbon-cache 
systemctl enable carbon-cache 
systemctl restart httpd 
```

Nếu SELinux đang bật thì thay đổi giá trị boolean như sau:

    setsebool -P httpd_can_network_connect on

Nếu firewall đang bật:

    firewall-cmd --add-port=80/tcp
    firewall-cmd --add-port=80/tcp --permanent
    firewall-cmd --add-port=2003/tcp --permanent
    firewall-cmd --add-port=2003/udp --permanent
    firewall-cmd --reload

Nếu muốn log rotation hàng ngày thì sử cấu hình trong file sau: `/etc/carbon/carbon.conf`

    ENABLE_LOGROTATION = True

Nếu để dòng trên với giá trị `False` thì carbon sẽ tự động mở lại file cũ (ngày hôm trước) để tiếp tục ghi, còn nếu để `True` thì hàng ngày logrotate daemon sẽ được thực hiện, và carbon sẽ mổ một file mới để ghi.

#### Cấu hình carbon-schemas.conf

    $ vim /etc/carbon/storage-schemas.conf
    ...
    [default_2min_for_120day]
    pattern = .*
    retentions = 120s:120d
    ...

Ở đây, tôi để cấu hình cho carbon lấy tất cả các metric đẩy về theo chu kỳ 120s lấy một lần (làm data point) và lưu trong 120 ngày

Ngoài ra có thể tham khảo thêm [ở đây](https://github.com/hocchudong/thuctap012017/blob/master/TamNT/Graphite-Collectd-Grafana/docs/5.Cai_dat_Graphite-Collectd.md)

Khởi động lại carbon:

    systemctl start carbon-cache

Có thể cấu hình thêm phần carbon-relay, để chạy graphite cluster.



## Install collectd on CentOS7

    yum update
    yum install epel-release -y 
    yum install collectd -y 

Sửa file cấu hình: `/etc/collectd.conf`

```sh
...
Hostname    "compute02"
FQDNLookup   false
...
```

Khởi động dịch vụ:

    systemctl enable collectd
    systemctl start collectd

Cấu hình một số các plugin để đẩy log về graphite:

```sh
$ vim /etc/collectd.conf

...
LoadPlugin write_graphite
LoadPlugin unixsock
LoadPlugin virt
...

LoadPlugin interface
LoadPlugin load
LoadPlugin disk
LoadPlugin memory
Interval 120
<Plugin memory>
        ValuesAbsolute true
        ValuesPercentage false
</Plugin>

LoadPlugin network
LoadPlugin df
<Plugin df>
#       Device "/dev/sda1"
#       Device "192.168.0.2:/mnt/nfs"
#       MountPoint "/home"
#       FSType "ext3"

        # ignore rootfs; else, the root file-system would appear twice, causing
        # one of the updates to fail and spam the log
        FSType rootfs
        # ignore the usual virtual / temporary file-systems
        FSType sysfs
        FSType proc
        FSType devtmpfs
        FSType devpts
        FSType tmpfs
        FSType fusectl
        FSType cgroup
        IgnoreSelected true

#       ReportByDevice false
#       ReportReserved false
#       ReportInodes false

       ValuesAbsolute false
       ValuesPercentage true
</Plugin>

...
<Plugin unixsock>
    SocketFile "/var/run/collectd-unixsock"
    SocketGroup "collectd"
    SocketPerms "0770"
    DeleteSocket false
</Plugin>
...
<Plugin "virt">
   RefreshInterval 120
   Connection "qemu:///system"
   BlockDeviceFormat "target"
   HostnameFormat "uuid"
   InterfaceFormat "address"
   PluginInstanceFormat name
   ExtraStats "cpu_util disk_err domain_state fs_info job_stats_background perf vcpupin"
</Plugin>
...
<Plugin write_graphite>
  <Node "graphite">
    # Chanege Your ip graphite    
    Host "192.168.20.56"
    Port "2003"
    Protocol "tcp"
    LogSendErrors true
    Prefix "collectd.compute2."
    #Postfix "collectd"
    StoreRates true
    AlwaysAppendDS false
    EscapeCharacter "_"
  </Node>
</Plugin>
...
```

Xem chi tiết hơn về cấu hình một số các Plugin [ở đây](https://github.com/trangnth/Monitor/tree/master/Colletcd-Graphite-Grafana)

Nếu bị lỗi với plugin virt thi có thế khi cài đặt bị thiếu gói, cần cài thêm gói:

    yum install collectd-virt.x86_64 -y 


## Install Grafana on CentOS7

Tạo repo với OSS releases

```sh
cat > /etc/yum.repos.d/grafana.repo <<'EOF'
# update 03/05/2020
# by trangnth
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF
```

Install Grafana:

    yum install epel-release -y
    yum --enablerepo=grafana -y install grafana initscripts fontconfig


File cấu hình:

```sh
$ vim /etc/grafana/grafana.ini
...
[server]
# Protocol (http, https, socket)
;protocol = http

# The ip address to bind to, empty will bind to all interfaces
;http_addr =

# The http port  to use
;http_port = 3000
...
```

Khởi động dịch vụ:

    systemctl start grafana-server 
    systemctl enable grafana-server

Nếu firewall đang bật:

    firewall-cmd --add-port=3000/tcp --permanent 
    firewall-cmd --reload

Truy cập vào theo đường link sau: `http://<ip_server_grafana>:3000` với username và password là admin:admin.

Sau đó vào giao diện grafana add data source graphite vào để liên kết với graphite server

<img src="3.\ Grafanaimg/img/1.png">

Nếu muốn grafana sử dụng port khác thì cần chạy lệnh sau:

    sudo setcap 'cap_net_bind_service=+ep' /usr/sbin/grafana-server

Sau đó sửa port cấu hình trong file "/etc/grafana/grafana.ini" sang port muốn đổi, rồi restart lại dịch vụ


#####################

vi /etc/collectd.conf

cd /opt/
rpm -i collectd-*
systemctl restart collectd
systemctl enable collectd

########

## Tham khảo

https://collectd.org/wiki/index.php/Interval


## Chú ý

Có thể cài đặt collectd trên centOS bằng cách tải xuống các gói cần thiết

Chạy lệnh sau để cài đặt nếu có internet để biết được những gói nào sẽ được download:

    yum install --downloadonly --downloaddir=/root/ collectd collectd-virt

Hai gói cần download là `collectd-5.8.1-1.el7.x86_64.rpm` và `collectd-virt-5.8.1-1.el7.x86_64.rpm`

    wget http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/c/collectd-5.8.1-1.el7.x86_64.rpm
    wget http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/c/collectd-virt-5.8.1-1.el7.x86_64.rpm

Cài đặt:
   
    rpm -i collectd-*

Ví dụ cấu hình collectd thu thập dữ liệu của các máy ảo thông qua libvirt:

```sh
Hostname    "compute1"
FQDNLookup   false

LoadPlugin write_graphite
LoadPlugin unixsock
LoadPlugin virt
Interval 60

<Plugin unixsock>
    SocketFile "/var/run/collectd-unixsock"
    SocketGroup "collectd"
    SocketPerms "0770"
    DeleteSocket false
</Plugin>

<Plugin "virt">
   RefreshInterval 60
   Connection "qemu:///system"
   BlockDeviceFormat "target"
   HostnameFormat "uuid"
   InterfaceFormat "address"
   PluginInstanceFormat name
   ExtraStats "cpu_util disk_err domain_state job_stats_background perf vcpupin"
</Plugin>

<Plugin write_graphite>
  <Node "graphite">
        # Chanege Your ip graphite
    Host "192.168.40.129"
    Port "2003"
    Protocol "tcp"
    LogSendErrors true
    Prefix "collectd.compute1."
    #Postfix "collectd"
    StoreRates true
    AlwaysAppendDS false
    EscapeCharacter "_"
  </Node>
</Plugin>
```