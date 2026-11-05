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

- Toast thành công dùng icon trắng (`.arg-toast--success`), tương phản tốt hơn vòng xanh lá trên nền tối.
- `.arg-toast--single` (gọi `ARG.toast({ text: '' })`): toast một dòng chỉ có tiêu đề, không xuống dòng; tiêu đề cần ngắn (khoảng dưới 30 chữ).

- Vị trí toast: có thanh tab dưới hoặc thanh nút dính đáy (Action bar) thì cách thanh đó 20px; không có thì cách vạch Home indicator 20px (`--arg-home-indicator` + 20px).
