# ARG UI

Component CSS và JS dựng từ token ARG. Mỗi component là một thư mục.

## Cấu trúc

```
ui/
  base/            base.css (reset, keyframes dùng chung) và core.js (đăng ký module, tự khởi tạo)
  components/<tên>/
    <tên>.css      style, chỉ dùng biến --arg-*
    <tên>.js       hành vi (chỉ component có tương tác)
    <tên>.html     ví dụ HTML, là nguồn markup mẫu
    <tên>.md       tài liệu: class, trạng thái, JS, phụ thuộc
  icons/           SVG Solar (Linear, Bold Duotone, Bold; CC BY 4.0), build gộp thành sprite
  viewer/          vỏ trang xem (sidebar, đổi sáng/tối, kiểm tra), không chứa component
  components.json  thứ tự component và thứ tự nạp CSS
  build.py         gộp file và chạy kiểm tra
  dist/            kết quả build
```

`field.css` là lớp nền chung của input, select, checkbox. `offcanvas` dùng chung `modal.css` và `modal.js`.

## Dùng trong dự án

```html
<link rel="stylesheet" href="dist/arg-tokens.css">
<link rel="stylesheet" href="dist/arg-ui.css">
<body class="arg-ui">
  <button class="arg-btn arg-btn--primary">Đặt lệnh</button>
  <script src="dist/arg-ui.js"></script>
</body>
```

- Bọc giao diện trong phần tử có class `arg-ui`. Overlay và toast gắn vào phần tử này để nhận đúng token sáng hoặc tối.
- Chế độ tối: đặt `data-theme="dark"` trên `<html>`.
- JS tự khởi tạo qua thuộc tính `data-arg-*`. Chèn markup mới thì gọi `ARG.init(phầnTử)`.
- Sự kiện: `arg:tab`, `arg:slide`, `arg:select`, `arg:change`, `arg:dismiss`, `arg:open`, `arg:close`.

## Build

```bash
python3 ui/build.py
```

Script ghi `dist/arg-ui.css`, `dist/arg-ui.js`, `dist/arg-tokens.css`, `dist/build-report.json` và `dist/arg-ui-viewer.html`.

Kiểm tra lúc build (script thoát với mã 1 nếu có lỗi):

- Mọi biến `--arg-*` được dùng đều có trong token.
- Mọi class `arg-*` trong ví dụ đều có CSS.
- Mọi icon dùng đều có trong sprite.
- Mỗi component có ví dụ HTML và tài liệu.
- Token chiều cao 32 / 40 / 44 / 48 và gradient nút chính tồn tại.

## File xem

`dist/arg-ui-viewer.html` là một file duy nhất: token, font Pretendard, `arg-ui.css`, `arg-ui.js`, ví dụ và tài liệu của từng component. Trang không có CSS hay JS riêng cho component. Khi mở, mục Kiểm tra đo chiều cao thật của nút, input, select và xác nhận từng module đã khởi tạo.

## Thêm component

1. Tạo `components/<tên>/` với `.css`, `.html`, `.md` (và `.js` nếu cần).
2. Thêm vào `components.json` (danh sách và thứ tự nạp CSS), thêm `.js` vào `js_order` trong `build.py`.
3. Chạy `python3 ui/build.py`.
