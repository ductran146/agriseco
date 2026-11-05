"""Đặc tả gắn vào từng thành phần của giao diện (kiểu ghi chú của Figma): bật bằng công tắc "Đặc tả" trên thanh đầu khung xem.
Mỗi mục: (bộ chọn CSS trong màn hình, cạnh đặt bong bóng 'l' hoặc 'r', nội dung). Bộ chọn không khớp hoặc phần tử đang ẩn thì bỏ qua.
Đối tượng đọc là người làm sản phẩm (thiết kế, phát triển): có tên component, kích thước, token, hành vi."""

TAB = ('.arg-tabbar', 'l', 'Tabbar: 5 mục, dính đáy, nền mờ 85%, chừa vùng an toàn đáy 34px.')

HOME = [
    ('.arg-appbar__logo', 'l', 'Appbar --sticky: logo thay chữ, dính đầu, nền mờ 85%, phủ cả status bar.'),
    ('.arg-splash', 'r', 'Splash [data-arg-splash]: gradient header, ô logo 96px, hình chìm lá lúa (.arg-brandmark); hiện ~1,1s rồi mờ 0,4s và gỡ, một lần mỗi phiên.'),
    ('.arg-index-row', 'l', 'Market card: cuộn ngang, màu theo token giao dịch, bấm mở chi tiết chỉ số.'),
        ('.arg-account__top', 'l', 'Hàng lời chào nằm ngoài thẻ: avatar gradient 40px, lời chào và số tài khoản (mã tô màu link thương hiệu). Tiểu khoản áp dụng cho cả tài khoản nên đặt ở đây, không đặt trong thẻ.'),
    ('.arg-account__sub', 'l', 'Select gốc (.arg-control.arg-select) cao 40px, rộng 96px, chữ trung tính, mũi tên caret-down: chọn tiểu khoản X1 (thường) hoặc M1 (ký quỹ).'),
    ('.arg-account', 'r', 'Account: nền gradient header web, hình chìm là logo Agriseco gốc (trắng mờ 14%); tổng tài sản (con mắt ẩn số), biến động hôm nay, thanh phân bổ; thân trắng một hàng: lãi/lỗ danh mục bên trái, nút Nộp tiền bên phải. Số tổng đếm 0 → giá trị ~600ms.'),
    ('.arg-service-grid', 'l', 'Service trong khối nền trắng (.arg-service-grid--card): lưới 3 cột, ô icon gradient dịch vụ (vàng sang cam), icon trắng.'),
    ('.arg-reco-row', 'r', 'Reco: cuộn ngang, nhãn B, G, M, giá mục tiêu và lãi lỗ.'),
    ('.arg-quote-list', 'l', 'Quote: sparkline, giá và % theo 5 trạng thái, bấm mở thông tin mã. Mũi tên ở tiêu đề khối mở tab Yêu thích của Thị trường (data-arg-go kèm data-arg-tab).'),
    ('.arg-news-list', 'r', 'News: ảnh 88×64, tiêu đề tối đa 2 dòng, nguồn và ngày.'),
    ('.arg-brandsign', 'l', 'Brandsign: logo cao 40px, tên Agriseco (đỏ logo) và dòng phụ; chữ ký cuối trang.'),
    TAB,
]

MARKET = [
    ('.arg-tabs--lg', 'l', 'Tabs --lg: 7 mục cuộn ngang, đệm trên 0, sát thanh đầu. Tablet: thành Side panel dọc rộng 240px bên trái (kiểu Cài đặt macOS), mục chọn nền tối như Chip tabs đang chọn, nội dung mục ở bên phải.'),
    ('.arg-chip-tabs--sm', 'r', 'Chip tabs --sm: cao 32px, bo 12px; đổi góc nhìn thị trường.'),
    ('.arg-tabpanel .arg-tabs--pill', 'l', 'Tabs --pill: HOSE, HNX, UPCoM; giữ lựa chọn khi đổi góc nhìn.'),
    ('.arg-donut', 'r', 'Donut: số mã tăng, giảm, đứng; giữa vòng là tổng số mã. Rê chuột hoặc nhấn giữ 250ms một cung: cung phóng to 7%, cung khác mờ, giữa vòng hiện số liệu của cung.'),
    TAB,
]

