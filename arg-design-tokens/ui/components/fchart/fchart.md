## Dùng khi
Biểu đồ chỉ tiêu tài chính theo quý hoặc năm: một chuỗi cột (ROE, lợi nhuận), hai chuỗi cột cạnh nhau (tổng tài sản và nợ), cột âm dương (lưu chuyển tiền), kèm đường phần trăm theo trục riêng (tăng trưởng so với cùng kỳ, nợ/tài sản).
## Class
| Class | Mô tả |
|---|---|
| `.arg-fchart` | Khung xếp dọc; `--n` là số kỳ |
| `__plot` | Vùng vẽ cao 160px: SVG `viewBox="0 0 100 100"` không giữ tỉ lệ; `.base` là đường 0 |
| `.s1` `.s2` | Cột chuỗi 1 (`--arg-viz-1`) và chuỗi 2 (`--arg-viz-2`) |
| `.pos` `.neg` | Cột dương, âm (màu tăng, giảm) |
| `.line` | Đường phần trăm (`--arg-viz-3`), nét không co giãn |
| `__dot` | Điểm trên đường, đặt bằng `left`, `top` theo % (HTML để không bị méo) |
| `__cols` `__col` `__period` | Nhãn mỗi kỳ dưới biểu đồ: kỳ, giá trị chuỗi 1, chuỗi 2 (`.s2`), phần trăm (`.arg-up` `.arg-down`); chữ Label 2 |
| `.up` `.down` `.ref` | Cột tô màu tăng, giảm, đứng theo từng cột |
| `--bins` | Nhiều cột hẹp (đến 11 khoảng): số trên, nhãn khoảng viết dọc (đọc từ dưới lên) dưới |
| `__legend` `__key` `--line` | Chú giải; `--c` đặt màu ô vuông |

Màu biểu đồ lấy từ `--arg-viz-1` đến `--arg-viz-6` (định nghĩa trong `base.css`, không phải token Figma vì P5_Chart đang để trống).
