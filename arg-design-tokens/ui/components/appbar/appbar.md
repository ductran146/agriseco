## Dùng khi
Đầu trang chủ ứng dụng: chỉ số thị trường chính, tìm kiếm.
## Class
| Class | Mô tả |
|---|---|
| `.arg-appbar` | Thanh đầu, cao tối thiểu 56px |
| `--sticky` | Dính đầu khung cuộn, nền 85% mờ và làm nhoè nội dung cuộn bên dưới. Đặt ngoài vùng có padding, đặt `--arg-safe-top` (ví dụ 44px) để chừa chỗ status bar |
| `__logo` | Thay `__title` bằng logo Agriseco (SVG nội tuyến, cao 36px) trên trang chủ. Thẻ `h1` mang `aria-label="Agriseco"` |
| `__title` | Tiêu đề trang, Title 2 đậm 20/28, bên trái |
| `__info` `__name` `__quote` | Kiểu thay tiêu đề bằng tên chỉ số và dòng giá (dùng `.arg-up` `.arg-down` `.arg-ref`) |
| `__tool` đầu tiên | Nút quay lại (icon `caret-left`, `data-arg-back`), lùi 8px để icon thẳng lề; tiêu đề đứng ngay sau |
| `--condense[data-arg-condense]` + `__stack` | Khi cuộn, tiêu đề (`__title`) chuyển sang dòng thông tin thị trường (`__info`: tên, giá, thay đổi). Giá trị `data-arg-condense` là selector của khối giá lớn trong cùng màn hình; chuyển cảnh bám theo tốc độ cuộn: biến `--p` (0 đến 1) trên thanh là mức khối đó đã khuất dưới thanh trên đoạn 48px cuối (đổi bằng `data-arg-condense-range`). Tiêu đề mờ và trượt lên, thông tin thị trường mờ vào, trượt lên và phóng dần về cỡ chuẩn. `.is-condensed` bật khi `--p` ≥ 0.5 |
| `__tools` `__tool` | Nhóm nút icon 40px: tìm kiếm, tài khoản, thông báo |
| `__tool[data-arg-fav-toggle]` | Nút ngôi sao yêu thích: hai icon `.arg-fav__on` (`star-fill`) và `.arg-fav__off` (`star`). Bấm đổi `aria-pressed`; đã yêu thích thì sao đặc màu vàng (`--arg-p-brand-yellow`). Nhãn đổi theo `data-label-on` `data-label-off`. Bắn `arg:fav` kèm `detail.on` |
