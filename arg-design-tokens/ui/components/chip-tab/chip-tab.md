## Dùng khi
Lọc hoặc chuyển nhanh giữa vài nhóm nội dung cùng cấp, ví dụ danh mục theo dõi, khoảng thời gian, loại tài khoản. Cần gạch chân hoặc nhiều tab thì dùng Tabs.
## Class
| Class | Mô tả |
|---|---|
| `.arg-chip-tabs[data-arg-tabs]` | Khung, dùng script của Tabs |
| `.arg-chip-tabs__list[role=tablist]` | Dải chip, cuộn ngang khi hết chỗ, ẩn thanh cuộn |
| `.arg-chip-tab[role=tab]` | Một chip cao 40px, bo tròn; `aria-selected="true"` là chip đang chọn |
| `--sm` | Chip cao 32px |
| `--xs` | Chip cao 28px, tối thiểu 28×28px, chữ viết tắt (ví dụ 1N, 1T, 1Th) |
| Chip hành động | Dùng `.arg-chip-tab` là nút thường (không `role=tab`, không có `data-arg-tabs`) để chọn nhanh một giá trị, ví dụ giá Sàn, TC, Trần hoặc khối lượng 25%, 50%. Kết hợp `--sm` và `--fill` cho hàng chip chia đều |
| `--wrap` | Xuống dòng thay vì cuộn ngang |
| `--fill` | Các chip chia đều chiều rộng |
| `.arg-tabpanel[role=tabpanel]` | Nội dung, cùng thứ tự với chip |
## JS
Không có file riêng. Dùng `tabs.js` (phím mũi tên, Home, End, bỏ qua chip `disabled`, bắn `arg:tab`).

Bo góc lấy theo tỷ lệ chiều cao × 0,325 như Button rồi làm tròn về giá trị có trong token bo góc: 40px → 13 → 12 (`rounded-lg`), 32px → 10,4 → 12 (`rounded-lg`), 28px → 9,1 → 8 (`radius-md`). Không bo tròn hết cỡ.
