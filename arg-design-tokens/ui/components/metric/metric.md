## Dùng khi
Tóm tắt vài con số chính của tài khoản (giá trị cổ phiếu, lãi/lỗ, biến động hôm nay) cần nổi bật hơn lưới Statgrid. Đặt thẻ lãi/lỗ cạnh nhau, thẻ tổng giá trị ở trên (rộng).
## Class
| Class | Mô tả |
|---|---|
| `.arg-metric-row` | `dl` lưới 2 cột, cách nhau 12px |
| `--inline` | Trên `.arg-metric-row`: ba thẻ một hàng (3 cột, cách nhau 8px, đệm 12px, giá trị cỡ Title 3); dòng phụ giữ ngắn để không bị cắt |
| `.arg-metric` | Một thẻ: viền 1px, nền trắng, bo `--arg-radius`, 16px đệm |
| `--wide` | Chiếm cả hàng (thẻ tổng) |
| `--up` `--down` | Lãi (xanh) hoặc lỗ (đỏ): màu giá trị, viền màu trạng thái 30% và nền chuyển màu nhạt 12% từ trái sang trắng. Không có thì thẻ trung tính, viền xám |
| `.arg-metric__value` `.arg-metric__sub` | Giá trị lớn (Title 2 đậm) và dòng phụ chữ nhỏ (phần trăm, tỷ trọng); trong `dd` |
Màu dùng token giao dịch (tăng, giảm), không dùng màu thành công, lỗi.