STOCK = [
    ('.arg-appbar', 'l', 'Appbar --condense: mã và giá hiện dần theo tốc độ cuộn; sao đổi vàng khi bấm.'),
    ('.arg-pricehead', 'r', 'Pricehead: giá cỡ lớn, màu theo biến động so với tham chiếu.'),
    ('.arg-statrow', 'l', 'Statrow: KL, TC, Trần, Sàn, Mở, Cao, Thấp; màu theo token giao dịch.'),
    ('.arg-chart', 'r', 'Chart: nến hoặc đường cùng chiều cao; đường gióng chỉ hiện khi rê chuột hoặc chạm giữ 250ms.'),
    ('.arg-depth', 'l', 'Depth: dư mua trái, dư bán phải, thanh nền theo khối lượng.'),
    ('.arg-actionbar', 'r', 'Action bar --fixed: Mua, Bán dính đáy, mở màn đặt lệnh.'),
]

INDEX = [
    ('.arg-appbar', 'l', 'Appbar --condense: tiêu đề chuyển thành tên và giá chỉ số khi cuộn.'),
    ('.arg-pricehead', 'r', 'Pricehead: điểm chỉ số cỡ lớn, thay đổi theo token giao dịch.'),
    ('.arg-chart', 'l', 'Chart: nến hoặc đường; nút đổi chế độ hiện chế độ sẽ chuyển tới.'),
    ('.arg-perf-row', 'r', 'Perf: 7 ngày, 1 tháng, 1 năm, 5 năm; badge xanh đỏ.'),
    ('.arg-breadth', 'l', 'Breadth: số mã tăng, đứng, giảm; nền 8% màu trạng thái.'),
]

THEME = [
    ('.arg-hero', 'l', 'Hero: ảnh 168px trên nền cùng màu ảnh, nút quay lại và tìm kiếm.'),
    ('.arg-theme-head', 'r', 'Theme head: tên chủ đề, thay đổi trung bình, số mã.'),
    ('.arg-metric-row', 'l', 'Metric: 4 chỉ số, thẻ viền xám, giá trị cỡ Title 2.'),
    ('.arg-stockrow-list', 'r', 'Stock row: giá, %, KL; sao đổi vàng khi bấm.'),
    ('.arg-splitbar', 'l', 'Split bar: thanh tỷ lệ 10px kèm chú giải màu viz.'),
]

TRADE = [
    ('.arg-acctsel', 'l', 'Acctsel + Dropdown: xổ danh sách toàn chiều ngang, nền mờ như hộp thoại.'),
    ('.arg-appbar__tools .arg-appbar__tool:nth-child(1)', 'r', 'Appbar tool 40px, icon calendar-check, aria-label Sổ lệnh: mở màn Sổ lệnh (tab Sổ lệnh: lệnh trong ngày, huỷ lệnh). Màn này không có thanh tab dưới; Quay lại về Giao dịch.'),
    ('.arg-appbar__tools .arg-appbar__tool:nth-child(2)', 'r', 'Appbar tool 40px, icon chart-pie-slice, aria-label Danh mục: mở màn Tài sản (danh mục đang nắm giữ, cơ cấu tài sản). Là màn gốc của thanh tab dưới nên tab Tài sản được chọn.'),
    ('.arg-symbol', 'r', 'Tabs --pill: Lite (đặt nhanh) hoặc Pro (đủ sổ lệnh).'),
    ('.arg-pricehead', 'l', 'Pricehead --lg: giá khớp, màu theo biến động; Thông tin CP mở trang mã.'),
    ('.arg-statrow', 'r', 'Statrow: màu theo token giao dịch (tăng, giảm, tham chiếu).'),
    ('.arg-trade--pro .arg-split .arg-tabs', 'l', 'Tabs --pill: độ sâu hoặc danh sách; cao 40px, thẳng hàng công tắc Mua / Bán.'),
    ('.arg-trade--pro .arg-book', 'l', 'Book: dư bán trên, dư mua dưới, Trần tím, Sàn xanh ngọc; cao bằng cột form.'),
    ('.arg-trade--pro .arg-side', 'r', 'Side 40px: đổi chiều lệnh, đổi màu nút đặt lệnh (token Mua, Bán).'),
    ('.arg-trade--pro .arg-selectsheet', 'r', 'Select sheet: bấm mở bảng LO, MP, ATO, ATC; chữ căn giữa trục ô Giá, KL.'),
    ('.arg-trade--pro [data-arg-field="price"]', 'r', 'Stepper: bước giá HOSE 0,01 / 0,05 / 0,10; nút − và + thẳng hàng.'),
    ('.arg-trade--pro [data-arg-field="qty"]', 'r', 'Stepper: bước 100 cổ phiếu; đổi giá, KL thì tính lại giá trị ước tính.'),
    ('.arg-trade--pro .arg-kv', 'r', 'Kv: giá trị ước tính = giá × KL × 1.000, nằm đáy cột. Icon info cạnh Sức mua mở Offcanvas bottom: 5 dòng Kv --lines (sức mua, tiền có thể rút, ứng trước, phong toả, tạm giữ).'),
    ('.arg-trade--pro [data-arg-order-cta]', 'l', 'Button --xl cao 44px: mở hộp xác nhận lệnh; cách khối trên 16px.'),
    ('.arg-trade--lite .arg-lite__group', 'l', 'Lite: chip Sàn, TC, Trần cho giá; 25%, 50%, 75%, Tối đa cho KL.'),
    TAB,
]

