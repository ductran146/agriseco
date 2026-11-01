# Quy tắc cho agent khi làm UI Agriseco (ARG)

Đọc hết file này trước khi thêm hoặc sửa component, trang, token. Quy tắc đã được chốt với chủ dự án trong quá trình làm. Không tự đổi; muốn đổi thì hỏi.

Ngôn ngữ làm việc và giao diện: **tiếng Việt**. Khách xem demo là khách hàng của Agriseco, không phải designer.

## 1. Cấu trúc và cách build

```
arg-design-tokens/
  arg-tokens.css, *.tokens.json, build_arg.py   Token ARG (--arg-*), dựng từ TradeX/Paave
  ui/
    base/            base.css (biến CSS ngoài token), core.js (ARG.register, ARG.$, ARG.once, ARG.icon)
    components/<tên>/<tên>.css|html|md|js        Mỗi component một thư mục
    components.json  "components": mục trong viewer (theo thứ tự). "css": thứ tự nạp CSS
    icons/*.svg      Icon Solar, build gộp thành sprite
    pages/           build_pages.py (mỗi màn một file trong dist/screens/ kèm khung xem), detail_parts.py, trade_parts.py, logo, status bar
    viewer/          vỏ viewer (shell.css, shell.js)
    build.py         Dựng dist/arg-ui.css, arg-ui.js, arg-ui-viewer.html và chạy kiểm tra
    dist/            Kết quả build. Không sửa tay
```

Lệnh (chạy trong `ui/`, luôn có `-I`):

```
python3 -I build.py            # phải không có dòng FAIL
python3 -I pages/build_pages.py
```

Sau khi sửa component: build, rồi build trang, rồi kiểm tra bằng mắt (mục 9).

## 2. Token và màu

- Mọi màu, cỡ chữ, khoảng cách, bo góc, bóng lấy từ token `--arg-*`. Không viết mã màu thô (`#fff`, `rgb()`), số px thô khi đã có token. Ngoại lệ đã được chấp nhận: chữ trắng `#fff` trên nền màu trạng thái.
- Build kiểm tra biến CSS không tồn tại. Nếu cần biến mới ngoài Figma thì định nghĩa trong `base/base.css` hoặc trong CSS component, ghi chú rõ không phải token Figma. Hiện có: `--arg-gutter`, `--arg-safe-top`, `--arg-safe-bottom`, thang `--arg-radius*`.
- **Tăng, giảm, tham chiếu, trần, sàn** chỉ dùng token giao dịch: tăng `--arg-trading-up-light-increase` (xanh), giảm `--arg-trading-down-light-increase` (đỏ), tham chiếu `--arg-trading-flat-flat` (vàng), trần `--arg-trading-ceiling-purple-flat`, sàn `--arg-trading-floor-cyan-flat`. Dùng lớp `.arg-up`, `.arg-down`, `.arg-ref`.
- **Mua và Bán là hai màu riêng**: `--arg-action-buy-button-*` và `--arg-action-sell-button-*`. Không dùng chung màu với thành công, lỗi.
- **Nút chính (primary)**: nền gradient `--arg-gradient-primary-button`, lấy đúng gradient header agriseco.com.vn (`--arg-p-brand-header-start` đến `--arg-p-brand-header-end`). Build có kiểm tra điều này.
- **Thang màu 11 bậc như Tailwind CSS** (50, 100, 200 … 900, 950): `--arg-p-neutral-*` (trung tính thuần, không ngả xanh), `--arg-p-primary-agri-orange-*` (600-M là cam header web `#EA5B2F`), `--arg-p-primary-agri-red-*` (600-M là đỏ logo `#A5000A`). Màu trung tính của nền, đường kẻ, chữ lấy từ các thang này và từ `Alpha.Black` gốc đen thuần. Không dùng Gray Raven của TradeX cũ (đã bỏ). Muốn đổi màu thì sửa `build_arg.py` rồi chạy lại (`python3 -I build_arg.py <thư mục design-tokens nguồn> <arg-design-tokens>`), không sửa tay `arg-tokens.css`.
- **Màu biểu đồ phân loại** (donut, cột, thanh chia tỷ lệ) lấy `--arg-viz-1` đến `--arg-viz-6` trong `base/base.css`, tông Agriseco: cam đỏ thương hiệu, hổ phách, đỏ đậm, xám trung tính. Không dùng xanh dương của TradeX cũ (Royal Blue) và không dùng xanh lá, đỏ của tăng giảm.
- Vùng tô mờ theo màu trạng thái dùng `color-mix(in srgb, var(--màu) N%, transparent)`.
- Nền mờ của thanh dính: `color-mix(in srgb, var(--arg-ui-background-…) 85%, transparent)` kèm `backdrop-filter: blur(20px) saturate(1.4)`.
- Đã biết, chưa sửa: chữ trắng trên nền gradient, Mua, Bán, vàng, cyan có độ tương phản dưới AA. Không giả vờ đã đạt AA.

