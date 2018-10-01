# Monitoring tools

## Command top

Cho thấy hoạt động thực tế của các tiến trình, mặc định nó sẽ hiển thị chủ yếu về CPU-intensive tasks đang chạy trên server và update nó mỗi 5s. Bạn có thể sắp xếp nó theo thứ tự của pid hoặc age, ...

```sh
top - 19:57:34 up 47 min,  2 users,  load average: 0.00, 0.01, 0.05
Tasks: 192 total,   1 running, 191 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.7 sy,  0.0 ni, 99.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :   283732 total,    14552 free,    77204 used,   191976 buff/cache
KiB Swap:  1046524 total,  1043444 free,     3080 used.   172428 avail Mem 

   PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND                    
     1 root      20   0   37828   5432   3900 S  0.0  1.9   0:02.20 systemd                    
     2 root      20   0       0      0      0 S  0.0  0.0   0:00.00 kthreadd                   
     3 root      20   0       0      0      0 S  0.0  0.0   0:00.05 ksoftirqd/0                
     5 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 kworker/0:0H               
     7 root      20   0       0      0      0 S  0.0  0.0   0:00.14 rcu_sched                  
     8 root      20   0       0      0      0 S  0.0  0.0   0:00.00 rcu_bh                     
     9 root      rt   0       0      0      0 S  0.0  0.0   0:00.00 migration/0                
    10 root      rt   0       0      0      0 S  0.0  0.0   0:00.01 watchdog/0                 
    11 root      20   0       0      0      0 S  0.0  0.0   0:00.00 kdevtmpfs                  
    12 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 netns                      
    13 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 perf                       
    14 root      20   0       0      0      0 S  0.0  0.0   0:00.00 khungtaskd                 
    15 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 writeback                  
    16 root      25   5       0      0      0 S  0.0  0.0   0:00.00 ksmd                       
    17 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 crypto                     
    18 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 kintegrityd                
    19 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 bioset                     
    20 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 kblockd                    
    21 root       0 -20       0      0      0 S  0.0  0.0   0:00.00 ata_sff 
```

**Dòng đầu tiên**: thể hiện thời gian máy uptime, số user đang đăng nhập, tải trung bình của hệ thống. Ba thông số của load average lần lượt chỉ khối lượng trung bình hệ thống phải xử lý trong khoảng thời gian 1p, 5p và 15p.

**Dòng 2**: thể hiện tổng số tiến trình, số tiến trình đang chạy, số tiến trình đang chờ, số tiến trình đã dừng, số tiến trình đang chờ dừng (zombie)

**Dòng 3**: Phần trăm CPU sử dụng cho người dùng (%us), Phần trăm CPU sử dụng cho hệ thống (%sy), Phần trăm CPU sử dụng cho tiến trình update (%ni), Phần trăm CPU không sử dụng (%id), Phần trăm CPU đợi các tiến trình I/O của hệ thống (wa%), Phần trăm CPU sử dụng giao tiếp với phần cứng (%hi), Phần trăm CPU sử dụng giao tiếp với phần mềm (%si)

**Dòng 4,5** thể hiện mức độ sử dụng RAM và swap

Bên dưới là bảng các tiến trình với các thông số:

* PID: ID của tiến trình
* USER: User sử dụng tiến trình đó
* PR: Mức đăng quyền của tiến trình
* NI: Giá trị tốt của tiến trình
* VIRT: Bộ nhớ ảo dùng cho tiến trình
* RES: Bộ nhớ vật lý dùng cho tiến trình
* SHARE Amount of memory shared with other processes, in kilobytes
* STAT State of the process: S=sleeping, R=running, T=stopped or traced, D=interruptible sleep, Z=zombie.
* %CPU: Phần trăm CPU sử dụng cho tiến trình
* %MEM: Phần trăm bộ nhớ sử dụng cho tiến trình
* TIME: Tổng thời gian hoạt động của tiến trình
* COMMAND: Tên của tiến trình


## vmstat

vmstat cung cấp thông tin về processes, memory, paging, block I/O, traps, and CPU activity.

```sh
root@trang-20-51:~# vmstat
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0   8520 174324 274476 1093084    0    0     5    15   79  169  0  0 99  1  0
```

