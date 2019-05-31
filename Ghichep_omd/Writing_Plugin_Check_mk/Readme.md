# Writing checks for Check_mk

[**Tham khảo chính từ MinhKMA**](https://github.com/MinhKMA/plugin_checkMK)

Có hai cách viết plugin chính cho check_mk theo kiểu nrpe:

1. Local check: 

Trên client sẽ có một chương trình output ra màn hình như sau:

```sh
<<<check_mysql>>
total queries : 10
```

Trong đó: 

* Tên chương trình sẽ là `check_mysql`
* Output hiển thị trên check_mk sẽ là: `total queries : 10`

Trên server plugin sẽ được gọi bằng command


2. Plugin check

#### Trên agent 

Bạn sẽ viết một chương trình python cũng có output:

```sh
<<<check_mysql>>
total queries : 10
```

Chương trình này được đặt ở thư mục chứa các plugin của agent là: `/usr/lib/check_mk_agent/plugins`, hoặc có thể kiểm tra đường dẫn trên máy bạn bằng câu lệnh sau:

```sh
$ check_mk_agent | head
<<<check_mk>>>
Version: 1.5.0p5
AgentOS: linux
Hostname: trang-20-53
AgentDirectory: /etc/check_mk
DataDirectory: /var/lib/check_mk_agent
SpoolDirectory: /var/lib/check_mk_agent/spool
PluginsDirectory: /usr/lib/check_mk_agent/plugins
LocalDirectory: /usr/lib/check_mk_agent/local
<<<df>>>
```

Chương trình này cần `chmod +x`

### Trên server

Trên server sẽ có một chương trình để xử lý cái output của agent và một chương trình xử lý việc hiển thị trên dashboard

```sh
[root@trang-20-53 check_mk]# tree
.
├── agents
│   ├── bakery
│   ├── linux
│   │   └── alert_handlers
│   ├── plugins
│   └── special
├── alert_handlers
├── checkman
├── checks
├── inventory
├── locale
├── mibs
├── notifications
├── pnp-rraconf
├── pnp-templates
├── reporting
│   └── images
└── web
    ├── htdocs
    │   └── images
    └── plugins
        ├── config
        ├── dashboard
        ├── icons
        ├── metrics
        ├── pages
        ├── perfometer
        ├── sidebar
        ├── views
        ├── visuals
        └── wato

31 directories, 0 files
```

File xử lý output `check_mk_info` sẽ đặt trong thư mục `checks`, file này sẽ có tên trùng với tên file trên agent

File dùng để hiện thị thanh trạng thái `check_mk_info.py` sẽ được đặt ở `web/plugins/perfometer` 

### Debug

	check_mk --debug -nv --checks=check_mk_info WEB 

Trong đó:

* `check_mk_info` là tên của plugin 
* `WEB` là tên của agent được đặt ở trên dashboard


## Tham khảo

[1] https://mathias-kettner.de/checkmk_writing_checks.html

[2] https://minhkma.github.io/2018/10/plugin_checkmk_openstack/

[3] http://www2.steinkogler.org/steinkogler.org/2016/08/21/check-mk-write-your-own-check/


> `/opt/omd/versions/1.5.0p5.cre/share/check_mk/checks`<br>
> `/opt/omd/sites/monitoring/share/check_mk/checks`
