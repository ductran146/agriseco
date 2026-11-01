## Dùng khi
Màn hai phần trên tablet (từ 720px): panel trái chứa danh mục (Thị trường) hoặc ô tìm kiếm và bộ lọc dạng danh sách (Sổ lệnh, Lịch sử lệnh), bên phải là nội dung. Mobile không dùng.
## Class
| Class | Mô tả |
|---|---|
| `.arg-sidepanel` | Khung panel: rộng `--arg-sidepanel-w` (240px, dùng chung mọi màn), nền xám của trang, cao tối thiểu bằng cả màn hình, lề trái bằng `--arg-gutter` |
| `__item` | Một mục dạng danh sách (cao 44px, chữ Body 3 đậm, nhãn trái, số hoặc mũi tên phải). Đang chọn (`aria-selected` hoặc `aria-pressed`) dùng đúng màu Chip tabs đang chọn: nền chữ nội dung đậm, chữ trắng |
| `__list` | Bọc nhóm các `__item` xếp dọc cách 2px |
## Dùng chung với
Tab (`.arg-tab`), Chip tab (`.arg-chip-tab`): thêm `__item` vào nút để đổi sang dạng danh sách.
