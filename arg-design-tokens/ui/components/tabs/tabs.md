## Dùng khi
Chuyển giữa các nhóm nội dung cùng cấp trong một vùng.
## Class
| Class | Mô tả |
|---|---|
| `.arg-tabs[data-arg-tabs]` | Khung; gạch chân gradient |
| `--pill` `--vertical` | Kiểu viên thuốc và kiểu dọc |
| `--fill` | Dải tab (kiểu `--pill`) chiếm hết bề rộng, các tab chia đều, dùng cho nhóm icon |
| `--lg` | Tab lớn làm tiêu đề màn hình (Title 3 đậm, cao 48px, gạch chân đúng bề rộng chữ), ví dụ Lệnh thường, Lệnh điều kiện |
| `[role=tablist]` > `.arg-tab` | Dải tab |
| `[role=tabpanel]` | Nội dung, cùng thứ tự với tab |
## JS
`tabs.js`: chỉ điều khiển tab và tabpanel thuộc chính nó (có thể lồng Tabs trong một tabpanel). Phím mũi tên, Home, End (Up/Down khi `aria-orientation="vertical"`). Bỏ qua tab `disabled`. Bấm một tab trong dải cuộn ngang thì dải tự cuộn để tab đó nằm trọn trong tầm nhìn. Bắn `arg:tab`. `data-arg-tabs-sync="nhóm"` trên nhiều bộ tab: chọn ở một bộ thì các bộ cùng nhóm chọn cùng vị trí.
