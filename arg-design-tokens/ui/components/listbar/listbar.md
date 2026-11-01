## Dùng khi
Đầu một danh sách mã (bảng giá, danh mục theo dõi): chọn nhóm (sàn, danh mục) ở bên trái, các nút công cụ (sắp xếp, thêm, menu) ở bên phải.
## Class
| Class | Mô tả |
|---|---|
| `.arg-listbar` `[data-arg-listbar]` | Hàng ngang; đặt trong vùng `[data-arg-listbar-scope]` |
| `__main` | Bên trái: select 158px (`.arg-control.arg-select`), có thể thêm nút `__tool` (ví dụ menu ba chấm) |
| `__main` + `.arg-chip-tabs` | Kiểu chip: dải `.arg-chip-tab[data-arg-pane-tab="giá trị"]` thay select (danh mục người dùng tạo). Dải cuộn ngang, chip chọn tự cuộn vào giữa, khi còn chip khuất thì `__main[data-more]` làm mờ mép phải |
| `__tools` | Bên phải: các nút `__tool` vuông 40px, icon 24px |
## Hành vi (JS)
| Thuộc tính | Việc làm |
|---|---|
| `select[data-arg-pane-select]` | Đổi giá trị thì hiện khung `[data-arg-pane="giá trị"]` cùng vùng, ẩn khung khác |
| `button[data-arg-pane-tab]` | Bấm thì chọn chip (`aria-pressed`), hiện khung `[data-arg-pane="giá trị"]` cùng vùng |
| `[data-arg-sort]` trên dropdown | Mỗi mục menu có `data-sort` (`def` `code` `up` `down` `price` `vol` `pl` `loss` `val`); sắp xếp mọi `ul[data-arg-sortable]` trong vùng theo `data-code` `data-pct` `data-price` `data-vol` `data-pl` (lãi/lỗ) `data-val` (giá trị) của từng `li` |
Sắp xếp đang chọn được giữ khi có dòng thêm vào (sự kiện `arg:rows`).
## Phụ thuộc
Select, Chip tabs, Dropdown, Icon.