## 3. Kích thước, bo góc, khoảng cách

- **Chiều cao điều khiển** (button, input, select, stepper, công tắc Mua/Bán): mặc định **40px**; sm 32, xl 44, xxl 48. Token `--arg-border-height-size-height-{small|normal|xl|xxl}`. Build kiểm tra.
- **Bo góc**: mốc **13px** cho điều khiển cao 40px. Công thức `--arg-radius-control = chiều cao × 0,325` (32 → 10,4; 40 → 13; 44 → 14,3; 48 → 15,6). Thang khác theo mốc: `--arg-radius-xs` (×0,5), `--arg-radius-sm` (×0,75), `--arg-radius` (13), `--arg-radius-lg` (×1,5). Thẻ lớn dùng `--arg-radius-lg`, thẻ vừa `--arg-radius`.
- **Chip** (Chip tabs): lấy tỷ lệ trên rồi làm tròn về giá trị có trong token bo góc: cao 40 và 32 → 12 (`--arg-border-radius-rounded-lg`), cao 28 → 8 (`--arg-border-radius-radius-md`). Không bo tròn hết cỡ.
- Hình tròn (avatar, chấm) vẫn 50%.
- **Lề hai bên với mép thiết bị: 20px** (`--arg-gutter`). Dải cuộn ngang tràn mép dùng `margin: 0 calc(var(--arg-gutter) * -1)` và `padding-inline: var(--arg-gutter)`.
- Các khối chính của một trang cách nhau **32px**. Trang nền trắng chia mục (`.arg-screen--sections`): mỗi khối trắng tràn mép, cách nhau **10px** bằng màu nền xám của trang.
- Bóng mềm (`--arg-shadow-soft-shadow`) lan khoảng 50px. Dải cuộn ngang (`overflow-x:auto`) sẽ cắt bóng: chừa padding 24px trên, 48px dưới và bù bằng margin âm. Không để khối kế tiếp đè lên bóng.

## 4. Icon

