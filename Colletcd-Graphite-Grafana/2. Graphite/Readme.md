#### Sử dụng script xóa db

Cài đặt python 3.6 trên CentOS 7

	sudo yum install python36
	sudo yum install python36-setuptools
	sudo easy_install-3.6 pip

Mặc định python 2,7 sẽ được cài đặt, và khi cài pip sẽ là pip của bản python 2.7, nên khi cài python 3.6 vào thì tôi sẽ đặt một cái alias ở `~/.bashrc` cho tiện sử dụng (có thể không cần tới bước này khi chưa cài pip nào khác):

```sh
$ vim ~/.bashrc
...
alias pip36='/usr/local/bin/pip3.6'
```

Sử dụng python3.6

	pip36 install keystoneauth
	pip36 install python-openstackclient

Test script với lệnh:

	python36 graphite_remove_db.py

Hoặc dùng shebang thì thêm quyền thực thi cho file

	chmod +x graphite_remove_db.py
	./graphite_remove_db.py

#### Tạo crontab chạy script 1 tuần 1 lần

Thêm dòng sau vào file `/etc/contab` để chạy scrpit mỗi tuần một lần vào lúc 8h05 ngày chủ nhật

	5 8 * * 0 root python36 /root/graphite_remove_db.py >> /var/log/graphite-web/deletedbgraphite.log 2>&1