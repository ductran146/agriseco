## Dùng khi
Menu hành động, bộ lọc, chọn một giá trị khi `<select>` gốc không đủ.
## Class
| Class | Mô tả |
|---|---|
| `.arg-dropdown[data-arg-dropdown]` | Khung chứa nút mở và menu |
| `.arg-menu` (`--end` căn phải) | Menu, thêm `hidden` ban đầu |
| `.arg-menu--compact` | Menu thu gọn cho danh sách ngắn: rộng tối thiểu 88px, mục cao 28px, chữ Label 1 |
| `.arg-menu__item` (`--danger`) | Mục chọn |
| `.arg-menu__sep` `.arg-menu__label` | Đường kẻ và nhóm |
| `data-arg-select` | Mục có `aria-checked` đổi nhãn `[data-arg-label]` |
## JS
`dropdown.js`: click hoặc ArrowDown mở, ArrowUp/Down chuyển mục, Esc và click ngoài đóng. Chọn mục bắn `arg:select`.
## Phụ thuộc
`button.css`, `icon.css`.
