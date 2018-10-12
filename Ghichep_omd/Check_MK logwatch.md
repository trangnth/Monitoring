# Check_mk Logwatch

Check log mỗi và báo lại mỗi lần log có từ `error`

Trên Linux Logfiles được giám sát bằng extension của check_mk_agent là `logwatch`.

Download `mk_lpgwatch` plugin về client từ server:

	$ scp <username>@<ip_server>:/opt/omd/versions/1.5.0p5.cre/share/check_mk/agents/plugins/mk_logwatch /usr/lib/check_mk_agent/plugins

Tạo một file config `/etc/check_mk/logwatch.cfg` trên agent với nội dung như sau:

```sh
/home/trangnth/serviceError.log maxlines=100 maxtime=10 overflow=W
 C [E,e]rror(.*)
 R There is error: \1
 W [W,w]anning*
 O accept*
```

*Lưu ý về định dạng của file.*

Giải thích sơ qua về file cấu hình trên:

* Dòng đầu tiên: F
	* File `/home/trangnth/serviceError.log`  đang được theo dõi
	* `maxlines` cấu hình về số lượng dòng log mới lớn nhất của file được chấp nhận check (còn lại sẽ bị drop) 
	* `maxtime`
	* `overflow`

* `C` Critical nếu bất cứ dong log nào thỏa mãn đoạn pattern phía sau
* Tương tự với `C` là `W`(Wanning), `O`(OK)
* Pattern: Ví dụ với pattern `[E,e]rror(.*)` sẽ bắt tất cả các dòng có từ error hoặc Error sẽ hiển thị trạng thái Critical
* `R` Rewrite: Hiển thị thông báo thay vì hiển thị dòng log là `There is error: ` cộng với *phần còn lại của log(phía sau từ error đầu tiên bắt được)*

Restart lại agent:

	service xinetd restart

Lên web của check_mk `Discovery` lại host

<img src="img/23.png">

Test thử xem plugin đã chạy đúng chưa:

	echo "Error" >> /home/trangnth/serviceError.log

<img src="img/24.png">


## Tham khảo

https://mathias-kettner.de/checkmk_logfiles.html