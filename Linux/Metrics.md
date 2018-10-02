# Understanding Linux performance metrics

## Processor metrics

#### CPU utilization

Đây có lẽ là metric đơn giản nhất. Nó miêu tả việc sử dụng trên một processor. Trên IBM System x architectures, nếu CPU sử dụng trên 80% trong một khoảng thời gian cố định nào đấy thì có thể xảy ra hiện tưởng thắt cổ chai

#### User time

Mô tả phần trăm CPU dành cho tiến trình người dùng, bao gồm cả nice time. Giá trị này càng cao thì càng tốt.

#### System time 

Mô tả phần trăm CPU dành cho hoạt động của kernel bao gồm IRQ và softirq time. Nếu system time quá cao thì có thể gây ra nhiều tắc nghẽn

#### Waiting

Tổng thời gian tiêu tốn cho một hoạt động I/O xảy ra. Hệ thông cũng không nên dành quá nhiều thời gian cho việc này

#### Idle time

Mô tả phần trăm CPU khi hệ thống không hoạt động khi chờ nhiệm vụ

#### Nice time

Mô tả tỷ lệ phần trăm CPU dành cho các quy trình tái xử lý thay đổi thứ tự thực hiện và mức độ ưu tiên của các quy trình

#### Load average

Load average không phải là phần trăm, nhưng nó là trung bình công của nhưng thông số sau: 
- Số lượng các quy trình trong hàng đợi đang chờ xử lý
- Số lượng các chương trình không thể ngắt được cho đến khi hoàn thành

Tức là trung bình cộng của các tiến trình TASK_RUNNING and TASK_UNINTERRUPTIBLE. Nếu processes request CPU time bị blocked (nghĩa là CPU không có thời gian để xử lý chúng) thì load average tăng 

Load average đại diện cho khoảng thời gian CPU bận. 

#### Runable processes

Giá trị này miêu tả các tiến trình đã sẵn sàng để thực thi. Giá trị này mà vượt quá 10 lần sô lượng physical processors trong một khoảng thời gian nhất định sẽ gây ra hiện tượng tắc nghẽn

#### Blocked

Processes không thể thực thi trong khi chúng đang đợi I/O operation kết thúc. Các quá trình bị chặn này có thể gây ra tình trạng thắt cổ chai

#### Context switch

Là số các quá trình switches giữa các thread trong hệ thống. Có 2 loại:

* Voluntary context switch: Tiến trình tự nguyện nhường lại CPU sau khi chạy hết thời gian dự kiến của nó hoặc nó yêu cầu sử dụng tài nguyên hiện không khả dụng.
* Involuntary context switch: Tiến trình bị gián đoạn và nhường lại CPU trước khi hoàn tất thời gian chạy theo lịch trình của nó do hệ thống xác định một tiến trình ưu tiên cao hơn cần thực thi.

Để hiện thị context switch

	pidstat -w 10 1

Trong đó: 

* cswch/s: Tổng các context switches task tự nguyện trên giây. Một context switch tự nguyện xảy ra khi là một task blocks vì nó yêu cầu nguồn tài nguyên không khả dụng.

* nvcswch/s: Tổng các context switches task không tự nguyện trên giây. Một context switch không tự nguyện xảy ra khi một task thự thi trong suốt khoảng thời gian im lặng của nó và sau đó buộc phải từ bỏ bộ vi xử lý của nó.


#### Interrupts

Giá trị này bao gồm cả hard Interrupts và soft Interrupts, hard Interrupts có nhiều ảnh hưởng xấu đến hiệu năng của hệ thống. Giá trị Interrupts cao cũng gây ra hiện tượng software bottleneck trong cả kernel lẫn driver. 

Các giá trị này bao gồm cả các Interrupts gây ra bởi CPU clock.


## Memory metrics

#### Memory Usage

