## Dùng khi
Lúc mở ứng dụng, trước khi thấy Trang chủ.
## Class
| Class | Mô tả |
|---|---|
| `.arg-splash` | Phủ toàn màn, nền gradient thương hiệu, `z-index` 100 |
| `__tile` | Ô trắng 96px bo `--arg-radius-lg` chứa logo |
| `__name` `__sub` | Tên và dòng phụ, hiện lần lượt từ dưới lên |
| `.is-leaving` | Đang mờ dần (JS gắn) |
| `--inline` | Bản nhúng tĩnh trong khung, dùng cho ví dụ |
## JS
`splash.js`: phần tử `[data-arg-splash]` hiện khoảng 1,1 giây rồi mờ 0,4 giây và bị gỡ; chỉ một lần mỗi phiên (`sessionStorage`). Khi bật giảm chuyển động thì gỡ ngay. Bắn `arg:splash` trên `document` khi đã gỡ.
