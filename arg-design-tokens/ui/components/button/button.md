## Dùng khi
Hành động chính hoặc phụ trên một màn hình. Mỗi vùng chỉ một nút `--primary`. Mua và Bán dùng `--buy` và `--sell`, không dùng Primary.
## Class
| Class | Mô tả |
|---|---|
| `.arg-btn` | Nút gốc, cao 40px |
| `--sm` `--xl` `--xxl` | Cao 32, 44, 48px |
| `--primary` | Gradient header web Agriseco |
| `--secondary` `--tertiary` | Nền nhạt |
| `--outline` `--outline2` | Có viền |
| `--text` `--text-strong` `--link` | Không nền |
| `--buy` `--sell` | Màu tăng và giảm |
| `--icon` | Nút vuông chỉ có icon (bắt buộc `aria-label`) |
| `--block` | Rộng hết hàng |
| `.arg-btn-group` | Nhóm nút, dùng `aria-pressed` để đánh dấu mục chọn |
| `.arg-icon-btn` | Nút icon 24px nhỏ, dùng trong input, alert, toast |
## Trạng thái
Mặc định, hover (lớp phủ State-Layer), pressed, focus-visible (viền 2px), disabled (`disabled` hoặc `aria-disabled="true"`), đang xử lý (icon `i--spin`).
## JS
`button.js`: bấm nút trong `.arg-btn-group` chuyển `aria-pressed` và bắn `arg:change`. Chặn click trên `a.arg-btn[aria-disabled="true"]`.
## Phụ thuộc
`base.css`, `icon.css`.