ORDERBOOK = [
    ('[data-ob-select]', 'r', 'Nút chữ: bật chọn nhiều lệnh (đổi thành Xong); nhấn giữ một lệnh cũng bật. Chỉ dùng cho tab Sổ lệnh, ẩn khi xem Lịch sử lệnh.'),
    ('.arg-orderbook__tabbed > .arg-tabs', 'l', 'Tabs --lg (Title 3 đậm, cao 48px, gạch chân gradient): Sổ lệnh và Lịch sử lệnh. Màn con của Giao dịch nên ẩn hẳn thanh tab dưới (không để thanh tab không chọn mục nào), Quay lại về Giao dịch.'),
    ('.arg-orderbook__search', 'l', 'Input có icon: lọc ngay khi gõ.'),
    ('.arg-orderbook__chips', 'r', 'Chip tabs --sm: lọc trạng thái, kèm số lệnh, cuộn ngang.'),
    ('.arg-orderbook__head .arg-tabs', 'l', 'Tabs --pill: lọc Tất cả, Mua, Bán.'),
    ('.arg-orderrow', 'r', 'Order row: viền và nền chuyển màu 5% theo chiều lệnh, đệm 12px, bấm mở chi tiết lệnh.'),
    ('.arg-orderrow__bar', 'l', 'Thanh tiến độ khớp: cao 3px, sát đáy thẻ (cắt theo bo góc). --v = khối lượng khớp / khối lượng đặt (%). Màu theo chiều lệnh (Mua, Bán), phần chưa khớp nền 14%. Ẩn ở lệnh đã huỷ.'),
    ('.arg-orderhist__bar', 'l', 'Hàng công cụ duy nhất của tab: Select (158px) chọn 7 ngày, 30 ngày (mặc định), 3 tháng, Tuỳ chọn và nút Bộ lọc (Button --outline2); cao 40px, cách nhau 12px. Tuỳ chọn hiện hai ô ngày (Datepicker).'),
    ('.arg-orderhist__filter', 'r', 'Button --outline2 (chữ trung tính) mở Offcanvas bottom: hai nhóm cách nhau bằng đường kẻ, nhãn nhóm Body 3 đậm, radio (Checkbox kiểu radio) xếp hai cột: Trạng thái (Tất cả, Đã khớp, Khớp một phần, Đã huỷ, Từ chối) và Chiều lệnh (Tất cả, Mua, Bán). Chọn là lọc ngay; số lệnh kết quả chỉ ghi ở nút chính "Xem n lệnh". Có lọc đang bật thì viền màu link và badge đếm.'),
    ('.arg-orderhist__sum', 'l', 'Statrow trong thẻ nền lv-3, bo 13px: giá trị mua khớp và bán khớp (đồng); tính lại theo khoảng thời gian và bộ lọc đang chọn.'),
    ('.arg-orderhist__date', 'r', 'Tiêu đề ngày (Body 4 đậm) kèm số lệnh trong ngày; ngày không còn lệnh sau khi lọc thì ẩn.'),
    ('.arg-orderhist .arg-orderrow', 'l', 'Order row dùng lại: không ô chọn, không thanh tiến độ; lệnh bị từ chối ghi lý do ngắn thay số khớp. Bấm mở chi tiết lệnh (không huỷ, không sửa được).'),
]

ORDERDETAIL = [
    ('.arg-orderdetail__head', 'r', 'Đầu màn: Lệnh mua / bán theo token Mua, Bán, Badge trạng thái, mã Title 1.'),
    ('.arg-kv', 'l', 'Kv --lines: hàng cao tối thiểu 44px, kẻ ngăn.'),
    ('.arg-actionbar', 'r', 'Action bar --fixed: Huỷ lệnh (có xác nhận) và Sửa lệnh. Sửa lệnh chỉ bật với lệnh LO còn hiệu lực (Chờ khớp, Khớp một phần), mở màn Sửa lệnh; lệnh MP, ATO, ATC không sửa được nên nút bị khoá.'),
]


