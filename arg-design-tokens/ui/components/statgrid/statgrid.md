## Dùng khi
Hiển thị 3 đến 12 chỉ số ngắn của một mã dạng lưới ô, ví dụ trần, tham chiếu, sàn, cao, thấp, hoặc giao dịch khối ngoại. Cần ít chỉ số trên một hàng thì dùng Stat row.
## Class
| Class | Mô tả |
|---|---|
| `.arg-statgrid` | Khung xếp dọc. Biến `--tile` là nền ô (mặc định nền xám của trang, hợp với khối trắng); trên nền xám đặt `--tile: var(--arg-ui-background-surface)` |
| `__grid` | Lưới `dl`, 3 cột (đổi bằng `--cols`), khoảng cách 8px |
| `__item` `dt` `dd` | Một ô bo `--arg-radius-sm`, đệm 8px 12px: nhãn Label 1 phụ, giá trị Body 4 đậm vừa, số đều chiều rộng. Tô màu `dd` bằng `.arg-up` `.arg-down` `.arg-ref` `.arg-ceil` `.arg-floor` |
| `.arg-collapse` | Phần chỉ số thêm, thu gọn được (xem Accordion & Collapse) |
| `__more` | Nút icon 48×24px ở giữa, cùng `.arg-collapse-toggle` và `data-arg-collapse`: mũi tên quay lên khi đang mở |
## JS
Không có file riêng. Thu gọn dùng `accordion.js` (`data-arg-collapse`, `aria-controls`, `aria-expanded`).
