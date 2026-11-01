## Dùng khi
Màn chi tiết một lệnh trong sổ lệnh: bấm một thẻ lệnh (Order row) để vào.
## Class
| Class | Mô tả |
|---|---|
| `__head` | Đầu màn, đặt `data-side="buy"` hoặc `"sell"` (màu Mua, Bán): hàng `__row` gồm `__side` ("Lệnh mua" hoặc "Lệnh bán", Title 2) và Badge trạng thái, dưới là `__code` (mã, Title 1 đậm) |
| `.arg-kv--lines` | Danh sách thông tin kẻ dòng (Kv): số hiệu lệnh, thời gian, loại lệnh, giá đặt, giá khớp trung bình, khối lượng đặt, khối lượng khớp, giá trị ước tính, phí giao dịch ước tính |
| `.arg-actionbar--fixed` | Chân màn: Huỷ lệnh (Button `--outline`, chỉ khi lệnh còn huỷ được) và Sửa lệnh (`--primary`, mở màn Giao dịch của mã, chọn sẵn chiều lệnh) |
## Hành vi (JS)
`[data-od-cancel]` mở hộp xác nhận `[data-od-modal]`; `[data-od-ok]` xác nhận: nhãn `[data-od-badge]` thành Đã huỷ và nút huỷ ẩn. Bắn `arg:ordercancel`.
Phụ thuộc: Kv, Action bar, Badge, Button, Modal.