- Chỉ dùng bộ **Solar** (Iconify `solar`, https://icones.js.org/collection/solar, tác giả 480 Design, giấy phép **CC BY 4.0** nên cần ghi nguồn). Tên file trong `ui/icons/` giữ tên nội bộ (`caret-down`, `house`…), nội dung là icon Solar tương ứng; build tự gộp sprite và giữ `viewBox` từng file (lưới 24). Không trộn bộ khác.
- **Linear** (nét 1,5) cho icon thường. **Bold Duotone** chỉ cho thanh tab dưới và ô dịch vụ yêu thích (tên đuôi `-duotone`). **Bold** chỉ cho mũi tên tăng giảm nhỏ (`caret-up-fill`, `caret-down-fill`), ngôi sao đặc và dấu tròn chọn đặc (`check-circle-fill`).
- Thêm icon: lấy `https://api.iconify.design/solar/<tên>-<kiểu>.svg` (kiểu `linear`, `bold`, `bold-duotone`), gửi User-Agent giống trình duyệt, ghi vào `ui/icons/<tên nội bộ>.svg`, giữ `viewBox` và `fill="currentColor"` ở thẻ svg.
- Ngoại lệ: `candlestick.svg` do mình vẽ theo lưới 24, nét 1,5 như Solar (Solar không có icon nến), thân nến tô màu tăng, giảm. Muốn thêm icon tự vẽ phải ghi rõ.
- **Yêu thích / theo dõi mã luôn là ngôi sao**, không dùng trái tim. Chưa yêu thích: `star` (nét); đã yêu thích: `star-fill` màu vàng `--arg-p-brand-yellow` (`.arg-fav`, `[data-arg-fav-toggle]`). Đây là ngoại lệ được phép của quy tắc Bold.
- Dùng `<i data-arg-icon="tên"></i>` hoặc `ARG.icon('tên', 'i--16')`. Cỡ mặc định theo chữ; có `i--16`, `i--20`, `i--24`. Icon trong nút icon phải đo đúng kích thước yêu cầu (đã từng lỡ: nút 24px nhưng icon 13px).
- Icon chỉ có nghĩa khi có `aria-label` nếu đứng một mình.

## 5. Component

- **Mỗi pattern một component riêng**, không gộp 2 đến 3 pattern vào một thư mục. Thư mục gồm: `<tên>.css`, `<tên>.html` (ví dụ cho viewer, dạng `<section id="tên">`), `<tên>.md` (Dùng khi, bảng Class, JS), thêm `<tên>.js` nếu có hành vi.
- Thêm component: tạo thư mục, thêm vào `components.json` (`components` và `css`, đúng thứ tự phụ thuộc), nếu có JS thì thêm tên vào `js_order` trong `build.py`.
- **Component mới bắt buộc xuất hiện trong viewer** (`dist/arg-ui-viewer.html`, file để review UI). Nghĩa là có mục trong `components.json` → `components` kèm `id` và `title`, có `<tên>.html` làm ví dụ đủ các biến thể và trạng thái, có `<tên>.md`. Build chỉ kiểm tra thư mục đã khai báo; thư mục quên khai báo sẽ **không** báo lỗi mà lặng lẽ không hiện trong viewer, nên sau khi build phải mở viewer và thấy mục mới. Sửa component có sẵn thì cập nhật luôn ví dụ trong viewer.
- Ngoại lệ có chủ đích: `field` (CSS nền cho input, select) và `colors` (chỉ có ví dụ, không có CSS riêng) không phải component độc lập.
- Tên lớp: `.arg-<tên>`, phần tử `__x`, biến thể `--x`. Hành vi gắn bằng `data-arg-*`. Không dùng `id` để gắn hành vi.
- JS: `ARG.register(tên, fn(root))`, dùng `ARG.once(el, khoá)` để tránh gắn trùng. Sự kiện tuỳ biến đặt tên `arg:*` và bắn kèm `detail`.
- Build kiểm tra: class trong ví dụ phải có CSS, icon dùng phải có trong sprite, mỗi component có html và md. Ví dụ html chỉ dùng class đã định nghĩa.
- Tài liệu `.md` viết tiếng Việt, ngắn. Khi đổi hành vi hay kích thước, cập nhật `.md` và ví dụ `.html` cùng lúc.
- Component dùng lại component khác thì tham chiếu, không chép CSS (ví dụ chip hành động dùng `.arg-chip-tab`, hàng KV dùng `.arg-badge`).

## 6. Quy tắc trang và hành vi

- **Mỗi giao diện là một file riêng** (`dist/screens/<id>.html`: `home`, `market`, `trade`, `stock-<mã>`, `trade-<mã>`, `idx-<id>`), không gộp tất cả vào một file. CSS, JS, font nằm chung ở `screens/assets/`. Màn mới thêm vào danh sách `SCREENS` trong `build_pages.py`. Bấm sang màn khác (`data-arg-go`) mở file của màn đó, nút quay lại dùng lịch sử trình duyệt.
- Khung mô phỏng iPhone: **375×812**; tablet 768×1068. Không có view desktop. Có status bar iOS, home indicator, vùng an toàn: `--arg-safe-top` 44px, `--arg-safe-bottom` 34px (khung xem trước đặt, thiết bị thật dùng `env()`).
- **Không hiện thanh cuộn dọc** (ẩn thanh, vẫn cuộn bằng lăn chuột hoặc vuốt). Màn đặt lệnh phải **vừa trọn một màn hình, không cuộn**; kiểm tra bằng `documentElement.scrollHeight === 812`.
- Thanh đầu (`.arg-appbar--sticky`) và thanh tab dưới (`.arg-tabbar--fixed`) dính, nền mờ 85% cùng token nền, làm nhoè nội dung cuộn qua. Header phủ luôn vùng status bar (padding `--arg-safe-top`).
- Trang chủ: logo Agriseco thay chữ "Trang chủ" (`.arg-appbar__logo`, SVG nội tuyến). Chỉ số: thẻ `a.arg-index[data-arg-go]` mở trang chi tiết.
- Chuyển màn dùng component Screen: `data-arg-screen`, `data-arg-go`, `data-arg-back`; mục thanh tab thêm `data-arg-root`. Mỗi màn gốc tự chứa thanh tab của nó (đánh dấu `aria-current` đúng màn). Link giữ chỗ `href="#"` luôn `preventDefault` (trong iframe `srcdoc` sẽ tải lại trang).
- Chuyển động bám tốc độ cuộn dùng biến `--p` (0 đến 1) cập nhật trong sự kiện `scroll`, không dùng `requestAnimationFrame` (headless không chạy). Mọi animation phải tôn trọng `prefers-reduced-motion`.
- Biểu đồ: các chế độ (nến, đường) **cùng chiều cao** để đổi chế độ không làm xô lệch giao diện. Đường gióng, nhãn giá, tooltip chỉ hiện khi rê chuột hoặc chạm giữ ~250ms rồi kéo; vuốt nhanh vẫn cuộn trang.
- Đóng thẻ (`data-arg-dismiss="selector"`): thu chiều cao, mờ dần, triệt luôn gap để khối dưới trượt lên.
- Nút icon chọn chế độ hiển thị **luôn hiện chế độ sẽ chuyển tới** (đang nến thì hiện icon sóng).

## 7. Nội dung và định dạng

- Toàn bộ chữ giao diện tiếng Việt, kể cả nhãn khuyến nghị (B, G, M) và tên mục. Giữ nguyên tên riêng: Lite, Pro, mã chứng khoán, loại lệnh LO, MP, ATO, ATC.
- Số kiểu Việt Nam: dấu chấm ngăn nghìn, dấu phẩy thập phân (`1.312,07`, `-0,41%`). Dùng `font-variant-numeric: tabular-nums` cho số. Phần trăm thay đổi có dấu `+` hoặc `-`.
- Dữ liệu mẫu phải **nhất quán**: giá, thay đổi, phần trăm, tham chiếu, trần, sàn, giá trị ước tính khớp phép tính. Cổ phiếu cơ sở: HOSE bước giá 0,10 với giá từ 50.000đ, bước khối lượng 100, trần và sàn ±7%. Hiện dùng VCB, tham chiếu 92,10, trần 98,50, sàn 85,70.
- Dữ liệu mẫu chưa có thật: nói rõ trong báo cáo cho người dùng, không để khách hiểu là số thật.

## 8. Panel mô tả bên phải khung xem (máy tính)

- Trong `pages/build_pages.py` (biến `INFO`): mỗi màn có `name`, `desc`, `feat` (Tính năng), `try` (Thử ngay).
- **Đối tượng đọc là khách hàng của Agriseco.** Viết bằng ngôn ngữ nghiệp vụ, câu ngắn. **Không** đưa tên component, token, thông số px, "nền mờ 85%", hay chú thích kiểu "mới đổi trạng thái".
- Thêm màn hoặc tính năng mới thì cập nhật `INFO`. Không liệt kê chức năng chưa chạy ở mục "Thử ngay".

- **Đặc tả trên giao diện** (kiểu ghi chú Figma): công tắc "Đặc tả" trên thanh đầu khung xem bật chấm đánh số trên từng thành phần, nối bằng đường nét đứt tới bong bóng ở hai bên khung thiết bị (nhớ trạng thái trong phiên, tự ẩn ở chế độ Toàn màn hình và cửa sổ hẹp). Nội dung nằm ở `pages/specs.py` (theo từng màn: bộ chọn CSS, cạnh `l` hoặc `r`, nội dung ngắn dưới khoảng 100 chữ: tên component, kích thước, token, hành vi). Khác với panel mô tả ở trên, đặc tả viết cho người làm sản phẩm nên được phép có tên component và token. Thêm màn hoặc thành phần mới thì thêm mục đặc tả tương ứng.

## 9. Kiểm tra trước khi báo xong

Không báo "xong" nếu chưa chạy. Dùng Chrome headless:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --window-size=900,800 --force-device-scale-factor=2 --virtual-time-budget=9000 \
  --screenshot=<file>.png "file://<đường dẫn>/dist/screens/home.html"
```

- Cửa sổ Chrome tối thiểu khoảng 500px rộng; muốn xem đúng 375px thì xem trong khung của `dist/screens/<màn>.html` (mỗi màn một file, dùng chung `screens/assets/`; `index.html` liệt kê tất cả). Muốn thao tác (bấm, cuộn) thì chép cả thư mục `screens/` vào scratchpad, chèn thẻ `<script>` vào bản sao rồi chụp, hoặc `--dump-dom` và đọc `document.title`.
- `window.scrollTo` trong headless không bắn `scroll` đáng tin: sau khi cuộn, tự `dispatchEvent(new Event('scroll'))` khi thử.
- Đo bằng số khi quy tắc có số: `getBoundingClientRect`, `getComputedStyle` (chiều cao 40, bo góc, cỡ icon, `scrollHeight`).
- Xem ít nhất Mobile. Tablet và toàn màn hình nếu đụng bố cục. Chụp lúc animation đã xong (chờ 1 giây trong `setTimeout`).
- File tạm để trong scratchpad, không để trong dự án.
- Báo cáo trung thực: nói rõ cái gì **đã** kiểm tra, cái gì **chưa**, và điểm còn hạn chế.

## 10. Cách báo cáo cho người dùng

- Trả lời tiếng Việt, ngắn, nói điều đã làm và điều đã kiểm tra.
- Khi làm khác ảnh mẫu (màu theo token, giản lược dữ liệu, bỏ phần cho vừa màn hình), nói rõ khác chỗ nào và vì sao.
- Không tự làm việc ngoài yêu cầu. Quyết định thiết kế chưa rõ: chọn mặc định hợp lý, nói ra, và để người dùng đổi.
- Còn tồn đọng đã biết (không tự làm khi chưa được yêu cầu): chọn đỏ `#A5000A` hay cam đỏ cho link, phụ, outline; cập nhật `arg-design-tokens/README.md` (thư mục `ui/`, token XL/XXL, gradient header, token Mua, Bán); nâng `--arg-gutter`, thang bo góc thành token chính thức trong `build_arg.py`; sửa tương phản; đồng bộ chiều lệnh Mua, Bán giữa Lite và Pro.
