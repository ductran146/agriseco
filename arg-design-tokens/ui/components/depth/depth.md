## Dùng khi
Trang thông tin mã: xem 3 mức giá mua bán tốt nhất cạnh nhau, dư mua bên trái, dư bán bên phải. Cạnh form đặt lệnh (cột hẹp) thì dùng Book; bấm "Xem đầy đủ" ở Book mở bảng bước giá nhiều mức (10 mức mỗi bên, kèm Sàn và Trần) trong bảng trượt từ dưới lên.
## Class
| Class | Mô tả |
|---|---|
| `.arg-depth` | Khung xếp dọc, chữ Body 4, số đều chiều rộng |
| `__head` `__side` `--bid` `--ask` | Hai ô tiêu đề: tên phía (đậm) và tổng khối lượng kèm tỷ lệ; nền 10% màu Mua hoặc Bán |
| `__ratio` | Thanh 4px chia tỷ lệ dư mua và dư bán theo `--v` (phần trăm dư mua) |
| `__row` | Một mức giá gồm hai nửa |
| `__half` `--bid` `--ask` | Nửa trái: khối lượng rồi giá; nửa phải: giá rồi khối lượng. Thanh nền 16% màu Mua hoặc Bán tỏa ra từ giữa, dài `--w`% (0 đến 100, so với khối lượng lớn nhất) |
| `__limits` `__limit` `--floor` `--ceil` | Hàng cuối bảng: Sàn (xanh ngọc, trái) và Trần (tím, phải), cao 36px, nền 10% của màu |
| `__price` `__vol` | Giá (đậm vừa, tô màu `.arg-up` `.arg-down` `.arg-ref` theo tham chiếu) và khối lượng |
