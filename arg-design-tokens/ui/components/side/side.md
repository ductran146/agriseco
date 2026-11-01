## Dùng khi
Chọn chiều lệnh trước khi đặt.
## Class
| Class | Mô tả |
|---|---|
| `.arg-side` | Khung cao 40px, bo theo tỷ lệ chiều cao như Button, nền xám nhạt |
| `__btn` `--buy` `--sell` | Hai lựa chọn; `aria-pressed="true"` là lựa chọn đang chọn (nền xanh Mua hoặc đỏ Bán) |
| `.arg-buy` `.arg-sell` | Màu chữ chiều lệnh trong bảng (ví dụ cột M/B ở khớp lệnh) |
## Mở màn đặt lệnh với chiều chọn sẵn
Nút có `data-arg-go="màn"` và `data-arg-side="buy"` hoặc `"sell"` (ví dụ thanh Mua / Bán ở trang thông tin mã): sau khi mở màn, mọi `.arg-side__btn` đúng chiều trong màn đó được chọn.
## Công tắc chế độ
`[data-arg-modes]` trên Tabs với `tab[data-mode]`: khi đổi tab, màn hình chứa nó nhận `data-mode`. CSS ẩn hiện theo đó (ví dụ Lite và Pro của màn Giao dịch).
## JS
`side.js`: trong `[data-arg-order]`, bấm lựa chọn thì cập nhật `data-side`, đổi nút `[data-arg-order-cta]` sang `.arg-btn--buy` hoặc `--sell` và nhãn "Mua - MÃ" hoặc "Bán - MÃ" (mã lấy từ `data-symbol`). Bắn `arg:side`. Nút `[data-arg-go][data-arg-side]` chọn sẵn chiều lệnh ở màn được mở.
