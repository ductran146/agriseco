## Dùng khi
Người dùng tự sắp xếp thứ tự các dòng trong một danh sách (ví dụ mã trong danh sách yêu thích).
## Class
| Class | Mô tả |
|---|---|
| `.arg-handle` | Nút kéo 20×28px đặt ở đầu dòng, icon `hamburger-menu` 20px, màu phụ; `aria-label` nêu mã và cách dùng bàn phím |
| `[data-arg-reorder]` | Gắn trên `ul`; mỗi `li` có `data-code` và chứa `[data-arg-handle]` |
| `.is-dragging` | Dòng đang kéo: nổi lên, nền surface, bóng mềm, bám theo con trỏ |
## Hành vi (JS)
Nhấn giữ nút kéo rồi kéo lên xuống (chuột hoặc cảm ứng); các dòng khác nhường chỗ ngay khi con trỏ qua giữa dòng. Bàn phím: nút kéo đang focus, mũi tên lên hoặc xuống đổi một bậc. Thả tay thì ghi thứ tự vào `li.dataset.i` (kiểu sắp xếp "Mặc định" của Listbar lấy thứ tự mới) và bắn `arg:reorder` ({ code, index }).
Dòng Quote `--fav` dùng nút kéo ở cột đầu; vùng bấm phủ cả dòng của `--link` nằm dưới nút (nút có `z-index: 1`).
