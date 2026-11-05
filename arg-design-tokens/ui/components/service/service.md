## Dùng khi
Danh sách lối tắt tới dịch vụ hay dùng trên trang chủ.
## Class
| Class | Mô tả |
|---|---|
| `.arg-service-grid` | Lưới 3 cột; thêm `--auto` để tự chia cột từ 720px |
| `.arg-service` | Ô dịch vụ là thẻ `<a>`, không nền và không bóng, chỉ có icon và nhãn |
| `__icon` `__label` | Icon trắng 24px trong ô bo 13px cao 48px nền gradient dịch vụ `--arg-gradient-service` (ngang, `#FF6A00` từ 50% sang `--arg-p-brand-header-end` ở 130%; định nghĩa trong `base.css`, không phải token Figma; ô 48 và 32 dùng chung), nhãn |

Icon dùng kiểu Solar Bold Duotone (đuôi `-duotone`), màu theo `currentColor`.

`.arg-service-grid--card`: lưới nằm trong thẻ nền trắng bo `--arg-radius-lg`; tiêu đề mục đặt ngoài thẻ.

## Hành vi (JS)
Lưới có `data-arg-catalog` (JSON danh mục dịch vụ) được dựng lại theo thứ tự đã lưu ở màn Tuỳ chỉnh dịch vụ nhanh (sessionStorage `arg-services`). Vừa lưu xong thì báo toast một dòng "Đã lưu dịch vụ nhanh".
