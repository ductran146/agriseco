## Dùng khi
Tab "Lịch sử lệnh" trong màn Sổ lệnh: xem lại các lệnh của những phiên trước (đã khớp, khớp một phần, đã huỷ, bị từ chối). Lệnh trong ngày và huỷ lệnh nằm ở tab "Sổ lệnh" (Order book).
## Class
| Class | Mô tả |
|---|---|
| `.arg-orderhist[data-arg-orderhist]` | Khối gốc. `data-today` là ngày "hôm nay" của dữ liệu mẫu, `data-period` là khoảng thời gian đang chọn |
| `__bar` | Hàng công cụ duy nhất: Select chọn khoảng thời gian bên trái (`.arg-control.arg-select` gốc, chữ trung tính, rộng 158px như Listbar; `[data-oh-period-select]` giá trị 7, 30, 90, custom; mặc định 30 ngày), nút Bộ lọc bên phải (`.arg-btn--outline2`, chữ trung tính); cao 40px |
| `__filter` | Nút Bộ lọc mở bảng Bộ lọc (`data-arg-open="oh-filter"`). Có bộ lọc đang bật thì viền màu link, kèm `.arg-count` ghi số bộ lọc (`.is-active`) |
| `__range` | Hai ô ngày (Datepicker, "Từ ngày" và "Đến ngày") chỉ hiện khi chọn Tuỳ chọn |
| `__sum` | Thẻ tổng kết dùng Statrow: Mua khớp, Bán khớp (giá trị khớp, đồng), tính lại theo khoảng thời gian và bộ lọc |
| `__list` `__day` `__date` | Danh sách chia theo ngày: tiêu đề ngày kèm số lệnh, mỗi ngày một `.arg-orderrow-list` |
| `.arg-orderrow` | Mỗi lệnh dùng lại Order row (không ô chọn, không thanh tiến độ); lệnh bị từ chối thay số khớp bằng lý do ngắn. Cần `data-date`, `data-side`, `data-status`, `data-matched`, `data-value` |
| `__opts` `__grp` `__radios` `__opt` `__foot` | Bảng Bộ lọc (Offcanvas `--bottom --auto`): hai nhóm Trạng thái (`[data-oh-status]`: all, matched, partial, cancelled, rejected) và Chiều lệnh (`[data-oh-side]`: all, buy, sell). Mỗi nhóm có nhãn đậm (Body 3, `__grp > .arg-label`), các nhóm cách nhau bằng đường kẻ; nhóm là `radiogroup` gồm các Checkbox kiểu radio (`label.arg-check` + `input[type=radio]`) xếp hai cột, không hiện số đếm. Chân bảng có Đặt lại (`[data-oh-reset]`) và nút chính "Xem n lệnh" (`[data-oh-apply]`), là nơi duy nhất ghi số lệnh kết quả |
## JS
`orderhist.js`: lọc theo khoảng thời gian, trạng thái, chiều lệnh (chọn xong lọc ngay, bảng Bộ lọc không cần bấm Áp dụng); cập nhật số lệnh theo từng trạng thái, tổng kết, số lệnh mỗi ngày, số bộ lọc đang bật; ẩn ngày không còn lệnh; hiện `[data-oh-empty]` khi không có lệnh. Bắn `arg:orderhist` (`detail.count`). Bấm một lệnh mở màn chi tiết lệnh (lệnh đã kết thúc: không huỷ, không sửa).
## Phụ thuộc
Order row, Select, Offcanvas, Checkbox (radio), Statrow, Datepicker, Badge.
