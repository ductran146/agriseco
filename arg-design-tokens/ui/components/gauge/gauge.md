## Dùng khi
Tóm tắt tín hiệu phân tích kỹ thuật: số chỉ báo cho tín hiệu Bán, Trung lập, Mua và kết luận chung.
## Class
| Class | Mô tả |
|---|---|
| `.arg-gauge` | Khung căn giữa; `--v` từ 0 (Bán mạnh) đến 1 (Mua mạnh) đặt góc kim |
| `__dial` | SVG `viewBox="0 0 320 160"`, rộng tối đa 320px: 5 vùng `.zone` `.z1` đến `.z5` (Bán đậm, Bán nhạt 40%, xám, Mua nhạt, Mua đậm) và nhãn `text` |
| `__needle` | Kim xoay quanh tâm theo `--v`, chuyển động 0,4s (tắt khi giảm chuyển động) |
| `__verdict` | Kết luận chữ hoa: thêm `.arg-buy` hoặc `.arg-sell`; trung lập để màu chữ phụ |
| `__counts` | Ba số: Bán (`.arg-sell`), Trung lập, Mua (`.arg-buy`) dạng `dl` |

Màu Mua, Bán lấy từ token nút Mua, Bán, không dùng màu tăng giảm hay thành công, lỗi.