Trong đó: 
* `Process` (procs):
	* r: Số lượng các process đang đợi runtime
	* b: Số lượng các tiến trình sleep không bị gián đoạn
* `Memory swpd`: The amount of virtual memory used (KB)
	* free: lượng memory nhàn rỗi (KB)
	* buff: lượng memory được sử dụng như buffers (KB)
	* cache: lượng memory được sử dụng như cache (KB)
* `Swap` 
	* si: Amount of memory swapped from the disk (KBps)
	* so: Amount of memory swapped to the disk (KBps)
* `IO`
	* bi: Blocks sent to a block device (blocks/s)
	* bo: Blocks received from a block device (blocks/s)
* `System`
	* in: The number of interrupts per second, including the clock
	* cs: The number of context switches per second
* `Cpu`
	* us: Time spent running non-kernel code (user time, including nice time).
	* sy: Time spent running kernel code (system time).
	* id: Time spent idle. Trước Linux 2.5.41, bao gồm cả I/O-wait time.
	* wa: Time spent waiting for IO. Trước Linux 2.5.41, this appeared as zero.

## uptime

The uptime command can be used to see how long the server has been running and how many users are logged on, as well as for a quick overview of the average load of the server

## ps and pstree

`ps` và `pstree` là một số command cơ bản để phân tích hệ thống. `ps` có 3 thể loại tùy chọn khác nhau, UNIX style, BSD style and GNU style. 

Một số tùy chọn với `ps`

* ps -ef – Liệt kê process đang chạy bây giờ. (Một command tương tự là ps aux)
* ps -f -u user1,user2 – Sẽ hiển thị tất cả process dựa rên UID (user id hoặc username).
* ps -f –pid ID – Hiển thị tất cả processes dựa trên process ID (pid). Điền PID hoặc PPID thay vào chỗ id. Có thể được dùng với PPID để lọc process dựa trên parent ID.
* ps -C command/name – Lọc Processes dựa trên tên của nó hoặc command
* ps aux –sort=-pcpu,+pmem – Hiển thị process đang dùng nhiều tài nguyên nhất của CPU.
* ps -e -o pid,uname,pcpu,pmem,comm – Được dùng để lọc column được chỉ định.
* ps -e -o pid,comm,etime – Việc này sẽ hiển thị thời gian đã được dùng của process.


|Thông số|Miêu tả|
|--|--|
|F | Process flag|
|S |State of the process: S=sleeping, R=running, T=stopped or traced, D=interruptable sleep, Z=zombie.|
|UID	|ID người sử dụng mà tiến trình này thuộc sở hữu (người chạy nó).|
|PID	|Process ID.|
|PPID	|Process ID gốc (ID của tiến trình mà bắt đầu nó).|
|LWP | LWP(light weight process, or thread) ID of the lwp being reported|
|C	|CPU sử dụng của tiến trình.|
|PRI| Priority of the process.|
|ADDR| Process Address space (not displayed)|
|SZ |Amount of memory (code+data+stack) used by the process in kilobytes.|
|PSR |Processor that process is currently assigned to.|
|STIME	|Thời gian bắt đầu tiến trình.|
|TTY	|Kiểu terminal liên kết với tiến trình.|
|TIME	|Thời gian CPU bị sử dụng bởi tiến trình.|
|CMD	|Lệnh mà bắt đầu tiến trình này.|


## Thread information
```
$ ps -LF
UID        PID  PPID   LWP  C NLWP    SZ   RSS PSR STIME TTY          TIME CMD
root      9688  9674  9688  0    1 13174  3980   1 17:34 pts/1    00:00:00 sudo -i
root      9689  9688  9689  0    1  5646  5188   0 17:34 pts/1    00:00:00 -bash
root      9750  9689  9750  0    1  9340  3236   1 17:39 pts/1    00:00:00 ps -LF
```

## free

Command hiển thị thông tin về tổng dung lượng của bộ nhớ trống và bộ nhớ đã được sử dụng (gồm swap) trên hệ thống. Nó cũng bao gồm  thông tin về buffers, cache được sử dụng bởi kernel.

Khi sử dụng `free`, hãy nhớ kiến ​​trúc bộ nhớ Linux và cách virtual memory manager hoạt động