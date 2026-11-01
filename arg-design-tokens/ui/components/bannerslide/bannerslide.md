## Dùng khi
Dải banner ảnh quảng bá (ảnh webp có sẵn chữ) ở trang chủ: nhiều ảnh trượt ngang, chiếm một hàng.
## Class
| Class | Mô tả |
|---|---|
| `.arg-bslide[data-arg-bslide]` | Khung. Đặt như một ô trong hàng hai cột (`.arg-page__cols`) hoặc cả hàng |
| `__track` | Dải cuộn ngang, dính từng ảnh (scroll-snap), bo `--arg-radius-lg`, ẩn thanh cuộn |
| `__item` | Một ảnh (liên kết), rộng đúng khung |
| `__dots` `__dot` | Chấm vị trí ở đáy ảnh, chấm hiện tại dài 16px (`aria-current="true"`) |
## JS
`bannerslide.js`: chấm theo vị trí cuộn, bấm chấm cuộn tới ảnh; tự chuyển sau 5 giây, dừng khi rê chuột, chạm hoặc focus; tắt khi bật giảm chuyển động. Kéo bằng chuột trên máy tính nhờ Dragscroll. Bắn `arg:bslide` (`detail.index`).
