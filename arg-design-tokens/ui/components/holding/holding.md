## Dùng khi
Danh sách cổ phiếu đang nắm giữ trong tài khoản (tab Danh mục): mỗi mã một thẻ hai dòng, thay cho bảng nhiều cột trên màn hẹp.
## Class
| Class | Mô tả |
|---|---|
| `.arg-holding-list` | Danh sách thẻ, cách nhau 8px (`ul`) |
| `.arg-holding` | Một thẻ, nền `--arg-ui-background-background` (nhạt, gần nền trang), bo `--arg-radius`, hai cột: thông tin mã và kết quả |
| `__id` | Liên kết, vùng bấm phủ cả thẻ. Dòng 1: mã (`b`) và `__last` giá hiện tại (màu `.arg-up` `.arg-down` `.arg-ref` theo biến động trong phiên). Dòng 2: `__meta` khối lượng và giá vốn, chữ xám |
| `__pl` | Kết quả lãi/lỗ: số tiền (`b`) và `.arg-badge` phần trăm so với giá vốn, cùng một màu (`up` lãi, `down` lỗ, `ref` hoà vốn) |
Mỗi con số có một vai trò: giá (màu theo phiên), vốn (xám), lãi/lỗ (màu theo kết quả). Không dùng cùng một màu cho hai ý khác nhau cạnh nhau.
