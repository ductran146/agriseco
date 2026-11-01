## Dùng khi
Tiến độ có số liệu: khớp lệnh, hạn mức, tải lên.
## Class
| Class | Mô tả |
|---|---|
| `.arg-progress` (`--sm` `--lg`) | Thanh 8px; 4, 16px |
| `.arg-progress__bar` | Phần đã đầy, đặt `--v: 68%` |
| `--up` `--down` `--info` `--striped` | Màu giao dịch, thông tin, sọc động |
| `.arg-ring` | Vòng tiến độ SVG, đặt `--v: 72` |
Thêm `role="progressbar"` và `aria-valuenow` trên `.arg-progress`.
## JS
`ARG.setProgress(el, value)`. Nút `[data-arg-progress-step]` tăng giá trị.
