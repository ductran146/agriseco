## Dùng khi
Diễn biến một giá trị có dấu trong phiên, ví dụ dòng tiền chủ động (mua chủ động trừ bán chủ động) lũy kế theo giờ.
## Class
| Class | Mô tả |
|---|---|
| `.arg-flow` | Khung xếp dọc |
| `__body` `__y` | Cột trục giá trị 40px (nhãn đặt theo `top` %) và vùng vẽ |
| `__plot` | SVG cao 160px `viewBox="0 0 100 100"` không giữ tỉ lệ: `.grid` lưới nét đứt, `.zero` đường 0, `.area-up` `.area-down` vùng tô 16%, `.line-up` `.line-down` đường xanh, đỏ (cắt theo mốc 0 bằng `clipPath`, id riêng cho từng biểu đồ) |
| `__x` | Nhãn giờ dưới biểu đồ, đặt theo `left` % (bỏ giờ nghỉ trưa) |
| `__legend` `__note` | Chú giải Dương / Âm và ghi chú (ví dụ dữ liệu đến 10:15) |
