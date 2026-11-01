## Dùng khi
Mọi icon trong giao diện. Chỉ dùng bộ Solar (kiểu Linear, nét 1,5), không trộn bộ khác.
## Class
| Class | Mô tả |
|---|---|
| `.i` | Icon mặc định, 1em, nét 2, màu `currentColor` |
| `.i--16` `.i--20` `.i--24` | Kích thước cố định |
| `.i--spin` | Quay liên tục (loader) |
## JS
- `<i data-arg-icon="check"></i>` được thay bằng SVG khi `ARG.init`.
- `ARG.icon('check', 'i--16')` trả về chuỗi SVG để chèn từ JS.
- `ARG.iconNames()` liệt kê icon có trong sprite.
## Phụ thuộc
`icon.js` chứa sprite Solar do `build.py` ghi vào (mỗi icon giữ `viewBox` riêng). Thêm icon: bỏ file SVG vào `ui/icons/` rồi build lại.
