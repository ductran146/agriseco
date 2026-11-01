## Dùng khi
Điều hướng chính trên mobile và tablet.
## Class
| Class | Mô tả |
|---|---|
| `.arg-tabbar` | Thanh dưới, mỗi mục chia đều |
| Vùng an toàn đáy | Chừa chỗ cho home indicator của iPhone: dùng `env(safe-area-inset-bottom)` trên thiết bị thật, hoặc đặt `--arg-safe-bottom` (iPhone là 34px) khi xem trong khung mô phỏng |
| `--fixed` | Dính đáy khung cuộn, nền 85% mờ và làm nhoè nội dung cuộn bên dưới |
| `__item` | Mục gồm icon 24px và nhãn; `aria-current="page"` là mục đang chọn |

Icon dùng kiểu Solar Bold Duotone (`house-duotone`, `chart-line-duotone`, `arrows-left-right-duotone`, `wallet-duotone`, `squares-four-duotone`). Phần nền icon mờ 20%, nét chính theo màu chữ của mục.
