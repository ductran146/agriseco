## Dùng khi
Sửa một lệnh đang chờ khớp hoặc khớp một phần: mở từ nút Sửa lệnh ở màn Chi tiết lệnh. Chỉ lệnh LO sửa được; lệnh MP, ATO, ATC không sửa được.
## Class
| Class | Mô tả |
|---|---|
| `.arg-locked` | Điều khiển bị khoá (chiều lệnh Mua/Bán, Loại lệnh): mờ 60%, con trỏ cấm; nút bên trong có `disabled` |
| `.arg-ordermodify__hint` | Dòng gợi ý dưới ô nhập (Lite: "KL mua tối đa"), sát mép trái |
Màn dùng lại Symbol, Pricehead, Statrow, Book (Pro), Bid / Ask (Lite), Side, Stepper, Kv, Action bar, Order modal.
## Hành vi (JS)
| Thuộc tính | Việc làm |
|---|---|
| `[data-arg-modify]` trên màn | Bật hành vi; hai form `[data-arg-order]` (Lite, Pro) giữ giá và khối lượng đồng bộ |
| `data-om-price`, `data-om-qty` trên form | Giá trị lệnh gốc. Khác gốc thì nút `[data-om-submit]` mới bật |
| `[data-om-submit]` | Mở hộp xác nhận `[data-om-modal]` (điền `[data-ord]`) |
| `[data-om-ok]` | Đóng hộp xác nhận, mở hộp báo thành công `[data-om-done]`; bắn `arg:ordermodify` |
