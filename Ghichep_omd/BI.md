# Check_MK BI (Business Intelligence)

Xem giới thiệu BI ở đây https://mathias-kettner.de/checkmk_bi.html

Dưới đây tôi sẽ cho các bạn xem một ví dụ về BI

Đầu tiên ở giao diện `WATO` chọn `Business Intelligence` 

<img src="img/1.png">

Bạn sẽ nhìn thấy các BI Pack được cấu hình ở đây, mặc định sẽ có sẵn một Pack. Giờ chúng ta sẽ thử tạo một cái mới:

<img src="img/2.png">

Điền các thông tin cần thiết và nhấn `create` để tạo

<img src="img/4.png">

<img src="img/5.png">

Đừng active change vội nhé, chúng ta sẽ tiếp tục tạo các rule trong BI Pack này: 

<img src="img/6.png">

<img src="img/7.png">

<img src="img/8.png">

<img src="img/9.png">

Như hình dưới đây ta đã tạo được một rule

<img src="img/10.png">

Ta tiếp tục tạo thêm một vài rule nữa:

<img src="img/11.png">

<img src="img/12.png">

Tạo thêm một cái nữa:

<img src="img/13.png">

<img src="img/14.png">

<img src="img/15.png">

Tiếp theo ta sẽ định nghĩa một Aggregation

<img src="img/16.png">

<img src="img/17.png">

<img src="img/18.png">

<img src="img/19.png">

Giờ thì hãy active changes và đi xem kết quả thôi:

Vào `VIEWS` -> `Business Intelligence` -> `All Aggregation`, ta sẽ thấy Aggregation mà mình vừa tạo

<img src="img/20.png">


## Tham khảo

https://mathias-kettner.de/checkmk_bi_rules.html

https://truepath.zendesk.com/hc/en-us/articles/115005488806-Detailed-Reports-On-B-I-Aggregates-In-Check-MK

https://mathias-kettner.de/checkmk_bi_example.html