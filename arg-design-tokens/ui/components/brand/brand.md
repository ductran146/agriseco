## Dùng khi
Muốn gắn nhận diện Agriseco vào một khối: hình chìm trên thẻ nổi bật (thẻ tài sản, banner), và chữ ký thương hiệu ở cuối trang chính.
## Class
| Class | Mô tả |
|---|---|
| `.arg-brandmark` | Hình ba lá lúa cắt từ logo gốc, tô bằng mask, màu lấy từ `--mark` (mặc định trắng mờ 16% cho nền gradient). Đổi cỡ bằng `--size` (mặc định 120px). Luôn `aria-hidden="true"` |
| `--soft` | Màu cam mờ 14% cho nền sáng |
| `--corner` | Đặt ở góc phải trên, nghiêng 8°, tràn mép. Khối cha cần `position: relative; isolation: isolate; overflow: hidden` |
| `--side` | Đặt lệch phải, ngang tầm giữa khối, dùng khi góc trên đã có avatar hoặc nút |
| `.arg-brandsign` | Chữ ký cuối trang: logo (cao 40px), `__name` (đỏ logo), `__sub` |
Họa tiết không mang thông tin nên không cần thay thế văn bản. Không dùng để thay logo ở thanh đầu.
