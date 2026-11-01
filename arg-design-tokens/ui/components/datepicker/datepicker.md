## Dùng khi
Chọn một ngày (lọc theo khoảng ngày, ngày giao dịch, ngày hiệu lực). Thay cho ô `type="date"` gốc để hiển thị đúng định dạng dd/mm/yyyy của Việt Nam, đồng bộ giao diện giữa các thiết bị.
## Class
| Class | Mô tả |
|---|---|
| `.arg-control.arg-datepicker__field` | Khung ô nhập (cao 40px, xem Input) chứa `input.arg-input[data-arg-datepicker]` chỉ đọc và icon `calendar-blank` |
| `.arg-datepicker` | Bảng lịch (Offcanvas từ dưới), tạo một lần bằng JS cho cả trang: `__nav` (tháng trước, tiêu đề, tháng sau), `__wd` (T2 đến CN), `__grid` |
| `__day` `__month` | Ô ngày (tròn 40px) và ô tháng; `aria-pressed="true"` là ngày đang chọn (gradient nút chính), `aria-current="date"` là hôm nay (viền), `:disabled` là ngoài khoảng cho phép |
| `__foot` | Chân bảng: "Hôm nay" bên trái, "Huỷ" và "Chọn" bên phải |
## Thuộc tính
| Thuộc tính | Ý nghĩa |
|---|---|
| `data-arg-datepicker` | Bật bộ chọn ngày cho ô |
| `data-iso` | Giá trị chuẩn `yyyy-mm-dd` (ô hiển thị `dd/mm/yyyy`) |
| `data-min` `data-max` | Giới hạn ngày chọn được, đọc lại mỗi lần mở bảng |
| `data-arg-today` (trên `.arg-page`) | Ngày "Hôm nay" của dữ liệu mẫu; không có thì dùng ngày của máy |
## Hành vi (JS)
- Bấm ô hoặc icon (hoặc Enter, Space) để mở. Chọn ngày rồi bấm Chọn thì ghi vào ô, bắn `change` và `arg:date` (`detail.iso`). Huỷ, Esc, bấm nền thì không đổi.
- Bấm tiêu đề để chuyển sang chọn tháng, trong đó nút trước, sau đổi năm.
- Bàn phím: mũi tên đổi ngày (trái phải ±1, lên xuống ±7), PageUp, PageDown đổi tháng, Enter, Space chọn.
## Phụ thuộc
Offcanvas, Modal, Button, Input, Icon.
