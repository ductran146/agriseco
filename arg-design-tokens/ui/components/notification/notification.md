## Dùng khi
Toast cho phản hồi tức thời, danh sách cho thông báo trong ứng dụng.
## Class
| Class | Mô tả |
|---|---|
| `.arg-toasts` | Vùng chứa toast (JS tự tạo) |
| `.arg-toast` | Một toast |
| `.arg-notilist` > `.arg-noti` (`.is-unread`) | Danh sách thông báo |
## JS
- `ARG.toast({ type, title, text, duration })`, tối đa 4 toast, tự tắt sau 4 giây.
- `[data-arg-toast="success"]` mở toast mẫu.
- `[data-arg-mark-read="#id"]` đánh dấu đã đọc.
## Phụ thuộc
`button.css` (`.arg-icon-btn`), `icon.css`.
