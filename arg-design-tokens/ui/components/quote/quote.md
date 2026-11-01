## Dùng khi
Danh sách mã theo dõi hoặc bảng giá ngắn trên mobile.
## Class
| Class | Mô tả |
|---|---|
| `.arg-quote-list` | Thẻ nền trắng chứa các dòng |
| `.arg-quote` `--up` `--down` | Một dòng: `__id` (mã, tên), sparkline, `__price` (giá, phần trăm), `__vol` (khối lượng, ẩn khi hẹp dưới 380px) |
| `--rank` `__rank` | Bảng xếp hạng: cột số thứ tự 20px, mã và tên, giá và phần trăm; không sparkline, khối lượng |
| `__price--metric` | Cột phải là chỉ tiêu khác giá (khối lượng, mua bán ròng): chữ màu thường hoặc `.arg-up` `.arg-down` trên `b` |
| `.arg-quote-list--plain` | Danh sách phẳng trong khối trắng, không khung thẻ |
| `--link` | Dòng bấm được: `__id` là thẻ `a` (ví dụ `data-arg-go` mở trang thông tin mã), vùng bấm phủ cả dòng, viền focus quanh dòng |
| `--ceil` `--floor` | Trạng thái trần (tím) và sàn (xanh ngọc): giá `b` đổi màu; dùng cùng Badge `--ceil` `--floor` và Spark `--ceil` `--floor` |
| `--board` | Bảng giá: mã và tên, sparkline kèm đường tham chiếu nét đứt, giá và Badge phần trăm (rộng đều 64px); không hiện khối lượng |
| `--fav` `.arg-fav` | Thêm cột nút ngôi sao yêu thích cuối dòng. `.arg-fav[aria-pressed="true"]` sao đặc màu vàng, `__on` `__off` là hai icon. Bấm nút để bỏ mã (xem Suggest) |
| `.arg-quote-list--vol` | Xem khối lượng: ẩn sparkline, hiện cột khối lượng giữa mã và giá (bật bằng Fab) |
