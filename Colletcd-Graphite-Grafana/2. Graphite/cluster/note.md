## Một số các lệnh chạy và kiểm tra

Khởi động lại các dịch vụ:

	systemctl restart carbon-cache
	systemctl restart carbon-relay

Khởi động lại các Instance:

	carbon-cache --config=/etc/carbon/carbon.conf restart 
	carbon-cache --config=/etc/carbon/carbon.conf --instance=b status
	carbon-cache --config=/etc/carbon/carbon.conf --instance=b start
	carbon-cache --config=/etc/carbon/carbon.conf --instance=b stop

Hoặc xem thêm [ở đây](https://stackoverflow.com/questions/49435902/how-do-i-run-multiple-carbon-services-in-one-systemd-file) để có thể sử dụng lệnh sau: 

	systemctl start 'carbon-cache@1'

Debug:

	/usr/bin/carbon-cache --debug --instance=XX start