## Dùng khi
Một trang có nhiều màn hình nối nhau (danh sách, chi tiết) mà không tải lại trang.
## Class và thuộc tính
| Tên | Mô tả |
|---|---|
| `.arg-screen[data-arg-screen="id"]` | Một màn hình; màn không hiển thị có `hidden` |
| `[data-arg-go="id"]` | Phần tử bấm để mở màn `id` (thường là thẻ `a`) |
| `[data-arg-go][data-arg-root]` | Mục điều hướng gốc (thanh tab): mở màn `id`, xoá lịch sử quay lại, chuyển bằng hiệu ứng mờ |
| `[data-arg-back]` | Nút quay lại màn trước |
| `--in-fwd` `--in-back` `--in-fade` | Hiệu ứng trượt vào, tự gắn khi chuyển màn; tắt khi bật giảm chuyển động |
## JS
`screen.js`: giữ ngăn xếp màn đã đi qua, cuộn về đầu trang khi chuyển, bắn `arg:screen`.
