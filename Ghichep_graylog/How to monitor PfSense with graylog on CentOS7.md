# Pfsense 2.4.3 + graylog 3.0 on centos7


## 1. Chuẩn bị 

* Cài đặt các gói cần thiết 

```sh
yum -y install wget pwgen java-1.8.0-openjdk-headless
java -version
```

### Cài đặt Elasticsearch

```sh
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
cat <<EOF > /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-6.x]
name=Elasticsearch repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

yum install -y elasticsearch
systemctl daemon-reload
systemctl enable elasticsearch
```

* Chỉnh sửa file cấu hình `/etc/elasticsearch/elasticsearch.yml` như sau:

```sh
cluster.name: graylog
node.name: ${HOSTNAME}
network.host: 0.0.0.0
http.port: 9200
```

* Khởi động lại service:

```sh
systemctl restart elasticsearch
curl -X GET http://localhost:9200
curl -XGET 'http://localhost:9200/_cluster/health?pretty=true'
```

* Kết quả:

```sh
[root@trang-graylog ~]# curl -X GET http://localhost:9200

{
  "name" : "trang-graylog.novalocal",
  "cluster_name" : "graylog",
  "cluster_uuid" : "1cFxpvRpTC6cbY336Ttaeg",
  "version" : {
    "number" : "6.8.3",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "0c48c0e",
    "build_date" : "2019-08-29T19:05:24.312154Z",
    "build_snapshot" : false,
    "lucene_version" : "7.7.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
[root@trang-graylog ~]#
[root@trang-graylog ~]# curl -XGET 'http://localhost:9200/_cluster/health?pretty=true'
{
  "cluster_name" : "graylog",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 0,
  "active_shards" : 0,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```



### Cài đặt MongoDB

```sh
cat <<EOF > /etc/yum.repos.d/mongodb-org-4.0.repo
[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
EOF

yum install -y mongodb-org
systemctl start mongod
systemctl enable mongod
```

**Lưu ý**: Nếu lúc cài đặt bị lỗi do repo không đúng, thì xóa file định nghĩa repo phía trên đi, sau đó tạo lại và copy/paste nội dung vào file đó.


### Cài đặt graylog

```sh
rpm -Uvh https://packages.graylog2.org/repo/packages/graylog-3.0-repository_latest.rpm
yum -y install graylog-server
```

* Chạy lệnh sau để lấy output

```sh
[root@trang-graylog ~]# pwgen -N 1 -s 96
feyYyKk3oRAc1qwtBxksYQpkfjYDTzCpHL8dHqrdywYSyJwQimzypEoJ4vi60HH0lxtyYicmPvqGh658vbouEr68VjKasFPb

## Replace your password 
[root@trang-graylog ~]# echo -n trang1234  | sha256sum
a295d92dee2a966b136c5c3ea356d33feab38f00bf5c18e2a82fc74000986394  -

```

* Sau đó chỉnh sửa file cấu hình `/etc/graylog/server/server.conf` lần lượt với các output như sau

```sh
password_secret = feyYyKk3oRAc1qwtBxksYQpkfjYDTzCpHL8dHqrdywYSyJwQimzypEoJ4vi60HH0lxtyYicmPvqGh658vbouEr68VjKasFPb
root_password_sha2 = a295d92dee2a966b136c5c3ea356d33feab38f00bf5c18e2a82fc74000986394  -
root_email = "tranguet@gmail.com"
root_timezone = UTC
is_master = true
elasticsearch_max_docs_per_index = 20000000
elasticsearch_max_number_of_indices = 20
elasticsearch_shards = 1
elasticsearch_replicas = 0
```

### Cấu hình web interface cho graylog

* Chỉnh sửa file cấu hình `/etc/graylog/server/server.conf`

```sh
# IP graylog
http_bind_address = 192.168.20.194:9000
```

* Khởi động Graylog service 

```sh
systemctl daemon-reload
systemctl restart graylog-server
systemctl enable graylog-server
```

* Nếu Firewall đang được sử dụng

```sh
firewall-cmd --permanent --add-port=9000/tcp
firewall-cmd --reload
```

Truy cập vào địa chỉ http://192.168.20.194:9000 và login với user/password là admin/trang1234

<img src="img/1.png">









## Tham khảo 

[1] https://www.itzgeek.com/how-tos/linux/centos-how-tos/how-to-install-graylog-on-centos-7-rhel-7.html

[2] https://github.com/opc40772/pfsense-graylog