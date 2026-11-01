## Dùng khi
Cơ cấu một khoản gồm nhiều thành phần cộng lại: tiền, giá trị cổ phiếu, phí và thuế. Mỗi thành phần có chấm màu khớp đoạn của thanh chia.
## Class
| Class | Mô tả |
|---|---|
| `.arg-breakdown` | Thẻ nền `--arg-ui-background-background`, bo `--arg-radius`, đệm 16px, số đều chiều rộng |
| `__head` | Tên khoản bên trái, tổng bên phải (đậm) |
| `__bar` | Thanh 8px chia đoạn: mỗi `li` đặt `--w` (phần trăm) và `--c` (màu, dùng `--arg-viz-1` đến `--arg-viz-6`) |
| `__list` `__row` `__key` | Danh sách thành phần: chấm màu, nhãn, giá trị đậm vừa; nút mũi tên `.arg-icon-btn.arg-collapse-toggle` ở cuối dòng có thành phần con |
| `__sub` | Thành phần con (T1, T2, T3...) nằm trong `.arg-collapse`, chữ nhỏ, thụt vào bằng chấm màu |
## Hành vi
Mũi tên dùng `data-arg-collapse` của Accordion: bấm mở hoặc đóng, mũi tên xoay 180°.
## Phụ thuộc
Accordion (Collapse), Button (`.arg-icon-btn`).
