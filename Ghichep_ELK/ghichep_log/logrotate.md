# Ghi chép về logrotate

Môi trường tìm hiểu: Centos 7

## 1. Cấu hình

File cấu hình chung được đặt tại `/etc/logrotate.conf`, một số các file cấu hình khác cho các ứng dụng hoặc nếu bạn muốn tự định nghĩa sẽ được đặt tại `/etc/logrotate.d/`

Ví dụ về file cấu hình mặc định của CentOS:

```sh
[root@mdt-server31 images]# cat /etc/logrotate.conf
# see "man logrotate" for details
# rotate log files weekly
weekly

# keep 4 weeks worth of backlogs
rotate 4

# create new (empty) log files after rotating old ones
create

# use date as a suffix of the rotated file
dateext

# uncomment this if you want your log files compressed
#compress

# RPM packages drop log rotation information into this directory
include /etc/logrotate.d

# no packages own wtmp and btmp -- we'll rotate them here
/var/log/wtmp {
    monthly
    create 0664 root utmp
        minsize 1M
    rotate 1
}

/var/log/btmp {
    missingok
    monthly
    create 0600 root utmp
    rotate 1
}

# system-specific logs may be also be configured here.
```

Như trên ta có thể thấy mặc định log sẽ được rotate một tuần một lần, giữ lại 4 bản, sau khi rotate file cũ sẽ tạo ra một file log mới (empty), sửa dụng ngày tháng năm đặt vào sau tên file (rotated) để phân biệt các file và ghi lại dấu thời gian. Ví dụ:

```sh
[root@mdt-server31 images]# ls /var/log/
anaconda/           boot.log-20190531   cron-20190609       libvirt/            messages-20190526   secure-20190609     tuned/
audit/              btmp                dmesg               maillog             messages-20190602   spooler             wtmp
boot.log            btmp-20190601       dmesg.old           maillog-20190519    messages-20190609   spooler-20190519    yum.log
boot.log-20190201   chrony/             firewalld           maillog-20190526    rhsm/               spooler-20190526    yum.log-20190131
boot.log-20190413   cron                glusterfs/          maillog-20190602    secure              spooler-20190602
boot.log-20190417   cron-20190519       grubby              maillog-20190609    secure-20190519     spooler-20190609
boot.log-20190502   cron-20190526       grubby_prune_debug  messages            secure-20190526     swtpm/
boot.log-20190522   cron-20190602       lastlog             messages-20190519   secure-20190602     tallylog
```

Ví dụ một file cấu hình để định nghĩa cách thực hiện rotate cho từng file log:

```sh
[root@mdt-server31 images]# cat /etc/logrotate.d/
bootlog         iscsiuiolog     libvirtd.lxc    numad           wpa_supplicant
chrony          libvirtd        libvirtd.qemu   syslog          yum
[root@mdt-server31 images]# cat /etc/logrotate.d/libvirtd
/var/log/libvirt/libvirtd.log {
        weekly
        missingok
        rotate 4
        compress
        delaycompress
        copytruncate
        minsize 100k
}
``` 

Giải thích một số thông số cơ bản: 

* `/var/log/libvirt/libvirtd.log`: đường dẫn tới file log để áp dụng cấu hình
* `weekly`: rotate theo tuần
* `rotate 4`: Giữ tối đa 4 phiên bản của file log
* `compress`: thực hiện nén file log sau khi được rotate bằng gzip


## 2. Cách log file được rotate

### Chọn file để thực hiện rotate

Chọn một hoặc nhiều file bằng wildcards, nhiều đối tượng file sẽ cách nhau bởi một dấu cách (space)

```sh
/var/log/messages
/home/*/logs/mysql*.log
/home/*/logs/access.log /home/*/logs/error.log /home/*/logs/nginx_error.log /home/service_error.log
```

### Rotate theo thời gian

Có 4 giá trị cấu hình tương ứng với khoảng thời gian log file sẽ được rotate

* Daily: mỗi ngày
* Weekly: mỗi đầu tuần
* Monthly: mỗi đầu tháng
* Yearly: mỗi năm

### Rotate theo dung lượng file

```sh
size 100k
size 100M
size 100G
```

Nếu vượt quá kích thước file đã được cấu hình thì sẽ thực hiện rotate. Các đơn vị khả dụng: K, M, G.

Khi một file log được cấu hình rotate theo cả thời gian và kích thước file, thì cả hai điều kiện này đều cùng được áp dụng, nếu dung lượng file vượt quá ngưỡng khi chưa tới ngưỡng thời gian thì file sẽ thực hiện rotate và reset lại dấu thời gian.

### Tham số `missingok`

Để xử lý file log trống, Logrotate hỗ trợ một số các tham số để xử lý: `missingok`, `nomissingok`, `Notifempty`

* `missingok`: Khi file log trống thì vẫn thực hiện rotate mà không thông báo lỗi
* `nomissingok`: Khi file log trống thì vẫn thực hiện rotate nhưng sẽ thông báo lỗi
* `Notifempty`: Không rotate nếu file này rỗng.

### Giữ lại các file cũ:

Cấu hình số lượng tối đa các file log được giữ lại:

	rotate [number]

### Nén file

Mặc định, nếu không cấu hình gì thì sau khi rotate, file log sẽ không được nén lại. Nếu muốn nén các file log cũ lại với gzip thì sử dụng `compress`. Bạn không muốn sử dung gzip mà sử dụng bzip2, zx hoặc zip thì sử dụng `compresscmd xz`

Tham số `delaycompress` sẽ hữu dụng trong trường hợp bạn không muốn nén file log cũ ngay sau khi rotate, mà muốn thực hiện nén nó trong lần rotate tiếp theo. Chỉ được thực hiện khi tham số `compress` được kích hoạt.

Nếu không muốn nén file log cũ thì nó cũng có tùy chọn là `nocompress`

### Phân quyền cho log file mới

Nếu muốn bạn có thể chỉ permission, owner, group sở hữu cho file log mới được tạo ra sau khi rotate. Thực hiện như sau:

	create [permission] [owner] [group]

Ví dụ:

	create 660 appuser www-data

Nếu bạn không muốn tự động tạo file mới thì sử dụng tham số `nocreate`

Sử dụng `dateext` để thêm dấu thời gian khi thực hiện rotate làm hậu tố tên log file cũ.


## 3. Một số lưu ý khác

Để quản lý các log files của các ứng dụng bên ngoài của các dịch vụ hệ thống được cấu hình trước, đóng gói trước, chúng ta sẽ có hai options:

* Tạo mới một file cấu hình logrotate đặt trong thư mục `/etc/logrotate.d/`. Nó sẽ được chạy hàng ngày với quyền `root` user như các các standard logrotate jobs khác.

* Tạo một file cấu hình mới và chạy nó bên ngoài thư mục cấu hình mặc định của log rotate. Cách này chỉ thực sự cần thiết nếu bạn cần chạy logrotate với user không phải root, hoặc nếu muốn rotate log files thường xuyên hơn là hàng ngày (với tham số `hourly` được đặt trong thư mục `/etc/logrotate.d` không thực sự hiệu quả, bởi mặc định thì logrotate chỉ được thiết lập chạy một ngày một lần)




## Tham khảo thêm 

[1] https://hocvps.com/logrotate/#2._C%E1%BA%A5u_h%C3%ACnh_Logrotate

[2] https://www.digitalocean.com/community/tutorials/how-to-manage-logfiles-with-logrotate-on-ubuntu-16-04
