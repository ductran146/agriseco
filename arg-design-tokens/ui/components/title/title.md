## Dùng khi
Đầu mỗi màn hình hoặc mỗi khối nội dung: tiêu đề, thông tin phụ và các thao tác nhanh bên phải. Cao tối thiểu 44px, đệm 8px 20px, khoảng cách 20px (theo Title Module trên Figma).
## Cấu trúc
`.arg-title` chứa `.arg-title__left` (trái, co giãn) và `.arg-title__right` (phải, giữ nguyên kích thước). Mọi phần tử con đều tuỳ chọn, chỉ thêm phần cần dùng.
## Class
| Class | Mô tả |
|---|---|
| `.arg-title` | Khung, cao tối thiểu 44px |
| `--lg` | Cao tối thiểu 48px |
| `--md` `--sm` | Cỡ chữ Title 3; cỡ Body 3 kèm cao 40px (mặc định Title 2 đậm 20/28) |
| `--stacked` | Tiêu đề trên, dòng phụ dưới |
| `--wrap` | Tiêu đề dài được xuống dòng (mặc định cắt bằng dấu ba chấm) |
| `--border` `--muted` `--brand` `--center` | Viền dưới, nền xám, nền gradient nút chính, căn giữa |
| `__back` `__icon` `__flag` | Nút quay lại, icon 24px, cờ 24×19px |
| `__text` `__label` `__sub` `__chip` | Tiêu đề, nhãn đậm 14px, chữ phụ 14px, chip |
| `__drop` | Icon chevron 20px cạnh tiêu đề để mở danh sách |
| `__action` `--underline` | Nút chữ bên phải, cao 32px |
| `__tool` | Nút icon 24px bên phải. Thu gọn cả khối: thêm `.arg-collapse-toggle`, `data-arg-collapse`, `aria-controls` trỏ tới `.arg-collapse` chứa nội dung khối, icon `caret-down` (đang mở thì xoay lên) |
| `__meta` | Chữ phụ bên phải |
