## Plugin Unixsock

Trên CentOS7

Chỉnh sửa file config:

	vim /etc/collectd.conf

Bỏ comment những dòng sau:

```sh
LoadPlugin unixsock
...
<Plugin unixsock>
        SocketFile "/var/run/collectd-unixsock"
        SocketGroup "collectd"
        SocketPerms "0660"
        DeleteSocket false
</Plugin>
...
```

Khởi động lại dịch vụ:

	systemctl restart collectd

Kiểm tra lại trạng thái dịch vụ:

	systemctl status collectd

Nếu hiển thị như sau là ok:

```sh
● collectd.service - Collectd statistics daemon
   Loaded: loaded (/usr/lib/systemd/system/collectd.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2018-11-01 11:59:17 +07; 5s ago
     Docs: man:collectd(1)
           man:collectd.conf(5)
 Main PID: 11557 (collectd)
   CGroup: /system.slice/collectd.service
           └─11557 /usr/sbin/collectd

Nov 01 11:59:17 trang-20-54 collectd[11557]: plugin_load: plugin "interface" successfully loaded.
Nov 01 11:59:17 trang-20-54 collectd[11557]: plugin_load: plugin "load" successfully loaded.
Nov 01 11:59:17 trang-20-54 collectd[11557]: plugin_load: plugin "memory" successfully loaded.
Nov 01 11:59:17 trang-20-54 systemd[1]: Started Collectd statistics daemon.
Nov 01 11:59:17 trang-20-54 collectd[11557]: plugin_load: plugin "ping" successfully loaded.
Nov 01 11:59:17 trang-20-54 collectd[11557]: plugin_load: plugin "unixsock" successfully loaded.
Nov 01 11:59:17 trang-20-54 collectd[11557]: plugin_load: plugin "write_graphite" successfully loaded.
Nov 01 11:59:17 trang-20-54 collectd[11557]: ping plugin: MaxMissed < 0, disabled re-resolving of hosts
Nov 01 11:59:17 trang-20-54 collectd[11557]: Systemd detected, trying to signal readyness.
Nov 01 11:59:18 trang-20-54 collectd[11557]: Initialization complete, entering read-loop
```

Còn một số trường có thể bị lỗi do không có file `/var/run/collectd-unixsock` hoặc không có quyền truy cập thì hay thử một số cách sau:

* Tạo file mới `/var/run/collectd-unixsock` phân quyền và group cho nó
* Nếu đã có file rồi mà báo file đã được sử dụng thì xóa đi tạo lại
* Nếu báo lỗi về group `collectd` thì `chgrp collectd /var/run/collectd-unixsock`
* Chú ý để đúng tên thư mục trong file cấu hình trùng với path mà `collectdctl` gọi

```sh
[root@controller home]# collectdctl listval
ERROR: Failed to connect to daemon at unix:/var/run/collectd-unixsock: Connection refused.
```
 