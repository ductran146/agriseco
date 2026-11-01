## Dùng khi
Chọn một giá trị mà mỗi lựa chọn cần mô tả (ví dụ loại lệnh LO, MP, ATO, ATC). Danh sách ngắn, không có mô tả thì dùng Select thường.
## Class
| Class | Mô tả |
|---|---|
| `.arg-selectsheet` | Thêm vào `.arg-control.arg-select`: ô chọn trông như Select (nhãn, giá trị, mũi tên). `<select>` thật nằm bên trong để giữ giá trị (không bấm trực tiếp) |
| `__hit` | Nút phủ kín ô: `data-arg-open="id bảng"`, `data-label` là nhãn đọc màn hình, `aria-haspopup="dialog"` |
| `.arg-offcanvas--bottom.arg-offcanvas--auto[data-arg-selectsheet]` | Bảng trượt từ dưới lên (Offcanvas); thân là `.arg-optlist[role="radiogroup"]` |
| `.arg-optrow` | Một lựa chọn (`role="radio"`, `aria-checked`, `data-value`): `__txt` gồm tên (Body 2 đậm) và mô tả (Body 4, màu phụ), `__tick` là dấu chọn tròn (nền gradient chính) chỉ hiện ở mục đang chọn |
## Hành vi (JS)
Mở bảng thì đánh dấu mục theo `select.value`. Chọn mục: gán giá trị cho `select`, bắn `change`, đóng bảng. Bấm nền mờ hoặc nút đóng để đóng không đổi.
Phụ thuộc: Select, Offcanvas, Modal.
