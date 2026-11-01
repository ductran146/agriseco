## Dùng khi
Menu các thao tác phụ của một danh sách hoặc màn hình, mở từ nút ba chấm (ví dụ "Thêm danh sách yêu thích", "Xoá hết mã"). Khác Dropdown dạng chọn một giá trị: Droplist là danh sách hành động, mỗi mục kèm icon, không tự xuống dòng.
## Class
| Class | Mô tả |
|---|---|
| `.arg-droplist` | Thêm vào `.arg-menu`: mặc định căn cạnh trái của nút mở; thêm `.arg-menu--end` để căn cạnh phải của nút: rộng theo nội dung, tối thiểu 88px, bo `--arg-radius-sm`, tối đa bằng chiều rộng màn trừ hai lề |
| `__item` | Thêm vào `.arg-menu__item`: cao 28px, chữ Label 1 một dòng (`white-space: nowrap`), icon 16px bên trái; cùng cỡ với `.arg-menu--compact` của Dropdown |
| `.arg-menu__sep` | Đường kẻ ngăn nhóm (dùng lại của Dropdown); `.arg-menu__item--danger` cho hành động xoá |
## Hành vi (JS)
Dùng Dropdown: `[data-arg-dropdown]` bọc nút `button[aria-haspopup]` và menu; Enter, Space, bấm để mở; mũi tên lên xuống di chuyển; Esc hoặc bấm ngoài để đóng. Mục có `data-arg-open="id"` mở lớp phủ (Offcanvas, Modal) tương ứng.
Phụ thuộc: Dropdown, Icon.

Menu luôn căn theo đúng cạnh của nút mở (trái hoặc phải), không bám mép thanh chứa. Khi mở, nút ba chấm hiện trạng thái đang bấm (xem Listbar).
