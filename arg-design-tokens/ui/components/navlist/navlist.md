## Dùng khi
Liệt kê các mục chức năng dạng hàng (màn Thêm, cài đặt): mỗi hàng mở một màn hoặc một hành động.
## Class
| Class | Mô tả |
|---|---|
| `.arg-navlist` | Danh sách `ul`, không dấu đầu dòng; hàng cuối không có đường kẻ |
| `__item` | Hàng cao tối thiểu 56px (`a` hoặc `button`), đường kẻ dưới `--arg-ui-divider-separator`; chuyển màn bằng `data-arg-go` |
| `__icon` | Ô icon 40px bo `--arg-radius`, nền gradient nút chính, icon trắng 24px (duotone) giống ô Dịch vụ yêu thích |
| `__label` | Nhãn, Body 3 vừa |
| `__meta` | Ghi chú phụ bên phải (phiên bản, số lượng), Label 1 màu phụ |
| `__go` | Mũi tên `caret-right` |
| `--danger` | Mục nguy hiểm (đăng xuất), cố ý không nổi bật: chữ và icon 20px màu lỗi, không ô nền, không mũi tên, giống Đăng xuất của panel tablet |
Mục chưa có đích dùng `href="#"` (luôn `preventDefault`).
