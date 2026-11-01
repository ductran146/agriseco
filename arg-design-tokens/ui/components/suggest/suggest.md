## Dùng khi
Danh mục theo dõi chưa có mã (hoặc vừa xoá hết): gợi ý vài cổ phiếu phổ biến để chọn nhanh, kèm lối thêm mã khác bằng bảng tìm kiếm.
## Class
| Class | Mô tả |
|---|---|
| `.arg-suggest` | Khối trống: `__head` (`__title`, `__text`), `__grid` 2 cột thẻ, `__actions` |
| `__card` `--up` `--down` `--ref` `--ceil` `--floor` | Thẻ chọn được (`label` có `input` checkbox): `__code` vòng tròn 40px chứa mã, `__tick` vòng chọn (đã chọn hiện dấu tích xanh), `__name` tối đa 2 dòng, `__price` giá màu theo trạng thái và Badge phần trăm |
| `__actions` | Nút văn bản "Thêm mã khác" bên trái, nút chính "Thêm vào danh mục (n)" bên phải; nút chính tắt khi chưa chọn thẻ nào |
| `.arg-suggest__sheet` | Offcanvas từ dưới (cao tối đa 560px): ô tìm và `__results` (mỗi `li[data-q]` có `__who` và nút Thêm; nút tắt, hiện "Đã thêm" khi mã đã có) |
## Hành vi (JS)
Vùng `[data-arg-watch]` chứa các khung `[data-arg-pane]` (xem Listbar), khối `[data-arg-suggest]`, các `<template data-arg-row="MÃ">` chứa dòng Quote mẫu, và bảng thêm mã.
- Khối gợi ý tự hiện khi danh sách đang chọn trống, ẩn khi có mã.
- Nút ngôi sao `.arg-fav` trong dòng Quote: bấm bỏ mã khỏi danh sách; hết mã thì khối gợi ý hiện lại.
- `[data-arg-watch-clear]` (nút xác nhận trong modal) xoá hết mã của danh sách đang chọn.
- Mã thêm mới nối cuối danh sách và giữ kiểu sắp xếp đang chọn.
## Phụ thuộc
Quote (`__fav`), Listbar, Offcanvas, Modal, Badge, Button, Input.

## Tạo danh sách mới
`#watch-new` (Offcanvas bottom) có ô `[data-arg-newlist-input]` (tự focus, bàn phím mô phỏng hiện lên) và nút `[data-arg-newlist-ok]` (tắt cho đến khi nhập tên). Bấm Xác nhận: thêm option vào select, dựng khung `[data-arg-pane]` từ `<template data-arg-pane-tpl>`, chọn danh sách mới (đang trống nên hiện khối gợi ý), đóng sheet và hiện toast thành công. Mở từ mục "Thêm danh sách yêu thích" của menu ba chấm.
Dòng trong danh sách yêu thích có nút kéo đổi thứ tự (xem Reorder).