SEARCH = [
    ('.arg-search__bar', 'l', 'Appbar --sticky + Input có icon: quay lại và ô tìm; mở màn là tự đặt con trỏ, bàn phím chữ trượt lên; nút × chỉ hiện khi có chữ.'),
    ('.arg-search__recent .arg-search__head', 'r', 'Tìm gần đây: tiêu đề Title 3 và nút thùng rác 24px xoá cả danh sách.'),
    ('.arg-search__recent .arg-search__list', 'l', 'Dòng 44px: icon kính lúp, mã đậm; bấm điền vào ô, nút × bên phải xoá dòng.'),
    ('.arg-search__results', 'r', 'Kết quả: Quote __id (mã, tên) và ngôi sao .arg-fav 28px (đang theo dõi: vàng --arg-p-brand-yellow); lọc theo mã hoặc tên, bỏ dấu.'),
]


ASSET = [
    ('.arg-acctsel', 'l', 'Acctsel + Dropdown: chọn tiểu khoản; màn mở sẵn tiểu khoản ký quỹ.'),
    ('.arg-tabs--lg', 'r', 'Tabs --lg: 4 tab Tài sản, Danh mục, Lãi lỗ, Sao kê tiền, cuộn ngang; cùng kiểu tab của màn Thị trường.'),
    ('.arg-assetcard', 'l', 'Assetcard: tổng tài sản Header 3; nút mắt ẩn mọi số có data-arg-secret trong tab.'),
    ('.arg-metric-row', 'r', 'Metric: 4 thẻ 2 cột; lãi xanh, lỗ đỏ theo token giao dịch.'),
    ('.arg-debtcard', 'l', 'Debtcard: nền, viền màu lỗi 8% và 24%; nút Trả nợ Button primary xl.'),
    ('.arg-donut', 'r', 'Donut: cổ phiếu và tiền; phần lớn nhất giữa vòng, màu --arg-viz. Rê chuột hoặc nhấn giữ 250ms một cung: cung phóng to 7%, cung khác mờ, giữa vòng hiện số liệu của cung.'),
    ('.arg-breakdown', 'l', 'Breakdown: dòng tổng, thanh 8px chia đoạn, chấm màu; dòng có mũi tên mở thành phần con (Collapse).'),
    ('.arg-asset-actions', 'r', 'Rút tiền (Button outline xl) và Nộp tiền (primary xl) chia đôi hàng.'),
    ('.arg-kv--lines', 'l', 'Kv --lines: dư nợ margin, hàng 44px; Tổng nợ trong ngày màu giảm.'),
    ('.arg-plchart', 'r', 'Plchart: trên đường 0 màu tăng, dưới màu giảm; tooltip khi rê chuột hoặc chạm giữ 250ms.'),
    ('.arg-stmt', 'l', 'Statement: ngày, loại giao dịch, các khoản; bản tiền có mũi tên mở phí và thuế.'),
]

MODIFY = [
    ('.arg-appbar__title', 'r', 'Appbar --sticky: tiêu đề Sửa lệnh, mũi tên quay lại chi tiết lệnh. Ghi chú: chỉ lệnh "LO" được sửa; lệnh "MP", "ATO", "ATC" không thể sửa.'),
    ('.arg-symbol', 'l', 'Tabs --pill: Lite (Bid / Ask gọn một cột) hoặc Pro (đủ sổ lệnh); giá, khối lượng đã sửa giữ nguyên khi đổi chế độ.'),
    ('.arg-pricehead', 'r', 'Pricehead --lg: giá khớp của mã, màu theo biến động; Thông tin CP mở trang mã.'),
    ('.arg-bidask, .arg-trade--pro .arg-book', 'l', 'Lite: Bid / Ask nằm ngang, 3 mức giá tốt nhất mỗi bên kèm tổng khối lượng và tỷ lệ. Pro: Book 3 mức, hoặc danh sách mức giá.'),
    ('.arg-trade--pro .arg-locked', 'r', 'Chiều lệnh (Side) và Loại lệnh (Selectsheet) bị khoá: mờ 60%, không bấm được. Chỉ lệnh LO sửa được, nên loại lệnh luôn là LO.'),
    ('.arg-trade--lite .arg-locked', 'r', 'Chiều lệnh (Side) và Loại lệnh (Selectsheet) bị khoá: mờ 60%, không bấm được. Chỉ lệnh LO sửa được, nên loại lệnh luôn là LO.'),
    ('.arg-trade--pro [data-arg-field="price"]', 'r', 'Stepper giá: bước HOSE 0,01 / 0,05 / 0,10, bắt đầu từ giá lệnh gốc. Gõ số có dấu phẩy, bàn phím giả hiện lên.'),
    ('.arg-trade--lite [data-arg-field="price"]', 'r', 'Stepper giá: bước HOSE 0,01 / 0,05 / 0,10, bắt đầu từ giá lệnh gốc. Gõ số có dấu phẩy, bàn phím giả hiện lên.'),
    ('.arg-trade--pro [data-arg-field="qty"]', 'r', 'Stepper khối lượng: bước 100, bắt đầu từ khối lượng lệnh gốc; giá trị ước tính tính lại = giá × KL × 1.000.'),
    ('.arg-trade--lite [data-arg-field="qty"]', 'r', 'Stepper khối lượng: bước 100, bắt đầu từ khối lượng lệnh gốc; giá trị ước tính tính lại = giá × KL × 1.000.'),
    ('[data-om-submit]', 'l', 'Button --primary --xl: khoá cho đến khi giá hoặc khối lượng khác lệnh gốc. Bấm mở hộp xác nhận Sửa lệnh (giá, KL, loại lệnh, giá trị ước tính), Xác nhận sửa thì báo thành công.'),
]

