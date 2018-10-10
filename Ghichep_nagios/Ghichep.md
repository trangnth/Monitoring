# Ghi chép một số các khái niệm

## Host checks

### Khi nào Host checks được thực hiện

Hosts được check bởi Nagios daemon:

* Đều đặn mỗi một khoảng thời gian bằng với check_interval hoặc retry_interval
* Theo yêu cầu khi service liên kết với host thay đổi trạng thái
* Theo yêu cầu khi cần một phần của `host reachability` logic.
* Theo yêu cầu khi cần predictive host dependency checks.

Việc đặt lịch một host checks là không bắt buộc. Nếu bạn thiết lập `check_interval` bằng 0, thì Nagios sẽ không thực hiện checks theo định kỳ nữa. Nó vẫn sẽ thực hiện check nhưng chỉ khi được yêu cầu checks hosts khi cần thiết.

[see more...](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/hostchecks.html)

### Services checks 
Services được check bởi Nagios daemon:

* Đều đặn mỗi một khoảng thời gian bằng với check_interval hoặc retry_interval
* Theo yêu cầu khi cần `predictive service dependency checks`.

#### Service States
Services được check có thể là một trong bốn state sau:

* OK
* WARNING
* UNKNOWN
* CRITICAL

### Service State Determination

Service checks đưuọc thực hiện bởi các plugins, và có thể trả về một trong 4 trạng thái trên. Trạng thái của các plugin chính là trạng thái của các service. 

Khi Nagios check status của các services thấy thay đổi giữa các trạng thái thì nó sẽ thực hiện các hành động thích hợp

[see more](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/servicechecks.html)


## State Types

Việc giám sát trạng thái hoạt động của các service hay hosts được xác định bằng hai thành phần:

* Trạng thái của service hoặc host (Ok, Warning, Up, Down,...)
* Và LOẠI state cử service hoặc host

Có hai loại state trong Nagios là: SOFT và HARD states. Hai loại này chính là một phần quan trọng của monitoring logic. Vì chúng được sử dụng để xác định khi nào trình event handlers được thực thi và khi thông báo ban đầu được gửi đi. 

Nagios cho phép bạn xác định bao nhiêu lần một dịch vụ hoặc host cần được kiểm tra lại trước khi nó được coi là một `real` problem. Điều này sẽ được điều khiển bởi tùy chọn `max_check_attempts` trên host đó. 

### Soft States

Soft States xảy ra trong các tính huống sau:

* Khi một kết quả check service hoặc host có state là `non-OK` hoặc `non-UP` và việc check service chưa đủ số lần được định nghĩa trong `max_check_attempts`. Đây được coi là một soft error.
* Khi một service hoặc một host được phục hồi lại từ một soft error. Đây được coi là một soft recovery

### Hard States

Hard States xảy ra trong các tính huống sau:

* Khi kết quả check host hoặc service trả về là `non-OK` hoặc `non-UP` và đã thực hiện check đủ số lần được định nghĩa trong `max_check_attempts`thì đây gọi lại hard error state.
* Khi dịch vụ hoặc host chuyển từ trạng thái hard error này sang trạng thái error khác (ví dụ: wanning -> critical)
* Khi service check results có trạng thái là `non-OK` và tướng ứng với host là DOWN hoặc UNREACHABLE
* Khi host hoặc service recovers từ một hard error state. Đây gọi là hard recovery.
* Khi nhận được một passive host check. Passive host checks được coi là HARD trừ khi tùy chọn passive_host_checks_are_soft được bật.

Một số điều dưới đây sẽ xảy ra khi hosts hoặc services thay đổi HARD state: 

* The HARD state is logged.
* Event handlers được thực thi để xử lý HARD state.
* Contacts are notified of the host or service problem or recovery.

#### Ví dụ:

Dưới đây là ví dụ về cách xác định loại state, khi state thay đổi, và khi Event handlers và các thông báo được gửi đi. Bảng bên dưới hiển thị các lần kiểm tra liên tục dịch vụ theo thời gian. Service có giá trị max_check_attempts là 3.

|Time|	Check #	|State	|State Type|	State Change|	Notes|
|--|--|--|--|--|--|
|0|	1|	OK|	HARD|	No|	Initial |state of the service|
|1|	1|	CRITICAL|	SOFT|	Yes	|First detection of a non-OK state. Event handlers execute.|
|2|	2|	WARNING|	SOFT|	Yes	|Service continues to be in a non-OK state. Event handlers execute.|
|3|	3|	CRITICAL|	HARD|	Yes	|Max check attempts has been reached, so service goes into a HARD state. Event handlers execute and a problem notification is sent out. Check # is reset to 1 immediately after this happens.|
|4|	3|	WARNING|	HARD|	Yes|	Service changes to a HARD WARNING state. Event handlers execute and a problem notification is sent out.|
|5|	3|	WARNING|	HARD|	No|	Service stabilizes in a HARD problem state. Depending on what the notification interval for the service is, another notification might be sent out.|
|6|	1|	OK|	HARD|	Yes|	Service experiences a HARD recovery. Event handlers execute and a recovery notification is sent out.|
|7|	1|	OK|	HARD|	No	|Service is still OK.|
|8|	1|	UNKNOWN|	SOFT|	Yes|	Service is detected as changing to a SOFT non-OK state. Event handlers execute.|
|9|	2|	OK|	SOFT|	Yes|	Service experiences a SOFT recovery. Event handlers execute, but notification are not sent, as this wasn't a "real" problem. State type is set HARD and check # is reset to 1 immediately after this happens.|
|10| 1|	OK|	HRD|	No|	Service stabilizes in an OK state.|

## Detection and Handling of State Flapping

Nagios hỗ trợ việc phát hiện host và service đang `flapping`. Flapping xảy ra khi service hoặc host thay đổi trạng thái quá thường xuyên, dẫn đến một loạt các thông báo về sự cố và recovery. Flapping có thể là dấu hiệu của các vấn đề configuration (thresholds được thiết lập quá thấp), troublesome services, or real network problems.

### Cách Flap Detection hoạt động

Bất cứ khi nào Nagios kiểm tra trạng thái của một host hoặc service, nó sẽ check xem nó đã start hay stop flapping. Nó làm như sau:

* Lưu lại kết quả của 21 lần check
* Phân tích kết quả kiểm tra lịch sử và xác định nơi thay đổi trạng thái
* Sử dụng state transitions để xác định phần trăm thay đổi trạng thái (a measure of change) 
* So sánh phần trăm thay đổi trạng thái so với ngưỡng low và high của flapping. 

Một host hoặc service được xác định là `started` flapping khi phần trăm chuyển đổi trạng thái đầu tiên vượt high flapping threshold.

Một host hoặc service được xác định là `stopped` flapping khi phần trăm chuyển đổi trạng thái thấp hơn slow flapping threshold.

[see more...](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/flapping.html)


## Install nagios 

Cài đặt nagios trên centos7 theo link dưới đây: 

https://github.com/meditechopen/meditech-ghichep-nagios/blob/master/docs/thuchanh-nagios/1.Setup-CentOS-7.md

Khi cài đặt cần lưu ý: 

* Phải mở một số port (5666..) khi cài agent trên centos7
* Cài đặt bằng repo epel-release thêm option sau: `--enablerepo=epel`. Ví dụ:
		
		yum --enablerepo=epel -y install nrpe nagios-plugins-all



