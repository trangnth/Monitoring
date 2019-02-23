## Cấu hình ELK phân tích log có từ Error

File log mẫu như [ở đây](mau_log.txt)

Cấu hình Filebeat tương tự như sau:

```sh
$ vim /etc/filebeat/filebeate.yml
- type: log
  enabled: true

  paths:
    - /root/mau_log.txt
  multiline.pattern: ^\[
  multiline.negate: true
  multiline.match: after
```

Ví dụ file cấu hình [Filebeat](config/filebeat_mbf.yml)

Thêm file filter cho Logstash như sau:

```sh
$ vim /etc/logstash/conf.d/22-filter-log-error.conf
filter {
    if [source] == "/root/mau_log.txt" {
        grok {
            patterns_dir => [ "/etc/logstash/extra_patterns" ]
            match => { "message" => "%{GREEDYDATA:preError}%{ERRORWORD:State_Error}%{GREEDYDATA:message}"
            }
            add_field => { "event_type" => "mbf_error_log"}
        #overwrite => "message"
        }
    }
}
```

Tạo một file `extra_patterns` có nội dung như sau:

```sh
$ vim /etc/logstash/extra_patterns
ERRORWORD [Ee][Rr][Rr][Oo][Rr]
```

Restart lại Logstash và Filebeat

```sh
systemctl restart logstash
systemctl restart filebeat
```

## Install elastalert trên CentOS 7 cảnh báo về slack

Chuẩn bị:
```sh
yum install epel-release -y
yum install git python-pip python-devel gcc -y
pip install --upgrade pip
```

Clone repo từ trên git:
```sh
git clone https://github.com/Yelp/elastalert
```

Cài đặt requirements
```sh
cd elastalert/
pip install --upgrade setuptools
pip install -r requirements.txt
pip install elastalert
```

Tạo file config

```sh
cp config.yaml.example config.yaml
```

Sửa file config đó:

```sh
$ vim config.yaml
...
rules_folder: alert_rules
run_every:
  minutes: 1
buffer_time:
  minutes: 15
es_host: localhost
es_port: 9200
writeback_index: elastalert_status
alert_time_limit:
  days: 2
```

Tạo Index cho ElasAlert
```sh
$ elastalert-create-index
Elastic Version:6
Mapping used for string:{'type': 'keyword'}
New index elastalert_status created
Done!
```

Tạo thư mục chứa các file rule
```sh
mkdir -p /root/elastalert/alert_rules/
```

Tạo một file rule trong thư mục vừa tạo trên để cấu hình gửi cảnh báo về slack
```sh
cat << EOF >> /root/elastalert/alert_rules/test.yml
# The following values need to be configured for your environment
es_host: 192.168.20.57
es_port: 9200

index: filebeat*
name: Notify log
type: any

filter:
- query:
    query_string:
      query: "event_type:mbf_error_log"

alert:
- "email"
- "slack"
email:
- "bosua666@gmail.com"

slack_webhook_url:
- "https://hooks.slack.com/services/xxx"
slack_channel_override: "#elastelert"
slack_username_override: "ELK-ALERT"

alert_text: |
    ElastAlert has detected a failed login attempt:
    Message: {0}
    Source Host: {1}
    Timestamp: {2}
alert_text_args:
  - "message"
  - "host.name"
  - "@timestamp"

alert_text_type: alert_text_only
EOF
```

Test rule
```sh
[root@trang-20-57 logstash]# elastalert-test-rule /root/elastalert/alert_rules/test.yml
Successfully loaded Notiy log

INFO:elastalert:Queried rule Notiy log from 2019-01-02 11:54 +07 to 2019-01-02 12:39 +07: 0 / 0 hits
INFO:elastalert:Queried rule Notiy log from 2019-01-02 12:39 +07 to 2019-01-02 13:24 +07: 0 / 0 hits
INFO:elastalert:Queried rule Notiy log from 2019-01-02 13:24 +07 to 2019-01-02 14:09 +07: 0 / 0 hits
INFO:elastalert:Queried rule Notiy log from 2019-01-02 14:09 +07 to 2019-01-02 14:54 +07: 0 / 0 hits
INFO:elastalert:Queried rule Notiy log from 2019-01-02 14:54 +07 to 2019-01-02 15:39 +07: 0 / 0 hits
```

Chạy ElasAlert

    python -m elastalert.elastalert --config /opt/elastalert/config.yaml --rule /root/elastalert/alert_rules/test.yml --verbose

Install zdaemon

    pip install zdaemon

Tạo file `zdaemon.conf`

```sh
<runner>
  program python -m elastalert.elastalert --config /root/elastalert/config.yaml --rule /root/elastalert/alert_rules/test.yml
  socket-name /tmp/elastalert.zdsock
  forever true
</runner>
```

Start zdaemon

    zdaemon -C zdaemon.conf start

Stop zdaemon

    zdaemon -C zdaemon.conf stop

