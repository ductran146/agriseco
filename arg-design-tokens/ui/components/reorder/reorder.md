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

## Dạng lưới
`[data-arg-reorder="grid"]` (ul lưới nhiều cột): cả thẻ `li` là nút kéo, không cần `[data-arg-handle]`. Chuột: kéo khi đã di chuyển quá 4px; cảm ứng: giữ khoảng 250ms rồi kéo, vuốt nhanh vẫn cuộn trang. Thẻ đang kéo bám theo con trỏ, con trỏ vào thẻ nào thì thẻ đang kéo đổi chỗ tới vị trí thẻ đó. Nút, liên kết bên trong thẻ không bắt đầu kéo. Dùng ở Svcedit.
