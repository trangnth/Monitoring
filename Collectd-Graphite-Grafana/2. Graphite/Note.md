## Note 

## Tìm đường dẫn 

Xem đường dẫn tới các thư mục, file cấu hình của graphite thì xem trong file cấu hình:

	/etc/graphite-web/local_settings.py


## Hàm Summarize

ví dụ khi sử dụng summarize(2min, sum) khi data đẩy về từ collectd 1 phút một lần thì hàm này sẽ thực hiện như sau:

<img src="img/3.png">

sum(0) = data (0) + data(1)
sum(2) = data (2) + data(3)

có nghĩa là lấy tổng các giá trị được đẩy về trong 2 phút *tiếp theo* (lấy giá trị đầu khoảng và bỏ giá trị cuối interval)

một hàm tương tự là `smartSummarize` nhưng khác ở chỗ lấy interval, với hàm `summarize` thì khoảng thời gian sẽ được lấy `chắn`, ví dụ interval là 10min thì các khoảng thời gian được lấy là 0h10min -> 0h20min, 0h20min -> 0h30min; còn `smartSummarize` thì khác, nếu hiện tại đang là 10h2min thì khoảng thời gian sẽ được tính từ thời điểm hiện tại trở về trước: 9h52min -> 10h2min.

Có thể thay thế sum bằng một số các hàm khác như: avg, last, max, min,

## Thực hiện query

r = requests.get('http://192.168.40.129/render?target=collectd.kvm31.088f1d13-9949-b03f-1aae-b979c7a1715d.virt-webvirt.if_octets-52_54_00_3d_2f_45.rx&from=-6h&until=now&format=json&maxDataPoints=683')


alias(collectd.kvm31.088f1d13-9949-b03f-1aae-b979c7a1715d.virt-webvirt.if_octets-52_54_00_3d_2f_45.tx%2C%20'Data%20Out')