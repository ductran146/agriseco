## Dùng khi
Danh sách mã trong một chủ đề hoặc nhóm, cần xem giá nhanh và đánh dấu yêu thích.
## Class
| Class | Mô tả |
|---|---|
| `.arg-stockrow-list` | Danh sách thẻ (`ul`), cách nhau 8px |
| `.arg-stockrow` | Một hàng nền `--arg-ui-background-background`, bo `--arg-radius`, 4 cột: mã, giá, khối lượng, sao |
| `__id` | Liên kết: mã (`b`) và tên (`span`); vùng bấm phủ cả hàng |
| `__price` | Giá (`b`, màu `.arg-up` `.arg-down` `.arg-ref`) và `.arg-badge` phần trăm |
| `__vol` | Khối lượng (triệu CP) |
| `.arg-fav[data-arg-fav-toggle]` | Nút ngôi sao (xem Quote): bấm đổi `aria-pressed`, sao đặc màu vàng khi yêu thích |
Phụ thuộc: Quote (`.arg-fav`), Badge, Appbar (xử lý `data-arg-fav-toggle`).
