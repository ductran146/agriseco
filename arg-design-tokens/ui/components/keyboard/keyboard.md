## Dùng khi
Mô phỏng bàn phím điện thoại trong bản demo: bấm vào ô nhập thì bàn phím trượt lên từ đáy màn hình, đúng loại theo nội dung ô (số hay chữ). Không dùng cho bản chạy thật, hệ điều hành đã có bàn phím riêng.
## Kiểu bàn phím theo ô nhập
| Ô nhập | Bàn phím |
|---|---|
| `inputmode="numeric"` hoặc `type="number"` | Phím số 0 đến 9 (khối lượng, số lượng) |
| `inputmode="decimal"` | Phím số kèm dấu phẩy (giá) |
| `type="tel"` hoặc `inputmode="tel"` | Phím số điện thoại có chữ ABC dưới số và phím `+*#` |
| Còn lại (`text`, `search`, `email`...) | Bàn phím chữ, có trang số và ký hiệu (phím 123 / ABC), chữ hoa (bấm 2 lần để khoá) |
| `date`, `checkbox`, `radio`, ô chỉ đọc | Không hiện bàn phím |
## Class
| Class | Mô tả |
|---|---|
| `.arg-kb` | Khối cố định ở đáy, rộng tối đa 768px, trượt lên bằng `.is-open`. Gồm `__bar` (thanh Xong cao 48px), `__body` (cao 270px), `__home` (vạch Home 21px); tổng 291px, thêm thanh Xong là 339px (`--arg-kb-h`) |
| `__key` `--fn` `--bare` `--c` | Phím trắng bo 5px đổ bóng 1px; `--fn` phím chức năng (xám); `--bare` chỉ có ký hiệu |
| `__num` `__alpha` | Lưới phím số (3 × 4) và phím chữ (20 cột) |
| `.arg-kb-open` (trên html) | Trang chừa chỗ cho bàn phím; bảng trượt từ dưới (Offcanvas) nổi lên trên bàn phím |
| `.arg-kb--static` | Bản tĩnh dùng để minh hoạ, tạo bằng `data-arg-kb-static="num | decimal | tel | alpha"` |
Màu và cỡ chữ lấy theo bản vẽ bàn phím iOS nên khai báo bằng `--kb-*` trong component, không dùng token ARG. Có bản chế độ tối.
## Hành vi (JS)
- Chỉ chạy với ô nhập nằm trong `.arg-page`. Ô được đặt `inputmode="none"` để bàn phím hệ điều hành không hiện cùng lúc; gõ bằng bàn phím máy tính vẫn dùng được.
- Phím gõ chèn ký tự vào đúng vị trí con trỏ rồi bắn sự kiện `input`; phím xoá giữ để xoá liên tục.
- Phím xuống dòng đổi nhãn theo `enterkeyhint` (`search` là Tìm, `go` là Đi, `next` là Tiếp, mặc định Xong), bấm thì bắn Enter và đóng bàn phím. Nút Xong trên thanh công cụ cũng đóng.
- Bấm ra ngoài ô nhập thì bàn phím hạ xuống; trang tự cuộn để ô đang nhập không bị che.
- Bắn `arg:keyboard` ({ open, mode }) trên `document`.
## Phụ thuộc
Icon (`keyboard`, `backspace`, `arrow-fat-up`).
