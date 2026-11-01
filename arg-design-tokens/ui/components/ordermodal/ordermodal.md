## Dùng khi
Luồng đặt lệnh trên màn Giao dịch: xác nhận lệnh trước khi gửi, rồi báo kết quả.
## Class
| Class | Mô tả |
|---|---|
| `.arg-ordermodal` | Thêm vào `.arg-modal--sm`: tiêu đề có đường kẻ dưới, chân không có đường kẻ trên |
| `__actions` | Chân hộp thoại: các nút chia đều chiều ngang; `--stack` xếp dọc (hộp báo thành công) |
| `__lead` | Câu hỏi xác nhận căn giữa phía trên danh sách thông tin (hộp huỷ một lệnh) |
| `--done` | Hộp báo thành công: nội dung căn giữa, icon `.arg-modal__icon--success.arg-modal__icon--lg`, nền hộp `.arg-overlay--blur` |
Hàng thông tin dùng Kv (`.arg-kv--lines`); nút dùng Button (`--buy` hoặc `--sell`, `--tertiary`, `--primary`).
## Hành vi (JS)
| Thuộc tính | Việc làm |
|---|---|
| `[data-arg-confirm]` trên overlay | Hộp xác nhận của màn. Bấm `[data-arg-order-cta]` trong form `[data-arg-order]` thì điền các ô `[data-ord="title|symbol|type|price|qty|value"]`, đổi nút `[data-ord="ok"]` thành Mua hoặc Bán (đổi màu theo chiều lệnh) rồi mở. Khối lượng hoặc giá bằng 0 thì không mở |
| `[data-arg-confirm-ok]` | Đóng hộp xác nhận, mở hộp `[data-arg-done]`, điền `[data-ord="done"]`; bắn `arg:order` ({ side, symbol, price, qty }) |
Phụ thuộc: Modal, Kv, Button, Side (form đặt lệnh).

Bấm xác nhận lệnh: thiết bị rung nhẹ 15ms nếu trình duyệt hỗ trợ `navigator.vibrate` (iOS Safari chưa hỗ trợ). Hộp thành công có hình chìm lá lúa.
