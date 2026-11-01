## Dùng khi
Màn có vài nhóm chức năng lớn (màn Thêm). Mobile: các nhóm nối nhau. Tablet (từ 720px): Side panel bên trái liệt kê tên nhóm, bấm nhóm nào thì bên phải hiện danh sách của nhóm đó.
## Class
| Class | Mô tả |
|---|---|
| `.arg-sidenav[data-arg-sidenav]` | Khung hai phần |
| `__nav` | Side panel (`.arg-sidepanel`) chứa các nút `.arg-sidepanel__item[data-sn-btn]`, ẩn ở mobile |
| `__body` | Vùng chứa các nhóm `[data-sn-group]` (mỗi nhóm một `.arg-page__block`); nhóm đang chọn có `data-sn-active` |
## JS
`sidenav.js`: bấm `[data-sn-btn]` đặt `aria-pressed` và chuyển `data-sn-active` sang nhóm cùng chỉ số. Bắn `arg:sidenav` (`detail.index`).
## Phụ thuộc
Side panel, Nav list, Title.
