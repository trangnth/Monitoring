## Một số các lệnh chạy và kiểm tra

Khởi động lại các dịch vụ:

	systemctl restart carbon-cache
	systemctl restart carbon-relay

Khởi động lại các Instance:

	carbon-cache --config=/etc/carbon/carbon.conf restart 
	carbon-cache --config=/etc/carbon/carbon.conf --instance=b status
	carbon-cache --config=/etc/carbon/carbon.conf --instance=b start
	carbon-cache --config=/etc/carbon/carbon.conf --instance=b stop