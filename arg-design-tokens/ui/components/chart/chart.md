## Dùng khi
Hiển thị giá theo thời gian của chỉ số hoặc mã.
## Class
| Class | Mô tả |
|---|---|
| `.arg-chart` `--up` `--down` `--ref` | Khung biểu đồ; modifier đặt màu của biểu đồ đường (`--c`, `--g`). Thêm `.arg-chart--line` (bằng JS) để chuyển từ nến sang biểu đồ đường |
| `__candles` `__line` | Hai lớp trong `__price`: nến và đường kèm vùng gradient. Chế độ đường ẩn nến và khối lượng, đường kéo cao ra phủ cả phần khối lượng nên chiều cao vùng vẽ (212px) không đổi khi chuyển chế độ |
| `__dot` | Chấm trên đường tại điểm đang trỏ (chỉ ở chế độ đường) |
| `[data-arg-chart-mode]` | Nút đổi chế độ. Icon luôn là chế độ sẽ chuyển tới: biểu đồ nến thì hiện `wave-sine`, biểu đồ đường thì hiện `candlestick` |
| `[data-arg-chart]` `__plot` | Vùng vẽ, mang `data-candles` (mảng [mở, cao, thấp, đóng, khối lượng] đã chuẩn hoá 0..1), `data-base`, `data-date`. Gồm `__price` (nến SVG, cao 160px), `__vol` (khối lượng, cao 40px), `__tip` (tooltip), `__tag` (nhãn giá ở đường gióng ngang) |
| `data-span` `data-vol` `data-vol-unit` `data-start` `data-end` | Tuỳ chọn trên `__plot` cho tooltip: biên độ giá quanh `data-base` (mặc định 0,03, giá = base × (1 − span/2 + t × span)), hệ số và đơn vị khối lượng (274, tr), phút đầu và cuối của nến trong ngày (540 = 09:00, 885 = 14:45). Dùng để mã cổ phiếu hiện đúng giá, giờ và khối lượng trong phiên |
| `.cur` `--x` `--y` | Đường gióng dọc (bám nến gần nhất) và ngang (theo điểm chạm), nét đứt |
| `.up` `.down` | Nến và cột khối lượng tăng, giảm |
| `__range` | Hàng chọn khoảng thời gian (Chip tabs `--xs` cao 28px, nhãn viết tắt 1N, 1T, 1Th, 3Th, 1Nm, 5Nm) và nút đổi dạng biểu đồ, toàn màn hình (`.arg-icon-btn` 24×24px, icon 24×24px, cách nhau 12px) |

## JS
`chart.js`: tooltip, nhãn giá và đường gióng ẩn mặc định. Rê chuột thì hiện và bám theo con trỏ; trên cảm ứng chạm giữ khoảng 250ms rồi kéo mới hiện (vuốt nhanh vẫn cuộn trang), thả tay thì ẩn.
