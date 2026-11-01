## Dùng khi
Danh sách hỏi đáp hoặc mục dài cần thu gọn. Collapse dùng cho một vùng đóng mở riêng lẻ.
## Class
| Class | Mô tả |
|---|---|
| `.arg-accordion[data-arg-accordion]` | Khung, mỗi lần mở một mục |
| `.arg-accordion__btn` | Nút tiêu đề, cần `aria-expanded` và `aria-controls` |
| `.arg-collapse` (`.is-open`) | Vùng nội dung |
| `[data-arg-collapse]` | Nút mở collapse độc lập |
| `.arg-collapse-toggle` | Nút có icon xoay 180° khi mở (ví dụ nút mũi tên ở tiêu đề khối) |
| `.arg-collapse-more` `__open` `__close` | Nút chữ "Xem thêm" / "Thu gọn" cao 32px, tự đổi chữ theo `aria-expanded`, mũi tên xoay |
| `.arg-clamp` | Đoạn văn rút gọn còn `--lines` dòng (mặc định 4); nút `data-arg-collapse` trỏ tới nó để mở hết (`.is-open`) |
| `.arg-accordion-list` | Danh sách thẻ đóng mở độc lập: mỗi thẻ là một `.arg-accordion` một mục, nút `.arg-accordion__btn` có `data-arg-collapse` (mở nhiều thẻ cùng lúc) |
## JS
`accordion.js` đổi `aria-expanded` và lớp `.is-open`.
