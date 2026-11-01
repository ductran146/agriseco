## Dùng khi
Nhập giá hoặc khối lượng cần tăng giảm theo bước.
## Class
| Class | Mô tả |
|---|---|
| `.arg-control.arg-stepper[data-step][data-dec]` | Khung cao 40px; `data-step` là bước, `data-dec` là số chữ số thập phân |
| `.arg-control__label` | Nhãn bên trái ô (Giá, Khối lượng), chữ phụ đậm vừa; cũng dùng được cho select (`.arg-select--center` căn giữa giá trị) |
| `.arg-icon-btn[data-arg-step="-1\|1"]` | Nút trừ, cộng |
| `.arg-input` | Ô nhập số, căn giữa |
## Chip chọn nhanh
Trong `[data-arg-order]`: `[data-arg-set="91,80"]` đặt giá; `[data-arg-qty-pct="50"]` đặt khối lượng bằng phần trăm của `data-max-qty`, làm tròn xuống lô 100.
## JS
`stepper.js`: đọc số trong ô theo định dạng Việt Nam (dấu chấm ngăn nghìn, dấu phẩy thập phân), cộng hoặc trừ bước, không xuống dưới 0, ghi lại cùng định dạng. Bắn `arg:step`.

Trong form đặt lệnh (`.arg-order`) nhãn dùng chữ ngắn (Giá, KL, Loại) và cùng rộng 36px, nên nút trừ, ô nhập, nút cộng ở các dòng thẳng hàng.
