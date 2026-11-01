## Dùng khi
Lãi/lỗ luỹ kế theo ngày trong một kỳ: phần trên đường 0 là lãi, phần dưới là lỗ.
## Class
| Class | Mô tả |
|---|---|
| `.arg-plchart` | Khung: vùng vẽ trên, trục ngày dưới (5 mốc) |
| `__plot` | Vùng vẽ cao 160px, mang `data-arg-plchart`, `data-points`, `data-dates`, `data-min`, `data-max` |
| SVG `.up` `.down` | Đường và vùng tô 16% cắt theo đường 0 (`clipPath`): trên màu tăng, dưới màu giảm; `.base` là đường 0 nét đứt |
| `__cur` `__dot` `__tip` | Đường gióng dọc, chấm trên đường và tooltip (ngày, lãi/lỗ luỹ kế) |
## Hành vi (JS)
Đường gióng, chấm, tooltip chỉ hiện khi rê chuột, hoặc chạm giữ khoảng 250ms rồi kéo; vuốt nhanh vẫn cuộn trang. Bắn `arg:plchart` ({ index }).
