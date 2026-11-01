## Dùng khi
Menu các thao tác phụ của một danh sách hoặc màn hình, mở từ nút ba chấm (ví dụ "Thêm danh sách yêu thích", "Xoá hết mã"). Khác Dropdown dạng chọn một giá trị: Droplist là danh sách hành động, mỗi mục kèm icon, không tự xuống dòng.
## Class
| Class | Mô tả |
|---|---|
| `.arg-droplist` | Thêm vào `.arg-menu` (và `.arg-menu--end` để căn phải): rộng theo nội dung, tối thiểu 240px, tối đa bằng chiều rộng màn trừ hai lề |
| `__item` | Thêm vào `.arg-menu__item`: cao 44px (token `height-xl`), chữ Body 3 một dòng (`white-space: nowrap`), icon 20px |
| `.arg-menu__sep` | Đường kẻ ngăn nhóm (dùng lại của Dropdown); `.arg-menu__item--danger` cho hành động xoá |
## Hành vi (JS)
Dùng Dropdown: `[data-arg-dropdown]` bọc nút `button[aria-haspopup]` và menu; Enter, Space, bấm để mở; mũi tên lên xuống di chuyển; Esc hoặc bấm ngoài để đóng. Mục có `data-arg-open="id"` mở lớp phủ (Offcanvas, Modal) tương ứng.
Phụ thuộc: Dropdown, Icon.

Trong Listbar menu bám mép phải của cả thanh (`.arg-listbar` đặt `position: relative`, dropdown chứa Droplist đặt `static`) để không tràn ra ngoài màn hình.
