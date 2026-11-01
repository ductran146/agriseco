## Dùng khi
Màn tìm mã chứng khoán mở từ biểu tượng kính lúp ở thanh đầu trang chủ và Thị trường: chưa gõ thì hiện danh sách tìm gần đây, gõ thì hiện mã khớp kèm ngôi sao theo dõi.
## Class
| Class | Mô tả |
|---|---|
| `.arg-search__bar` | Thanh đầu dính (Appbar): nút quay lại và ô tìm (Input có icon, nút xoá chữ chỉ hiện khi có chữ); đặt trên màn `.arg-screen--plain` nền trắng |
| `__recent` `__head` `__title` | Khối tìm gần đây: tiêu đề Title 3 và nút thùng rác xoá cả danh sách |
| `__list` `__row` | Danh sách và một dòng cao tối thiểu 44px (kết quả cao 68px, kẻ ngăn `--arg-ui-divider-separator`) |
| `__pick` | Dòng tìm gần đây: icon kính lúp và mã đậm; bấm điền mã vào ô. Nút `.arg-icon-btn` bên phải xoá dòng |
| `__results` | Kết quả: mỗi dòng dùng `.arg-quote__id` (mã đậm, tên công ty bên dưới) và ngôi sao `.arg-fav[data-arg-fav-toggle]` (đã theo dõi: sao vàng) |
| `__none` | Thông báo "Không tìm thấy mã phù hợp." hoặc "Chưa có tìm kiếm nào gần đây." |
## Hành vi (JS)
| Thuộc tính | Việc làm |
|---|---|
| `[data-arg-search]` | Gốc của màn; là `.arg-screen` thì mở màn tự đặt con trỏ vào ô, bàn phím mô phỏng trượt lên |
| `[data-arg-search-input]` | Lọc ngay khi gõ theo mã hoặc tên công ty (bỏ dấu, không phân biệt hoa thường); mã bắt đầu bằng chữ gõ xếp trước |
| `[data-arg-search-clear]` | Xoá chữ trong ô, quay về danh sách tìm gần đây |
| `[data-arg-search-pick]` `-remove` `-clear-all` | Điền mã vào ô, xoá một dòng, xoá cả danh sách tìm gần đây |
Bắn `arg:search` ({ q, count }). Tìm gần đây chỉ lưu trong màn đang mở (bản demo chưa ghi nhớ giữa các lần mở).
## Phụ thuộc
Appbar, Input, Quote (`__id`, `.arg-fav`), Button (`.arg-icon-btn`), Keyboard, Screen.
