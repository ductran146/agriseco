## Dùng khi
Hiển thị độ sâu thị trường cạnh form đặt lệnh.
## Class
| Class | Mô tả |
|---|---|
| `.arg-book` | Khối không khung viền, rộng theo cột (khoảng 104px trên mobile) |
| `__limit` `--ceil` `--floor` | Dòng trần (tím) và sàn (xanh ngọc), nền 10% của màu |
| `__row` `--ask` `--bid` | Một mức giá: `__price` (màu `.arg-up` `.arg-down` `.arg-ref`) và `__vol`; thanh nền dài `--w` × 0,6% bề rộng dòng (`--w` từ 0 đến 100) |
| `--list` `__head` `__scroll` `__li` `__total` `__ratio` | Chế độ danh sách: tiêu đề Giá, KL; 6 mức bán (giá cao xuống) rồi 6 mức mua trong vùng cuộn nội bộ `__scroll` (cao 192px, ẩn thanh cuộn, mép trên dưới mờ, `data-arg-book-center` + `data-asks` để mở ra đã cuộn tới ranh giới bán, mua); `__total` "Tổng KL"; thanh tỷ lệ Mua (xanh, trái) Bán (đỏ, phải) dùng token nút Mua, Bán, kèm hai phần trăm (`__ratio` đặt `--v` là phần trăm mua) |
| `__more` | Nút "Xem đầy đủ" (ở màn đặt lệnh cách khối Sàn 16px) cao 32px dưới sổ lệnh (`button` hoặc liên kết); có `data-arg-open="id"` thì mở bảng bước giá đầy đủ (Offcanvas `--bottom`, bên trong là Depth) |
## JS
`book.js`: cuộn vùng danh sách tới ranh giới giữa mức bán và mức mua mỗi khi hiện ra.
