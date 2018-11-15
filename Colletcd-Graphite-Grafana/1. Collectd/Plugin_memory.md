## Plugin memory

Cấu hình bỏ comment các dòng sau trong file `/etc/collectd/collectd.conf`:

```sh
LoadPlugin memory
<Plugin memory>
        ValuesAbsolute true
        ValuesPercentage false
</Plugin>
```

Cấu hình với các option như trên để lấy các giá trị chính xác nó lấy được, nếu muốn lấy theo dạng phần trăm thì cấu hình ngược lại như sau:

```sh
ValuesAbsolute false
ValuesPercentage true
```

Các thông số mà nó lấy được:

* **Used**: Lượng bộ nhớ đã được sử dụng: mem_used = mem_total - (mem_free + mem_buffered + mem_cached + mem_slab_total);
* **Buffered**: Lượng (theo KB) bộ nhớ tạm lưu trữ cho các khối lưu trữ thô.
* **Cached**: Lượng bộ nhớ RAM vật lý (theo KB), sử dụng để cache.
* **Free**: Lượng bộ nhớ RAM vật lý (theo KB) có sẵn mà không được hệ thống sử dụng.
* **Total**: Tổng lượng RAM có thể sử dụng (theo KB) đó là lượng RAM vật lý không tính lượng dữ trữ.
* **slab_recl**:	The part of Slab that can be reclaimed, such as caches.
* **slab_unrecl**: The part of Slab that cannot be reclaimed even when lacking memory

