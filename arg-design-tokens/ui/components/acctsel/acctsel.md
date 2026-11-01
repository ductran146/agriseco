## Dùng khi
Đầu màn đặt lệnh hoặc tài sản, khi một người dùng có nhiều tiểu khoản.
## Class
| Class | Mô tả |
|---|---|
| `.arg-acctsel` | Nút khối, bấm để mở danh sách tài khoản |
| `__row` `__no` | Số tài khoản (Title 3 đậm, số đều chiều rộng) và mũi tên `caret-down` |
| `__type` | Loại tài khoản, chữ nhỏ màu phụ |
| `.arg-dropdown[data-arg-acct-menu]` | Kiểu menu trên thanh đầu: nút `.arg-acctsel` (có `aria-haspopup="menu"`; dòng trên `__no` là số tiểu khoản kèm mũi tên, dòng dưới `__type` là loại) là trigger của Dropdown. Bấm xổ danh sách toàn chiều ngang ngay dưới thanh đầu (thanh đầu phải là phần tử định vị như `.arg-appbar--sticky`): mỗi mục `.arg-menu__item[role="menuitemradio"]` cao tối thiểu 60px, hai dòng: `<b>` số tiểu khoản, `<span>` loại (chữ nhỏ màu phụ), có `data-no` và `data-type`, mục đang chọn nền xám. Khi danh sách mở, nội dung và thanh tab phía dưới phủ nền mờ như hộp thoại (`--arg-ui-background-bg-overlay`, nhoè 2px); bấm nền mờ để đóng. Chọn mục thì số và loại trên nút đổi theo, mũi tên lật lên khi mở, bắn `arg:acct` ({ no, type }) |
| `select[data-arg-acct]` | Chọn tiểu khoản bằng Select gốc (`.arg-control.arg-select.arg-control--sm.arg-acct-select` + `.arg-select-native`), đặt ở `__right` của tiêu đề khối. `value` mỗi `option` là id tiểu khoản, chữ ngắn gồm mã và loại (ví dụ `X1 · Thường`), `data-sub` là chữ dòng phụ của tiêu đề (số tài khoản đầy đủ) |
| `[data-arg-acct-pane="id"]` | Khối của một tiểu khoản; khi đổi lựa chọn, khối của tiểu khoản khác bị ẩn (`hidden`); `[data-arg-acct-sub]` đổi chữ theo `data-sub` |
## JS
Đổi lựa chọn hiện khối `data-arg-acct-pane` tương ứng trong cùng tabpanel; bắn `arg:acct` kèm `detail.id`.
