## Check_mk check SQL server 

Sử dụng Windows Server 2008

Đầu tiên tạo một file cấu hình `mssql.ini` cho check_mk ở đường dẫn của thư mục cấu hình, thường ở path "C:\Program Files(x86)\check_mk\config" (có thể không cần file này)

```sh
[auth]
type = db
username = monitoring
password = secret-pw
```
Copy file Plugin `mssql.vbs` trên check_mk host, trong thư mục plugin, hoặc lấy ở [đây](plugin/mssql.vbs), đặt vào "C:\Program Files(x86)\check_mk\config" của agent

Khởi động lại dịch vụ trên Agent

Do a service discovery adding unmonitored services

Activate Changes