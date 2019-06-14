## Checkmk + Qemu-KVM

Hướng dẫn cấu hình Check_mk get info về ram, cpu của các VM trên KVM

**Bước 1**: Cài đặt gói mkp trên check_mk server 

```sh
cd /opt
wget https://checkmk.com/check_mk-exchange-download.php?file=qemu-1.0.mkp
su monitoring
mkp install /opt/check_mk-exchange-download.php\?file\=qemu-1.0.mkp
mkp list
```

**Bước 2:** Trên client, tạo một file script để thực hiện lấy các thông tin của các instance:

Kiểm tra thư mục local để đặt script

```sh
[root@mdt-server36 ~]# check_mk_agent | head
<<<check_mk>>>
Version: 1.5.0p16
AgentOS: linux
Hostname: mdt-server36
AgentDirectory: /etc/check_mk
DataDirectory: /var/lib/check_mk_agent
SpoolDirectory: /var/lib/check_mk_agent/spool
PluginsDirectory: /usr/lib/check_mk_agent/plugins
LocalDirectory: /usr/lib/check_mk_agent/local
<<<df>>>
```

Đặt script vào thư mục 	`/usr/lib/check_mk_agent/local`

```sh
cd /usr/lib/check_mk_agent/local
wget https://raw.githubusercontent.com/Bastian-Kuhn/Check_MK-Treasures/master/qemu/src/agents/plugins/qemu
chmod +x qemu
```

Chạy thử script:

```sh
[root@mdt-server36 local]# ./qemu
<<<qemu>>>
2 hungnt-ctl2 running 8192 113.3 12.3
3 hungnt-ctl3 running 8192 100.0 10.9
4 hungnt-com1 running 4096 60.0 6.0
5 hungnt-com2 running 4096 6.7 6.1
13 hungnt-ceph1 running 4096 33.3 6.0
14 hungnt-ceph2 running 4096 26.7 5.9
15 hungnt-ceph3 running 4096 20.0 6.1
36 hungnt-ctl1 running 8192 31.2 11.9
37 trang-ctl running 6144 146.7 9.4
38 trang-com1 running 4096 6.7 6.2
39 trang-com2 running 4096 6.7 5.5
42 trang_checkmk running 2048 0.0 3.1
```

**Bước 3:** Kiểm tra trên web check_mk

<img src="img/33.png">

**Bước 4:** Thiết lập các ngưỡng cảnh báo, thực hiện trên Wato theo các bước sau:

<img src="img/34.png">

<img src="img/35.png">

Tạo một rule mới 

<img src="img/36.png">

<img src="img/37.png">

Lưu rule lại, và check lại các service trên host

<img src="img/38.png">

<img src="img/39.png">

<img src="img/40.png">




## Tham khảo

[1] https://checkmk.com/check_mk-exchange-file.php?&file=qemu-1.0.mkp

[2] https://github.com/Bastian-Kuhn/Check_MK-Treasures/tree/master/qemu
