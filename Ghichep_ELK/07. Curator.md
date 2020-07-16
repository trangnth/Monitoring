## Elasticsearch Curator 

1. [Overview](#overview)

2. [Deployment](#deployment)

3. [Research](#research)

4. [Reference](#reference)


<a name="overview"></a>
## 1. Overview

Elasticsearch Curator là một công cụ giúp bạn quản lý (curate) các Elasticsearch indices và snapshot của bạn:

* Lấy toàn bộ một danh sách đầy đủ các indices hoặc snapshots trong cluster của bạn, như *actionable list*
* Lặp đi lặp lại một danh sách các user được định nghĩa trong `filter` để xóa bỏ dần các indices từ *actionable list* khi cần thiết
* Thực hiện các hành động khác nhau cho mỗi items còn lại trong *actionable list*

Curator cho phép thực hiện nhiều thao tác khác nhau với indices và snapshots, bào gồm:

* Add or remove indices (or both!) from an alias
* Change shard routing allocation
* Close indices
* Create index
* Delete indices
* Delete snapshots
* Open closed indices
* forceMerge indices
* reindex indices, including from remote clusters
* Change the number of replicas per shard for indices
* rollover indices
* Take a snapshot (backup) of indices
* Restore snapshots

Curator sẽ luôn luôn có một *command-line tool* để thao tác.


<a name="deployment"></a>
## 2. Deployment

### 2.1 Installation 

Có nhiều cách cài đặt để sử dụng, ở đây tôi sẽ chọn cài đặt bằng `pip`

Đầu tiên sẽ cần cài đặt `pip`:

* Trên Ubuntu:

		sudo apt-get install python-pip -y

* Trên CentOS:

		sudo yum install python-pip -y

Sau đó thực hiện cài đặt Curator:

	sudo pip install elasticsearch-curator

Kiểm tra lại việc cài đặt:

```sh
[root@trang-20-57 .curator]# curator --version
curator, version 5.6.0
```

Upgrading:

	pip install -U elasticsearch-curator

Nếu muốn cài đặt một phiên nhất định nào đó, thực hiện câu lệnh dưới đây với version tương ứng:

	pip install -U elasticsearch-curator==X.Y.Z


### 2.2 Use case 

Sử dụng Curator để xóa các log cũ, đã lâu, chỉ giữ lại các log trong một khoảng thời gian nhất định gần nhất.

Tạo thư mục chứa file cấu hình nếu chưa có 

```sh
$ mkdir ~/.curator/
$ touch ~/.curator/curator.yml
```

Tạo một file cấu hình để kết nối tới Elasticsearch (hoặc Cluster):
```sh
$ cat << EOF >> ~/.curator/curator.yml
client:
  hosts:
    - <IP_Elasticsearch>
  port: 9200
  url_prefix:
  use_ssl: False
  certificate:
  client_cert:
  client_key:
  ssl_no_validate: False
  http_auth:
  timeout: 30
  master_only: False

logging:
  loglevel: INFO
  logfile:
  logformat: default
  blacklist: ['elasticsearch', 'urllib3']
EOF
```

Tạo một file thực hiện xóa tất cả các index trước thời điểm hiện tại là 16 ngày
```sh
$ cat << EOF >> ~/.curator/curator-action.yml
actions:
  1:
    action: delete_indices
    description: "Delete indices"
    filters:
    -
      filtertype: age
      source: name
      direction: older
      timestring: '%Y.%m.%d'
      unit: days
      unit_count: 16
      exclude:
EOF
```

Test thử như sau (date_now = 05/01/2019):

```sh
[root@trang-20-57 .curator]# curator curator-action.yml  
2019-01-05 08:40:26,508 INFO      Preparing Action ID: 1, "delete_indices"
2019-01-05 08:40:26,560 INFO      Trying Action ID: 1, "delete_indices": Delete indices
2019-01-05 08:40:26,645 INFO      Deleting selected indices: [u'filebeat-2018.12.20', u'metricbeat-2018.12.20']
2019-01-05 08:40:26,645 INFO      ---deleting index filebeat-2018.12.20
2019-01-05 08:40:26,645 INFO      ---deleting index metricbeat-2018.12.20
2019-01-05 08:40:27,434 INFO      Action ID: 1, "delete_indices" completed.
2019-01-05 08:40:27,434 INFO      Job completed.
```

Kết quả như trên cho thấy đã xóa được hai indices của ngày 20/12/2018 do dữ liệu đã cũ (lâu hơn 16 ngày trước)

Tạo một crontab để kiểm tra và xóa dữ liệu hàng ngày và lưu lại log:

```sh
$ sudo vim /etc/crontab
...
0 0 * * * /bin/curator --config ~/.curator/curator.yml ~/.curator/curator-action.yml >> /var/log/curator.log 2>&1
```


<a name="research"></a>
## 3. Research

### Configuration File

Khi curator thực hiện lệnh, nếu không chỉ rõ đường dẫn tới file cấu hình với tùy chọn `--config`, thì mặc định nó sẽ load file ở path `~/.curator/curator.yml` 

Configuration File sẽ gồm client connection và cài đặt logging được viết dưới dạng file YAML, ví dụ:

```sh
---
# Remember, leave a key empty if there is no value.  None will be a string,
# not a Python "NoneType"
client:
  hosts:
    - 127.0.0.1
  port: 9200
  url_prefix:
  use_ssl: False
  certificate:
  client_cert:
  client_key:
  ssl_no_validate: False
  http_auth:
  timeout: 30
  master_only: False

logging:
  loglevel: INFO
  logfile:
  logformat: default
  blacklist: ['elasticsearch', 'urllib3']
```

#### hosts

Có thể là single value:

	hosts: 127.0.0.1

hoặc multiple value:

* Flow:
```sh
hosts: [ "10.0.0.1", "10.0.0.2" ]
```

* Spanning:
```sh
hosts: [ "10.0.0.1",
    "10.0.0.2" ]
```
* Block:
```sh
hosts:
  - 10.0.0.1
  - 10.0.0.2
```

* Hoặc có thể cấu hình luôn cùng port đi kèm và bỏ qua tùy chọn `port` tiếp theo:

```sh
hosts:
  - 10.0.0.1:9200
  - 10.0.0.2:9201
```

#### port

Nên để single value:

```sh
port: 9200
```

#### Other

Ngoài ra nếu muốn tùy chỉnh thêm một vài các tùy chọn khác có thể tham khảo [ở đây](https://www.elastic.co/guide/en/elasticsearch/client/curator/5.6/configfile.html)


### Action File 

Một Action file có cấu trúc như sau:

```sh
actions:
  1:
    action: ACTION1
    description: OPTIONAL DESCRIPTION
    options:
      option1: value1
      ...
      optionN: valueN
      continue_if_exception: False
      disable_action: True
    filters:
    - filtertype: *first*
      filter_element1: value1
      ...
      filter_elementN: valueN
    - filtertype: *second*
      filter_element1: value1
      ...
      filter_elementN: valueN
  2:
    action: ACTION2
    description: OPTIONAL DESCRIPTION
    options:
      option1: value1
      ...
      optionN: valueN
      continue_if_exception: False
      disable_action: True
    filters:
    - filtertype: *first*
      filter_element1: value1
      ...
      filter_elementN: valueN
    - filtertype: *second*
      filter_element1: value1
      ...
      filter_elementN: valueN
  3:
    action: ACTION3
    ...
  4:
    action: ACTION4
    ...
```

Key gốc để bắt đầu luôn là `actions`, sau đó có thể là bất kỳ một action nào khác được viết xuống dưới. Các Actions luôn được thực hiện và hoàn thành theo thứ tự.

High-level elements của mỗi một số được đánh là:

* `action`
* `description`
* `options`
* `filters`


#### description

Đây là tùy chọn cho phép miêu tả các hành động và filter những việc được hỗ trợ

```sh
description: >- I can make the description span multiple
    lines by putting ">-" at the beginning of the line,
    as seen above.  Subsequent lines must also be indented.
options:
  option1: ...
```


<a name="reference"></a>
### 4. Reference

https://www.elastic.co/guide/en/elasticsearch/client/curator/5.6/pip.html

https://fabianlee.org/2017/04/03/elk-using-curator-to-manage-the-size-and-persistence-of-your-index-storage/