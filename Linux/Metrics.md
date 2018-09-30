# Understanding Linux performance metrics

## Processor metrics

### CPU utilization

Đây có lẽ là metric đơn giản nhất. Nó miêu tả việc sử dụng trên một processor. Trên IBM System x architectures, nếu CPU sử dụng trên 80% trong một khoảng thời gian cố định nào đấy thì có thể xảy ra hiện tưởng thắt cổ chai

### User time

Mô tả phần trăm CPU dành cho tiến trình người dùng, bao gồm cả nice time. Giá trị này càng cao thì càng tốt.

### System time 

Mô tả phần trăm CPU dành cho hoạt động của kernel bao gồm IRQ và softirq time. Nếu system time quá cao thì có thể gây ra nhiều tắc nghẽn

### Waiting

Tổng thời gian tiêu tốn cho một hoạt động I/O xảy ra. Hệ thông cũng không nên dành quá nhiều thời gian cho việc này

### Idle time

Mô tả phần trăm CPU khi hệ thống không hoạt động khi chờ nhiệm vụ

### Nice time

Mô tả tỷ lệ phần trăm CPU dành cho các quy trình tái xử lý thay đổi thứ tự thực hiện và mức độ ưu tiên của các quy trình

### Load average

Load average không phải là phần trăm, nhưng nó là trung bình công của nhưng thông số sau: 
- Số lượng các quy trình trong hàng đợi đang chờ xử lý
- Số lượng các chương trình không thể ngắt được cho đến khi hoàn thành

Tức là trung bình cộng của các tiến trình TASK_RUNNING and TASK_UNINTERRUPTIBLE. Nếu processes request CPU time bị blocked (nghĩa là CPU không có thời gian để xử lý chúng) thì load average tăng 

Load average đại diện cho khoảng thời gian CPU bận. 

### Runable processes

Giá trị này miêu tả các tiến trình đã sẵn sàng để thực thi. Giá trị này mà vượt quá 10 lần sô lượng physical processors trong một khoảng thời gian nhất định sẽ gây ra hiện tượng tắc nghẽn

### Blocked

Processes không thể thực thi trong khi chúng đang đợi I/O operation kết thúc. Các quá trình bị chặn này có thể gây ra tình trạng thắt cổ chai

### Context switch

Là số các quá trình switches giữa các thread trong hệ thống.

### Interrupts

Giá trị này bao gồm cả hard Interrupts và soft Interrupts, hard Interrupts có nhiều ảnh hưởng xấu đến hiệu năng của hệ thống. Giá trị Interrupts cao cũng gây ra hiện tượng software bottleneck trong cả kernel lẫn driver. 

Các giá trị này bao gồm cả các Interrupts gây ra bởi CPU clock.


## Memory metrics

### Memory Usage

Khi một process yêu cầu hệ  thống cấp phát bộ nhớ và lúc này hệ thống đang hết memory vật lý, thì kernel sẽ `paging out` các memory blocks ít sử dụng để giải phóng một vài vùng nhớ, cho đến khi tiến trình được cấp phát đủ yêu cầu mà nó cần.

### Free memory

Là lượng memory rảnh rỗi khả dụng. kernel cấp phát bộ nhớ không sử dụng nhiều nhất là cache của file system, vì vậy trừ đi buffers và cache từ bộ nhớ đang được sử dụng để xác định free memory

### Swap usage

Giá trị này miêu tả swap space used. Values above 200 to 300 pages per second for a sustained period of time express a likely memory bottleneck.

### Buffer and cache

Cache allocated as file system and block device cache.

### Slabs

Depicts the kernel usage of memory. Note that kernel pages cannot be paged out to disk.

### Active versus inactive memory

Provides you with information about the active use of the system memory. Inactive memory is a likely candidate to be swapped out to disk by the kswapd daemon



Tham khảo thêm

http://www.monitis.com/blog/key-linux-performance-metrics/