Khi một process yêu cầu hệ thống cấp phát bộ nhớ và lúc này hệ thống đang hết memory vật lý, thì kernel sẽ `paging out` các memory blocks ít sử dụng để giải phóng một vài vùng nhớ, cho đến khi tiến trình được cấp phát đủ yêu cầu mà nó cần.

#### Free memory

Là lượng memory rảnh rỗi khả dụng. kernel cấp phát bộ nhớ không sử dụng nhiều nhất là cache của file system, vì vậy trừ đi buffers và cache từ bộ nhớ đang được sử dụng để xác định free memory

#### Swap usage

Giá trị này miêu tả swap space used. Values above 200 to 300 pages per second for a sustained period of time express a likely memory bottleneck.

#### Buffer and cache

Cache được cấp phát như file system và block device cache.

#### Slabs

Miêu tả kernel sử dụng memory. Chú ý kernel pages không thể paged out tới disk.

#### Active versus inactive memory

Cung cấp cho bạn thông tin về hoạt động sử dụng bộ nhớ của hệ thống. 

Inactive memory is a likely candidate to be swapped out to disk by the kswapd daemon

## Network interface metrics

Dưới đây là một số các network interface metrics:

#### Packets received and sent

Số liệu này thông báo cho bạn về số lượng các package nhận được và được gửi bởi một network interface đã cho

#### Bytes received and sent

Giá trị này thể hiện số lượng bytes nhận và gửi từ một network interface đã cho.

#### Collisions per second

Thể hiện số lần va chạm (collisions) xảy ra trên mạng mà interface tường ứng đang kết nối. Các giá trị này cố định trong một thời gian dài là dấu hiệu của việc tắc nghẽn trên hạ tầng mạng chứ không phải là một trong server. 

Hầu hết trong hạ tầng mạng cấu hình đúng sẽ hiếm khi xảy ra va chạm, trừ khi trong hạ tầng gồm cả các hub.

#### Packets dropped

Là số lượng các packets đã bị kernel drop, hay do cấu hình firewall, hoặc cũng có thể do thiếu network buffers.

#### Overruns

Là số lần network interface hết không gian bộ nhớ đệm. Số liệu này nên được sử dụng kết hợp với giá trị packets dropped để xác định có thể xuất hiện một bottleneck trong network buffers hoặc the network queue length.

#### Errors

Số lượng Frame bị đánh dấu là lỗi. Điều này thường do mạng không khớp hoặc cáp mạng bị hỏng một phần. Một phần cáp mạng bị hỏng có thể là một vấn đề hiệu suất đáng kể đối với các mạng cùng dựa trên gigabit.


## Block device metrics

#### Iowait

Thời gian CPU dành cho I/O. Giá trị này cao và cố định có nhiều khả năng có hiện tượng I/O bottleneck.

#### Average queue length

Amount of outstanding I/O requests. In general, a disk queue of 2 to 3 is optimal; higher values might point toward a disk I/O bottleneck.

#### Average wait

Một phép đo thời gian trung bình tính bằng ms cần để phục vụ cho một yêu cầu I/O

#### Transfers per second

Là sô lượng hoạt động I/O thực thi trên giây (reads và writes). Transfers per second metric kết hợp với kBytes per second giúp bạn xác định kích thước trasfer trung bình của hệ thống. Kích thước trasfer trung bình này nhìn chung là phải phù hợp với stripe size được sử dụng bởi hệ thống disk của bạn.

#### Blocks read/write per second

Miêu tả việc đọc ghi dữ liệu trên một giây trong một blocks 1024 bytes như kernel 2.6. Các kernel trước đó có thể báo cáo với các kích thước block khác nhau, từ 512 byte đến 4 KB.

#### Kilobytes per second read/write

Đọc và ghi từ/tới block device tính bằng kilobyte thể hiện lượng dữ liệu thực tế được truyền đến và đi từ block device.


## Tham khảo thêm

http://www.monitis.com/blog/key-linux-performance-metrics/