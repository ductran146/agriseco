## Dùng khi
Tóm tắt tài sản của tiểu khoản ở đầu trang chủ: tổng tài sản, biến động hôm nay, phân bổ cổ phiếu và tiền mặt, lãi/lỗ danh mục.
## Class
| Class | Mô tả |
|---|---|
| `.arg-account` | Thẻ, bo `--arg-radius-lg`, bóng `--arg-shadow-shadow` |
| `__head` | Phần đầu nền gradient thương hiệu (`--arg-gradient-primary-button`, theo header agriseco.com.vn) kèm quầng sáng và hình chìm lá lúa (không có vòng tròn trang trí); chữ trắng |
| `__top` `__avatar` `__hello` `__greet` `__no` | Hàng lời chào nằm ngoài thẻ, phía trên: avatar gradient 40px, lời chào (Body 3 đậm) và số tài khoản (Label 1, trắng mờ) |
| `__label` `__eye` | Nhãn "Tổng tài sản (đ)" kèm nút ẩn/hiện 24×24px (icon 20px) |
| `__amount` | Tổng tài sản, Header 3 (28/36) đậm, số đều chiều rộng |
| `__delta` | Nhãn biến động hôm nay trên nền trắng mờ 16%, icon `trend-up` hoặc `trend-down` |
| `__alloc` `__bar` `__split` `__dot` `--cash` | Thanh phân bổ 6px (`--v` là % cổ phiếu: trắng đặc; tiền mặt: trắng mờ) và hai cột giá trị kèm chấm màu |
| `__sub` | Chọn tiểu khoản (X1 thường, M1 ký quỹ) ở bên phải hàng lời chào, ngoài thẻ: Select gốc (`.arg-control.arg-select`, chữ trung tính, rộng 96px, cao 40px). Tiểu khoản áp dụng cho cả tài khoản nên đặt cạnh số tài khoản, không đặt trong thẻ |
| `__body` | Phần thân trắng một hàng: lãi/lỗ bên trái, nút Nộp tiền bên phải |
| `__foot` `__pl` | Lãi/lỗ danh mục (tô `.arg-up` `.arg-down`) và nút Nộp tiền |
| `[data-arg-secret]` | Số được ẩn khi bấm nút mắt |
| `.is-hidden` | Thẻ đang ẩn số dư (JS gắn) |
## JS
`account.js`: bấm `[data-arg-account-eye]` thay mọi `[data-arg-secret]` trong thẻ bằng "••••••" hoặc trả lại số thật. Icon luôn là trạng thái sẽ chuyển tới (đang hiện: `eye-slash`, đang ẩn: `eye`), nhãn đổi giữa "Ẩn số dư" và "Hiện số dư". Bắn `arg:secret` (`detail.hidden`).

Số tổng tài sản đếm từ 0 lên giá trị thật (~600ms) khi thẻ hiện ra lần đầu; tắt khi bật giảm chuyển động. Hình chìm lá lúa dùng `.arg-brandmark--side` (xem Brand).

Phần trăm biến động và phân bổ vẫn hiện khi ẩn số dư, chỉ ẩn số tiền.
