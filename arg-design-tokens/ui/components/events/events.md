## Dùng khi
Lịch sự kiện của một mã (trả cổ tức, phát hành, đại hội cổ đông, công bố kết quả) có lọc theo khoảng ngày.
## Class
| Class | Mô tả |
|---|---|
| `.arg-events[data-arg-events]` | Khung; `data-week-start`, `data-week-end` (YYYY-MM-DD) để đếm sự kiện trong tuần |
| `__range` | Hai ô ngày cạnh nhau. Mỗi ô là Datepicker (`input[data-arg-datepicker][data-arg-events-from]` hoặc `-to`, giá trị chuẩn ở `data-iso`) |
| `[data-arg-events-count]` | Ô số đếm (`all`, `dividend`, `week`), thường đặt trong Stat grid `--cols: 2` |
| `.arg-accordion-list` > `.arg-accordion[data-date][data-type]` | Mỗi sự kiện là một thẻ đóng mở (xem Accordion); nội dung là Key-value `--lines` |
| `__empty` `[data-arg-events-empty]` | Dòng báo không có sự kiện trong khoảng ngày |
## JS
`events.js`: đọc `data-iso` của hai ô; đổi ngày thì ẩn thẻ ngoài khoảng, cập nhật các số đếm, bắn `arg:filter` (`detail.shown`).