MORE = [
    ('.arg-profile', 'l', 'Profile: thẻ nền cam nhạt 8%, avatar tròn 56px gradient thương hiệu, tên Title 2 đậm, số tài khoản; hình chìm .arg-brandmark--soft. Họ tên là dữ liệu mẫu.'),
    ('.arg-navlist', 'r', 'Navlist: hàng cao tối thiểu 56px, ô icon 40px nền cam nhạt 12%, nhãn Body 3 vừa, mũi tên; đường kẻ --arg-ui-divider-separator. Mục có data-arg-go mở màn tương ứng, mục còn lại là giữ chỗ.'),
    ('.arg-navlist__item--danger', 'l', 'Navlist --danger: Đăng xuất, cố ý không nổi bật: icon 20px không ô nền, chữ màu lỗi (--arg-action-noti-toast-error), không mũi tên.'),
    ('.arg-brandsign', 'r', 'Brandsign: chữ ký thương hiệu cuối màn, logo cao 40px, tên Agriseco, dòng phụ.'),
    TAB,
]

SERVICES = [
    ('.arg-svcedit__hint', 'r', 'Hướng dẫn và bộ đếm "Đã chọn n/6": tối đa 6 dịch vụ, bằng số ô của lưới Trang chủ.'),
    ('.arg-svcedit__tile', 'l', 'Thẻ dịch vụ nhanh (Svcedit): icon gradient dịch vụ 48px, nhãn; giữ và kéo (cảm ứng giữ 250ms) để đổi vị trí bằng Reorder dạng lưới.'),
    ('.arg-svcedit__remove', 'r', 'Nút bỏ: tròn 20px nền đỏ (token lỗi), icon trừ trắng; bỏ dịch vụ khỏi dịch vụ nhanh.'),
    ('.arg-svcedit__list', 'l', 'Danh sách theo nhóm: thẻ nền xám bo --arg-radius-lg, dòng cao 56px, đường kẻ nhạt bắt đầu từ chữ; icon gradient dịch vụ 32px.'),
    ('.arg-svcedit__add', 'r', 'Nút thêm: icon plus-circle màu thương hiệu; màu disable nhạt khi đã đủ 6 dịch vụ; dịch vụ đã chọn không hiện nút.'),
    ('[data-svc-save]', 'l', 'Button --primary --xl: lưu thứ tự vào phiên (sessionStorage), quay lại Trang chủ và báo toast một dòng.'),
]


def specs_for(sid):
    """Danh sách đặc tả của màn hình có id sid."""
    if sid == 'home': return HOME
    if sid == 'market': return MARKET
    if sid == 'more': return MORE
    if sid == 'services': return SERVICES
    if sid == 'orderbook': return ORDERBOOK
    if sid == 'search': return SEARCH
    if sid == 'asset': return ASSET
    if sid.startswith('order-'): return ORDERDETAIL
    if sid.startswith('modify-'): return MODIFY
    if sid == 'trade' or sid.startswith('trade-'): return TRADE
    if sid.startswith('stock-'): return STOCK
    if sid.startswith('idx-'): return INDEX
    if sid.startswith('theme-'): return THEME
    return []
