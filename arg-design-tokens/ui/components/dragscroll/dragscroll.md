## Dùng khi
Mọi dải cuộn ngang trên máy tính cần kéo bằng chuột (không có thanh cuộn, không có trackpad). Tự áp dụng, không cần thêm class.
## Hành vi (JS)
`dragscroll.js` nghe chuột ở mức `document`: bấm trái trong một dải cuộn ngang được (`overflow-x: auto` hoặc `scroll`, nội dung dài hơn khung) rồi kéo thì dải cuộn theo.
| Chi tiết | Mô tả |
|---|---|
| Ngưỡng | Kéo quá 4px mới tính là kéo; bấm nhẹ vẫn chọn tab, mở liên kết |
| Sau khi kéo | Lần bấm kế tiếp bị nuốt để thả chuột không kích hoạt nút bên dưới |
| Scroll-snap | Tắt trong lúc kéo, trả lại khi thả |
| Bỏ qua | `input`, `textarea`, `select`, và phần tử có `data-arg-nodrag` |
| Cảm ứng | Không xử lý, vuốt tay đã có sẵn |
| Sự kiện | `arg:dragscroll` (`detail.left`) sau mỗi lần kéo |
## Class và thuộc tính
| Tên | Mô tả |
|---|---|
| `[data-arg-dragscroll]` | JS tự gắn khi rê chuột vào dải cuộn được: con trỏ `grab` |
| `.is-dragging` | Đang kéo: con trỏ `grabbing`, chặn chọn chữ |
