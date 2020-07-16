# Hướng dẫn cấu hình nâng cấp phiên bản cho Grafana server 

**Bước 1**: Backup database và file cấu hình

* Copy database và file cấu hình của grafana:

```sh
cp /var/lib/grafana/grafana.db /opt/
cp /etc/grafana/grafana.ini /opt/
```

* Sử dụng yum để update version 

```sh 
sudo yum upgrade grafana -y
```

* Upgrade thành công từ phiên bản 6.1.6 lên phiên bản 6.4.4

```sh
...
  Updating   : grafana-6.4.4-1.x86_64                                                                                                      1/2
  Cleanup    : grafana-6.1.6-1.x86_64                                                                                                      2/2
POSTTRANS: Running script
  Verifying  : grafana-6.4.4-1.x86_64                                                                                                      1/2
  Verifying  : grafana-6.1.6-1.x86_64                                                                                                      2/2

Updated:
  grafana.x86_64 0:6.4.4-1

Complete!

[root@trang-68-110 ~]# grafana-server -v
Version 6.4.4 (commit: 092e514, branch: HEAD)
```

* Kiểm tra lại file cấu hình và database, nếu không có gì thay đổi thì không cần restore lại.

