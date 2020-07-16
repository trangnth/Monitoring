# NOTE

## Một số lệnh kiểm tra thông tin CPU
```sh
cat /proc/cpuinfo
lscpu
```


### Lệnh cpuid

```sh
$ yum install cpuid
$ cpuid
```

### Một số cách và ý nghĩa các trường hợp cấu hình IP

* IP localhost 

```sh
127.0.0.1
```

* Nếu có hỗ trợ IPv6 thì localhost có thể được viết các cách như sau:

```sh
127.0.0.1
::127.0.0.1
::ffff:127.0.0.1
```

* Để allow tất các IPv4 và IPv6

```sh
::/0
```

* Để cho phép tất cả các IPv4 (không bao gồm IPv6)

```sh
0.0.0.0/0
```

* Kết hợp nhiều IP và Domain

```sh
127.0.0.1,192.168.1.0/24,::1,2001:db8::/32,zabbix.example.com
```



## Tham khảo

[1] https://cuongquach.com/top-8-lenh-kiem-tra-thong-tin-cpu-tren-linux.html