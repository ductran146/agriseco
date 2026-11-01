## Dùng khi
Đầu màn Tài sản: tổng tài sản của tiểu khoản và lãi/lỗ hôm nay, có nút ẩn số khi người dùng ở nơi đông người.
## Class
| Class | Mô tả |
|---|---|
| `.arg-assetcard` | Thẻ nền gradient thương hiệu (`--arg-gradient-primary-button`, quầng sáng và hai vòng trang trí như phần đầu thẻ Account), chữ trắng, bo `--arg-radius-lg`, bóng `--arg-shadow-shadow`, đệm 20px |
| `__label` | Nhãn "Tổng tài sản (đ)" kèm nút `.arg-icon-btn[data-arg-asset-eye]` (icon 20px) |
| `__amount` | Tổng tài sản, Header 3 đậm, số đều chiều rộng |
| `__delta` | Nhãn "Lãi/lỗ hôm nay" nền trắng đặc (chữ xám trên trắng, không đặt chữ màu trực tiếp lên gradient): icon `trend-up` hoặc `trend-down`, số tiền và phần trăm tô `.arg-up` `.arg-down` |
## Hành vi (JS)
Bấm nút mắt ẩn hoặc hiện mọi `[data-arg-secret]` trong `[data-arg-secret-scope]` gần nhất (cả tab Tài sản; không có vùng thì chỉ trong thẻ). Icon luôn là trạng thái sẽ chuyển tới. Bắn `arg:secret` ({ hidden }).
## Phụ thuộc
Button (`.arg-icon-btn`), Icon.
