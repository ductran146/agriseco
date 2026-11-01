## Dùng khi
Một lệnh trong sổ lệnh: xem nhanh chiều lệnh, mã, giá và khối lượng đặt, trạng thái và tiến độ khớp; bấm cả thẻ để mở màn chi tiết lệnh (Order detail).
## Class
| Class | Mô tả |
|---|---|
| `.arg-orderrow-list` | Danh sách (`ul`), các thẻ cách nhau 8px |
| `.arg-orderrow` | Một thẻ có viền màu Mua (xanh) hoặc Bán (đỏ) 22% và nền chuyển màu rất nhạt (5%) từ trái sang trắng, cắt theo bo góc, bo `--arg-radius`. Thuộc tính `data-side="buy"` hoặc `"sell"`, `data-status` (`pending` `partial` `matched` `cancelled`), `data-cancelable` (còn huỷ được) |
| `__pick` | Ô chọn (`label.arg-check`), chỉ hiện khi vùng cha có `data-select` và lệnh có `data-cancelable` |
| `__main` | Liên kết bấm cả thẻ (đệm 12px, khoảng cách hai dòng 8px) (`a[data-arg-go]` tới màn chi tiết): dòng 1 `__side` (M hoặc B), `__id` (mã đậm, giờ và loại lệnh nhỏ), `.arg-badge` trạng thái; dòng 2 `__px` (giá × khối lượng) và `__fill` (khớp x/y, khối lượng đã khớp x in đậm trong `<b>`); bên phải `__go` là nút tròn nhỏ 24px có mũi tên 12px `caret-right` báo là bấm được |
| `__bar` | Thanh tiến độ khớp 3px, nằm sát đáy thẻ, `--v` là phần trăm khớp (0 đến 100), màu theo chiều lệnh |
Màu trạng thái dùng Badge: Chờ khớp `--yellow`, Khớp một phần `--blue`, Đã khớp `--success`, Đã huỷ mặc định (xám).
Hành vi nằm ở component Order book.
