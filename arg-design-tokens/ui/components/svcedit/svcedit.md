## Dùng khi
Người dùng chọn các dịch vụ hay dùng và sắp xếp vị trí để hiện ở lưới Dịch vụ nhanh trên Trang chủ. Mở từ nút Tuỳ chỉnh.
## Class
| Class | Mô tả |
|---|---|
| `__grid` `__tile` | Lưới 3 cột các thẻ dịch vụ đã chọn (Service: icon gradient dịch vụ 48px và nhãn) trên nền xám nhạt, bo `--arg-radius`; `[data-arg-reorder="grid"]` cho kéo đổi vị trí; `.is-dragging` thẻ đang kéo phóng to 106%, nổi lên có bóng, các thẻ khác mờ còn 40% (`.is-sorting` trên lưới) |
| `__remove` | Nút bỏ ở góc trên phải thẻ: tròn 20px nền đỏ (token lỗi), icon trừ trắng, viền trắng |
| `__hint` | Dòng hướng dẫn và bộ đếm "Đã chọn n/6" |
| `__list` `__row` | Danh sách dịch vụ theo nhóm trong thẻ nền xám bo `--arg-radius-lg`, dòng cao 56px, đường kẻ nhạt (50% màu kẻ) bắt đầu từ chữ, không kéo qua icon |
| `__icon` `__name` | Icon gradient dịch vụ 32px (icon trắng 20px) và tên dịch vụ |
| `__add` | Nút thêm: icon `plus-circle` 24px màu thương hiệu; dịch vụ đã chọn không có nút; chuyển màu disable (`--arg-ui-text-on-bright-text-disable`, nhạt) khi đã đủ 6 dịch vụ |
## Hành vi (JS)
`[data-arg-svcedit]` trên màn, `data-arg-catalog` là JSON danh mục dịch vụ (id, nhãn, icon), `data-max` số dịch vụ tối đa. Bấm `[data-svc-remove]` bỏ, `[data-svc-add]` thêm vào cuối, kéo thẻ để đổi vị trí. `[data-svc-save]` lưu thứ tự vào sessionStorage (`arg-services`), đặt cờ `arg-services-saved` rồi quay lại; Trang chủ (Service) đọc lại và báo toast. Bắn `arg:services` ({ ids }).
Phụ thuộc: Service, Reorder (dạng lưới), Button, Action bar, Title, Appbar.
