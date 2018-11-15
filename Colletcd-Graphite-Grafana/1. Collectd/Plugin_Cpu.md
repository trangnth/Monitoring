## Plugin CPU

Cấu hình file `/etc/collectd/collectd.conf` bỏ comment nhưng dòng như sau:

```sh
LoadPlugin cpu
<Plugin cpu>
        ReportByCpu true
        ReportByState true
        ValuesPercentage false
</Plugin>
```

Các tùy chọn cấu hình như sau:

* `ReportByState true|false`

	* Khi thiết lập true (mặc định), báo cáo metric theo trạng thái, ví dụ: "system", "user" và "idle"

	* Khi thiết lập false, kết tập (tính tổng) trên tất cả trạng thái non-idel vào một metric "active"

* `ReportByCpu true|false`

	* Khi thiết lập true (mặc định), metric được thu thập theo từng core CPU. Khi thiết lập false, thay vì báo cáo metric theo từng CPU, chỉ một tổng toàn cục của các trạng thái CPU được hiển thị.

* `ValuesPercentage false|true`

	* Tùy chọn này được sử dụng khi cả 2 thiết lập trên được đặt là true. Trong trường hợp này, mặc định các thông số sẽ được báo cáo theo jiffy. Thiết lập này set thành true, bạn cũng có thể yêu cầu các giá trị phần trăm ở chế độ chưa được tổng hợp (cho mỗi CPU, mỗi trạng thái).

* `ReportNumCpu false|true`

	* Khi thiết lập thành true, báo cáo số lượng CPU sẵn có. Mặc định là false.

* `ReportGuestState false|true`

	* Khi thiết lập thành true, báo cáo về trạng thái "guest" và "guest_nice" của CPU. Mặc định là false.

* `SubtractGuestState false|true`

	* Tùy chọn này chỉ được dùng khi tùy chọn ReportGuestState được thiết lập là true. "guest" và "guest_nice" tương ứng "user" và "nice". Nếu thiết lập true, "guest" sẽ loại bỏ "user" và "guest_nice" sẽ bỏ "nice". Mặc định là true.

Sau khi cấu hình, các thông số được thu thập gồm có:

* idle: Thời gian CPU ở trạng thái idle (rảnh rỗi, và sẵn sàng được sử dụng)

* nice: Thời gian CPU dùng để chạy các tiến trình người dùng được đánh dấu là niced. Mức ưu tiên một tiến trình user space có thể được tinh chỉnh bằng các điều chỉnh thông số nice.

* interrupt: Thời gian CPU dành để phục vụ các tiến trình ngắt.

* softirq	(apparently) : Time spent handling interrupts that are synthesized, and almost as important as Hardware interrupts (above). "In current kernels there are ten softirq vectors defined; two for tasklet processing, two for networking, two for the block layer, two for timers, and one each for the scheduler and read-copy-update processing. The kernel maintains a per-CPU bitmask indicating which softirqs need processing at any given time."

* steal: Là sự đo lường về phần thời gian mà trong trạng thái “involuntary wait.” Là khoảng thời gian mà kernel không thể đặt trong các trạng thái cơ bản như user, system, hay idle.

* system: Thời gian mà CPU dành để chạy trong kernel.

* user: Thời gian CPU dành để chạy các tiến trình user space mà không phải các tiến trình nice.

* wait: Thời gian CPU dành để chời một hoạt động I/O được hoàn thành.


### Tham khảo
