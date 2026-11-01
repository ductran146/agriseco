## Dùng khi
Một mục chưa có nội dung hoặc chưa làm (ví dụ mục Thêm trong bản demo), danh sách rỗng cần giải thích và hướng người dùng đi tiếp.
## Class
| Class | Mô tả |
|---|---|
| `.arg-empty` | Khung căn giữa theo cả hai chiều, cao tối thiểu 62% màn hình |
| `__art` | Hình minh hoạ SVG nội tuyến, rộng 200px (viền trống quanh hình được kéo bù bằng margin âm). Hình thư mục trống (`empty-folder.svg`) do chủ dự án cung cấp; id trong SVG là duy nhất, chỉ đặt một hình mỗi trang |
| `__title` | Tiêu đề, Title 2 đậm |
| `__text` | Giải thích ngắn, tối đa 300px, màu phụ |
Nút hành động (tuỳ chọn) dùng Button (`--primary --xl`).

## Hình minh hoạ là ngoại lệ của quy tắc icon
Hình empty state không thuộc bộ Solar (xem AGENT-RULES mục 4, ngoại lệ về hình minh hoạ). Khi nhúng SVG do chủ dự án cung cấp:
- Hiệu ứng nhoè của bản gốc (phần thư mục phía trước làm nhoè phần phía sau) giữ lại, nhưng không dùng `foreignObject` kèm `backdrop-filter`: lớp đó vẽ khối nhoè đè lên nội dung bên dưới khi hình bị thu nhỏ. Thay bằng bản sao của phần phía sau (quầng sáng và thân thư mục), làm nhoè bằng `feGaussianBlur` (độ lệch chuẩn 18) và cắt theo đúng hình thư mục phía trước (`clipPath`), đặt dưới lớp kính trắng trong suốt.
- Màu vàng và bóng đổ của bản gốc đổi sang token hệ thống: hai điểm dừng của gradient là `--arg-p-brand-header-start` và `--arg-p-brand-header-end` (đúng gradient nút chính), đặt bằng `style="stop-color: var(...)"`; phần trắng trong suốt giữ nguyên.
