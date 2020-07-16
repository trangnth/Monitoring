## Ghi chép qua trình tìm hiểu Colletcd + Graphite + Grafana

Những thứ cần tập trung tìm hiểu kỹ

### Collectd

Chủ yếu tìm hiểu về các plugin
* Tìm hiểu plugin unixsock
* Tìm hiểu plugin virt ===>>> giám sát máy ảo. Tìm hiểu các thông số mà nó lấy được gồm những gì mà đại diện cho những gì

Tìm hiểu command collectdctl => list ra các cái mà collectd thu thập được trước khi đẩy nó về graphite

### Graphite

Khái niệm

Cấu trúc, các thành phần

Tập trung vào cacbon trước, sau đó là whisper.

Đọc các functions để có thể vẽ được trên grafana

Cài collectd + graphite =>> giao diện web của graphite

### Bài toán tối ưu

Ví dụ: collectd mặc định đẩy 10s một lần, cấu hình cho nó đẩy 1 phút một lần

