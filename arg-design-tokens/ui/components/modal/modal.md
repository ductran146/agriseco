## Dùng khi
Xác nhận hoặc nhập liệu ngắn cần chặn thao tác phía sau.
## Class
| Class | Mô tả |
|---|---|
| `.arg-overlay[data-arg-modal]` | Nền mờ, thêm `hidden` ban đầu |
| `.arg-modal` (`--sm` `--lg`) | Hộp thoại 480px; 360, 720px |
| `__header` `__title` `__body` `__footer` | Các vùng |
| `__icon` (`--success` `--lg`) | Icon tròn cho hộp thoại cảnh báo; `--success` màu thành công, `--lg` cao 72px |
| `.arg-overlay--blur` | Nền nhoè mạnh hơn (12px), dùng khi hộp thoại báo kết quả |
| `[data-arg-open="id"]` | Nút mở |
| `[data-arg-close]` | Nút đóng |
## JS
`modal.js`: Esc và bấm nền để đóng, giữ focus trong hộp thoại, trả focus về nút mở, khoá cuộn nền. `ARG.openLayer(el)` và `ARG.closeLayer(el)`. Bắn `arg:open` và `arg:close`.

Mở lớp phủ bằng `ARG.openLayer` thì focus vào phần tử `[data-arg-autofocus]` nếu có (ví dụ ô nhập tên danh sách, bàn phím mô phỏng hiện luôn), không thì vào phần tử nhập đầu tiên. Nhấn xuống trong hộp rồi nhả ra ngoài hộp không đóng hộp.
