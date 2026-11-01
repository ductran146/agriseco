## Dùng khi
Nhập một dòng chữ hoặc số. Luôn có `<label>` đi kèm.
## Class
| Class | Mô tả |
|---|---|
| `.arg-control` + `.arg-input` | Ô nhập, cao 40px |
| `.arg-control--sm` `--xl` `--xxl` | Cao 32, 44, 48px |
| `.arg-addon` `.arg-addon--end` | Tiền tố và hậu tố (đơn vị) |
| `.arg-textarea` trong `.arg-control--area` | Nhiều dòng |
| icon đặt trong `.arg-control` | Icon bên trái hoặc phải |
## Trạng thái
Mặc định, hover (viền đậm hơn), focus (viền Primary + vòng sáng), lỗi, thành công, chỉ đọc (`readonly`), vô hiệu (`disabled`).
## JS
`input.js`: nút `[data-arg-password]` trong `.arg-control` đổi giữa ẩn và hiện mật khẩu.
## Phụ thuộc
`field.css`, `button.css` (`.arg-icon-btn`), `icon.css`.
