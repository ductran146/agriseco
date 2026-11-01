## Dùng khi
Màn sổ lệnh: xem các lệnh trong ngày, lọc theo trạng thái, chiều lệnh, mã; huỷ một hoặc nhiều lệnh còn hiệu lực.
## Class
| Class | Mô tả |
|---|---|
| `__search` | Ô tìm mã (Input có icon), tìm ngay khi gõ, bàn phím hiện nút tìm |
| `__chips` | Dải chip trạng thái (Chip tabs `--sm`): Tất cả, Chờ khớp, Khớp một phần, Đã khớp, Đã huỷ, mỗi chip kèm số lệnh |
| `__head` `__count` | Hàng đầu danh sách: "n lệnh" bên trái, công tắc Tất cả, Mua, Bán (Tabs `--pill`) bên phải |
| `__empty` | Dòng thông báo khi bộ lọc không có lệnh |
| `.arg-actionbar[data-ob-bar]` | Thanh huỷ lệnh ở chế độ chọn nhiều: ô "Chọn tất cả" và nút Huỷ lệnh (n); thay thanh tab dưới |
## Hành vi (JS)
| Thuộc tính | Việc làm |
|---|---|
| `[data-arg-orderbook]` | Vùng chứa (thường là màn hình) |
| `[data-ob-status]` `[data-ob-side]` `[data-ob-search]` | Chip trạng thái, nút chiều lệnh, ô tìm mã; lọc ngay, `[data-ob-count]` và `[data-ob-empty]` cập nhật; số lệnh trong `[data-ob-n]` của chip |
| `.arg-orderrow__main` | Liên kết `data-arg-go` mở màn chi tiết lệnh; ở chế độ chọn nhiều thì bấm là chọn lệnh (nếu còn huỷ được), không chuyển màn |
| `[data-ob-select]` | Nút chữ (Button `--text`) đặt ở bên phải thanh đầu (navigation): bật hoặc tắt chế độ chọn nhiều (`data-select` trên vùng chứa), chữ đổi Chọn và Xong. Nhấn giữ khoảng nửa giây trên một lệnh còn huỷ được cũng bật chế độ này và chọn sẵn lệnh đó |
| `[data-ob-all]` `[data-ob-cancel]` `[data-ob-ok]` | Chọn tất cả lệnh đang hiện còn huỷ được; huỷ các lệnh đã chọn; xác nhận trong hộp thoại `[data-ob-modal]`. Lệnh chuyển sang Đã huỷ, bắn `arg:ordercancel` |
Chỉ lệnh Chờ khớp và Khớp một phần (`data-cancelable`) chọn được và huỷ được. Phụ thuộc: Order row, Chip tabs, Tabs, Input, Checkbox, Action bar, Modal, Badge.
