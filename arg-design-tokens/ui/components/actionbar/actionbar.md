## Dùng khi
Màn chi tiết cần một hoặc hai hành động chính luôn trong tầm tay ở đáy màn, ví dụ Mua, Bán ở trang thông tin mã. Màn gốc có thanh tab dưới thì không dùng thêm thanh này.
## Class
| Class | Mô tả |
|---|---|
| `.arg-actionbar` | Hàng nút chia đều, khoảng cách 12px, đệm 12px và lề 20px; chừa vùng an toàn đáy; nền trắng mờ 85% làm nhoè nội dung cuộn qua, bóng như thanh tab |
| `--fixed` | Dính đáy màn khi cuộn |
| `.arg-btn` | Các nút bên trong (thường `--buy` `--sell` `--xl`), giãn hết ô |
## JS
Không có file riêng. Nút `data-arg-go="trade" data-arg-side="buy"` mở màn đặt lệnh và chọn sẵn chiều lệnh (xem Side toggle).
