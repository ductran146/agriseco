"""Markup cho màn Giao dịch (đặt lệnh cổ phiếu cơ sở), dựng từ component ARG:
acctsel, symbol, pricehead, statrow, book, side, stepper, kv. Dùng chung cho ví dụ trong ui/components/* và pages/build_pages.py.
Các hàm theo mã nhận một stocks.Stock (mặc định VCB: sàn HOSE, tham chiếu 92,10, trần 98,50, sàn 85,70). Dữ liệu mẫu trong stocks.py."""
import random
from detail_parts import vn
from stocks import VCB, BUYING_POWER

num = lambda n: f'{n:,}'.replace(',', '.')
I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'

SYMBOL = 'VCB'


# Tiểu khoản mẫu của tài khoản 039C101991 (số tài khoản và loại là dữ liệu mẫu)
ACCOUNTS = [('039C101991 - 01', 'Chứng khoán cơ sở'), ('039C101991 - 02', 'Ký quỹ'), ('039C101991 - 03', 'Phái sinh'),
            ('039C101991 - 05', 'Chứng khoán cơ sở'), ('039C101991 - 06', 'Tài khoản ảo')]


def acctsel(accounts=ACCOUNTS):
    """Nút chọn tiểu khoản trên thanh đầu: dòng trên là số tiểu khoản kèm mũi tên, dòng dưới là loại. Bấm xổ danh sách toàn chiều ngang
    liền với thanh đầu (mỗi hàng: số tiểu khoản, loại ở dòng dưới, hàng đang chọn nền xám); chọn thì đổi số và loại trên nút (Dropdown)."""
    no, kind = accounts[0]
    items = ''.join(f'<button class="arg-menu__item" role="menuitemradio" aria-checked="{"true" if i == 0 else "false"}" type="button" data-no="{n}" data-type="{k}"><b>{n}</b><span>{k}</span></button>' for i, (n, k) in enumerate(accounts))
    return (f'<div class="arg-dropdown" data-arg-dropdown data-arg-acct-menu><button class="arg-acctsel" type="button" aria-haspopup="menu" aria-expanded="false" aria-label="Đổi tiểu khoản, đang chọn {no} - {kind}">'
            f'<span class="arg-acctsel__row"><b class="arg-acctsel__no">{no}</b>{I("caret-down")}</span><span class="arg-acctsel__type">{kind}</span></button>'
            f'<div class="arg-menu" role="menu" hidden>{items}</div></div>')


def mode_switch(first='Lite', second='Pro'):
    """Công tắc hai chế độ hiển thị, dùng Tabs --pill."""
    return (f'<div class="arg-tabs arg-tabs--pill" data-arg-tabs data-arg-modes><div class="arg-tablist" role="tablist" aria-label="Chế độ hiển thị">'
            f'<button class="arg-tab" role="tab" type="button" data-mode="lite" aria-selected="false">{first}</button>'
            f'<button class="arg-tab" role="tab" type="button" data-mode="pro" aria-selected="true">{second}</button></div></div>')


def symbol(code=SYMBOL, ex='HOSE', right=None):
    return (f'<div class="arg-symbol"><span class="arg-symbol__search">{I("magnifying-glass")}</span><b class="arg-symbol__code">{code}</b>'
            f'<span class="arg-badge">{ex}</span>{right if right is not None else mode_switch()}</div>')


def quote_head(st=VCB):
    """Giá khớp lớn kèm thay đổi và liên kết thông tin cổ phiếu (mở trang thông tin của mã)."""
    ic = {'up': 'caret-up-fill', 'down': 'caret-down-fill', 'ref': 'minus'}[st.kind]
    return (f'<div class="arg-pricehead arg-pricehead--lg arg-pricehead--{st.kind}"><div class="arg-pricehead__row">'
            f'<div class="arg-pricehead__main"><b class="arg-pricehead__value">{vn(st.last)}</b>'
            f'<span class="arg-pricehead__change"><span>{I(ic)}{vn(abs(st.chg))}</span><span class="arg-badge arg-badge--{st.kind}">{vn(st.pct, 2, True)}%</span></span></div>'
            f'<a class="arg-btn arg-btn--text arg-btn--sm" href="#" data-arg-go="{st.id}">Thông tin CP{I("caret-right")}</a></div></div>')


def statrow(items):
    """items: [(nhãn, giá trị, lớp màu)]"""
    return '<dl class="arg-statrow">' + ''.join(f'<div class="arg-statrow__item"><dt>{l}</dt><dd{f" class=\"{c}\"" if c else ""}>{v}</dd></div>' for l, v, c in items) + '</dl>'


def stats(st=VCB):
    return statrow([('KL', num(st.vol), ''), ('TC', vn(st.ref), 'arg-ref'), ('Mở', vn(st.open), st.cls(st.open)), ('Cao', vn(st.high), st.cls(st.high)), ('Thấp', vn(st.low), st.cls(st.low))])


def view_switch(st=VCB):
    """Công tắc kiểu sổ lệnh: độ sâu (3 mức, có thanh khối lượng) hoặc danh sách (6 mức mỗi bên, tổng khối lượng, tỷ lệ mua bán)."""
    return ('<div class="arg-tabs arg-tabs--pill arg-tabs--fill" data-arg-tabs><div class="arg-tablist" role="tablist" aria-label="Kiểu sổ lệnh">'
            f'<button class="arg-tab" role="tab" type="button" aria-selected="true" aria-label="Độ sâu">{I("chart-bar-horizontal")}</button>'
            f'<button class="arg-tab" role="tab" type="button" aria-selected="false" aria-label="Danh sách">{I("list-bullets")}</button></div>'
            f'<div class="arg-tabpanel" role="tabpanel">{book(st)}{book_more()}</div>'
            f'<div class="arg-tabpanel" role="tabpanel" hidden>{book_list(st)}</div></div>')


def levels(st=VCB, n=6):
    """n mức bán (giá tăng dần từ mức tốt nhất) và n mức mua (giá giảm dần), trong khoảng sàn trần. 3 mức đầu lấy từ dữ liệu mã, các mức xa sinh theo mã."""
    r = random.Random('book-' + st.code)
    asks, bids = list(st.asks), list(st.bids)
    while len(asks) < n and asks[-1][0] + st.step <= st.ceil + 1e-9: asks.append((round(asks[-1][0] + st.step, 2), r.randint(40, 600) * 100))
    while len(bids) < n and bids[-1][0] - st.step >= st.floor - 1e-9: bids.append((round(bids[-1][0] - st.step, 2), r.randint(40, 600) * 100))
    return asks, bids


def book_list(st=VCB, n=6):
    """Danh sách mức giá: n mức bán (giá cao xuống) rồi n mức mua (giá cao xuống) trong vùng cuộn nội bộ, kèm Tổng KL và tỷ lệ mua bán."""
    asks, bids = levels(st, n)
    row = lambda p, v: f'<div class="arg-book__li"><span class="{st.cls(p)}">{vn(p)}</span><span>{num(v)}</span></div>'
    sa, sb = sum(v for _, v in asks), sum(v for _, v in bids)
    pb = round(sb / (sa + sb) * 100)
    return ('<div class="arg-book arg-book--list" role="table" aria-label="Danh sách mức giá">'
            '<div class="arg-book__head"><span>Giá</span><span>KL</span></div>'
            f'<div class="arg-book__scroll" data-arg-book-center data-asks="{len(asks)}" tabindex="0" aria-label="Các mức giá, cuộn để xem thêm">'
            + ''.join(row(p, v) for p, v in reversed(asks)) + ''.join(row(p, v) for p, v in bids) + '</div>' +
            f'<div class="arg-book__total"><span>Tổng KL</span><b>{num(sa + sb)}</b></div>'
            f'<div class="arg-book__ratio" style="--v:{pb}" role="img" aria-label="Mua {pb}%, bán {100 - pb}%"><div class="arg-book__ratio-bar"></div>'
            f'<span class="arg-buy">{pb}%</span><span class="arg-sell">{100 - pb}%</span></div></div>')


def book(st=VCB):
    """Sổ lệnh 3 mức giá tốt nhất như bảng giá HOSE: dư bán (giá cao xuống) trên, dư mua dưới. Thanh nền theo khối lượng lớn nhất mỗi bên."""
    ma, mb = max(v for _, v in st.asks), max(v for _, v in st.bids)
    row = lambda k, p, v, m: f'<div class="arg-book__row arg-book__row--{k}" style="--w:{round(v / m * 100)}"><span class="arg-book__price {st.cls(p)}">{vn(p)}</span><span class="arg-book__vol">{num(v)}</span></div>'
    return ('<div class="arg-book" role="table" aria-label="Sổ lệnh">'
            f'<div class="arg-book__limit arg-book__limit--ceil"><span>Trần</span><b>{vn(st.ceil)}</b></div>'
            + ''.join(row('ask', p, v, ma) for p, v in reversed(st.asks)) + ''.join(row('bid', p, v, mb) for p, v in st.bids) +
            f'<div class="arg-book__limit arg-book__limit--floor"><span>Sàn</span><b>{vn(st.floor)}</b></div></div>')


def book_more():
    return f'<button class="arg-book__more" type="button" data-arg-open="ord-depth">Xem đầy đủ{I("arrow-square-out")}</button>'


def side():
    return ('<div class="arg-side" role="group" aria-label="Chiều lệnh">'
            '<button class="arg-side__btn arg-side__btn--buy" type="button" aria-pressed="true">Mua</button>'
            '<button class="arg-side__btn arg-side__btn--sell" type="button" aria-pressed="false">Bán</button></div>')


def stepper(label, step, dec, value='', field='', short=None):
    return (f'<div class="arg-control arg-stepper" data-step="{step}" data-dec="{dec}"{f" data-arg-field=\"{field}\"" if field else ""}><span class="arg-control__label">{short or label}</span>'
            f'<button class="arg-icon-btn" type="button" data-arg-step="-1" aria-label="Giảm {label.lower()}">{I("minus")}</button>'
            f'<input class="arg-input" inputmode="{'decimal' if dec else 'numeric'}" aria-label="{label}" value="{value}">'
            f'<button class="arg-icon-btn" type="button" data-arg-step="1" aria-label="Tăng {label.lower()}">{I("plus")}</button></div>')


def order_type():
    """Ô chọn loại lệnh: trông như Select, bấm mở bảng trượt từ dưới lên (component selectsheet, bảng ở type_sheet)."""
    return ('<div class="arg-control arg-select arg-select--center arg-selectsheet"><span class="arg-control__label">Loại</span><select class="arg-select-native" tabindex="-1" aria-label="Loại lệnh" aria-hidden="true">'
            '<option>LO</option><option>MP</option><option>ATO</option><option>ATC</option></select>' + I('caret-down')
            + '<button class="arg-selectsheet__hit" type="button" data-arg-open="ord-type" data-label="Loại lệnh" aria-haspopup="dialog" aria-label="Loại lệnh, đang chọn LO"></button></div>')


TYPES = [('LO', 'Lệnh giới hạn (LO)', 'Khớp tại mức giá đã chọn hoặc tốt hơn'), ('MP', 'Lệnh thị trường (MP)', 'Khớp ngay tại giá thị trường tốt nhất hiện có'),
         ('ATO', 'Lệnh xác định giá mở cửa (ATO)', 'Khớp tại giá có khối lượng khớp lớn nhất trong phiên xác định giá mở cửa'),
         ('ATC', 'Lệnh xác định giá đóng cửa (ATC)', 'Khớp tại giá có khối lượng khớp lớn nhất trong phiên xác định giá đóng cửa')]


def type_sheet():
    """Bảng chọn loại lệnh cổ phiếu cơ sở trên HOSE (LO, MP, ATO, ATC), mỗi mục kèm mô tả."""
    rows = ''.join(f'<button class="arg-optrow" type="button" role="radio" aria-checked="{"true" if v == "LO" else "false"}" data-value="{v}"><span class="arg-optrow__txt"><b>{t}</b><span>{d}</span></span>'
                   f'<span class="arg-optrow__tick">{I("check")}</span></button>' for v, t, d in TYPES)
    return (f'<div class="arg-offcanvas-wrap" id="ord-type" hidden data-arg-offcanvas data-arg-selectsheet><aside class="arg-offcanvas arg-offcanvas--bottom arg-offcanvas--auto" role="dialog" aria-modal="true" aria-labelledby="ord-type-t">'
            f'<div class="arg-modal__header"><h4 class="arg-modal__title" id="ord-type-t">Loại lệnh</h4><button class="arg-icon-btn" type="button" data-arg-close aria-label="Đóng">{I("x", "i--20")}</button></div>'
            f'<div class="arg-modal__body arg-optlist" role="radiogroup" aria-label="Loại lệnh">{rows}</div></aside></div>')


def _kv(st, margin=True):
    return ('<dl class="arg-kv"><div class="arg-kv__row"><dt>Sức mua<button class="arg-icon-btn" type="button" aria-label="Giải thích sức mua">' + I('info') + f'</button></dt><dd>{num(BUYING_POWER)}</dd></div>'
            + ('<div class="arg-kv__row"><dt>Tỷ lệ ký quỹ</dt><dd>50%</dd></div>' if margin else '') +
            f'<div class="arg-kv__row"><dt>KL mua tối đa</dt><dd>{num(st.max_qty)}</dd></div>'
            f'<div class="arg-kv__row arg-kv__row--total"><dt>Giá trị ước tính</dt><dd data-arg-order-total>{num(round(st.last * 100 * 1000))}</dd></div></dl>')


def _step(st):
    return f'{st.step:g}'


def order_fields(st=VCB):
    return side() + order_type() + stepper('Giá', _step(st), 2, vn(st.last), 'price') + stepper('Khối lượng', '100', 0, '100', 'qty', short='KL') + _kv(st)


def order_panel(st=VCB):
    """Form đặt lệnh vừa một màn: sổ lệnh bên trái, trường nhập bên phải, nút đặt lệnh ở đáy."""
    return (f'<form class="arg-order" data-arg-order data-side="buy" data-symbol="{st.code}" onsubmit="return false">'
            f'<div class="arg-split"><div>{view_switch(st)}</div><div>{order_fields(st)}</div></div>'
            f'<button class="arg-btn arg-btn--buy arg-btn--xl arg-btn--block" type="button" data-arg-order-cta>Mua - {st.code}</button></form>')


def order_modals():
    """Hộp xác nhận lệnh và hộp báo đặt lệnh thành công của màn Giao dịch (component ordermodal)."""
    return ORDER_MODALS


ORDER_MODALS = '''<div class="arg-overlay" id="ord-confirm" hidden data-arg-modal data-arg-confirm>
  <div class="arg-modal arg-modal--sm arg-ordermodal" role="alertdialog" aria-modal="true" aria-labelledby="ord-confirm-t">
    <div class="arg-modal__header"><h4 class="arg-modal__title" id="ord-confirm-t" data-ord="title">Xác nhận lệnh mua</h4></div>
    <div class="arg-modal__body"><dl class="arg-kv arg-kv--lines">
      <div class="arg-kv__row"><dt>Mã</dt><dd data-ord="symbol">VCB</dd></div>
      <div class="arg-kv__row"><dt>Loại lệnh</dt><dd data-ord="type">LO</dd></div>
      <div class="arg-kv__row"><dt>Giá</dt><dd data-ord="price">91,80</dd></div>
      <div class="arg-kv__row"><dt>Khối lượng</dt><dd data-ord="qty">100</dd></div>
      <div class="arg-kv__row"><dt>Giá trị ước tính</dt><dd data-ord="value">9.180.000</dd></div>
    </dl></div>
    <div class="arg-modal__footer arg-ordermodal__actions"><button class="arg-btn arg-btn--tertiary arg-btn--xl" type="button" data-arg-close>Huỷ</button><button class="arg-btn arg-btn--buy arg-btn--xl" type="button" data-arg-confirm-ok data-ord="ok">Mua</button></div>
  </div>
</div>
<div class="arg-overlay arg-overlay--blur" id="ord-done" hidden data-arg-modal data-arg-done>
  <div class="arg-modal arg-modal--sm arg-ordermodal arg-ordermodal--done" role="dialog" aria-modal="true" aria-labelledby="ord-done-t">
    <div class="arg-modal__body">
      <span class="arg-modal__icon arg-modal__icon--success arg-modal__icon--lg"><i data-arg-icon="seal-check"></i></span>
      <h4 class="arg-modal__title" id="ord-done-t">Đặt lệnh thành công</h4>
      <span data-ord="done">Lệnh của bạn đã được gửi. Bạn có thể xem trạng thái lệnh tại Sổ lệnh.</span>
    </div>
    <div class="arg-modal__footer arg-ordermodal__actions arg-ordermodal__actions--stack"><button class="arg-btn arg-btn--tertiary arg-btn--xl" type="button" data-arg-go="orderbook" data-arg-close>Sổ lệnh</button><button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-arg-close>Đặt lệnh khác</button></div>
  </div>
</div>'''


def chip_row(items, attr):
    """Hàng chip hành động (không phải tab): items = [(nhãn, giá trị)], attr = tên thuộc tính data."""
    b = ''.join(f'<button class="arg-chip-tab" type="button" {attr}="{v}">{l}</button>' for l, v in items)
    return f'<div class="arg-chip-tabs arg-chip-tabs--sm arg-chip-tabs--fill"><div class="arg-chip-tabs__list">{b}</div></div>'


def lite_panel(st=VCB):
    """Chế độ Lite: đặt lệnh nhanh, không sổ lệnh. Chọn nhanh giá Sàn, TC, Trần và khối lượng theo % sức mua."""
    return (f'<form class="arg-order arg-lite" data-arg-order data-side="buy" data-symbol="{st.code}" data-max-qty="{st.max_qty}" onsubmit="return false">' + side() +
            '<div class="arg-lite__group">' + stepper('Giá', _step(st), 2, vn(st.last), 'price') + chip_row([(f'Sàn {vn(st.floor)}', vn(st.floor)), (f'TC {vn(st.ref)}', vn(st.ref)), (f'Trần {vn(st.ceil)}', vn(st.ceil))], 'data-arg-set') + '</div>'
            '<div class="arg-lite__group">' + stepper('Khối lượng', '100', 0, '100', 'qty', short='KL') + chip_row([('25%', 25), ('50%', 50), ('75%', 75), ('Tối đa', 100)], 'data-arg-qty-pct') + '</div>'
            + _kv(st, margin=False) +
            f'<button class="arg-btn arg-btn--buy arg-btn--xl arg-btn--block" type="button" data-arg-order-cta>Mua - {st.code}</button></form>')


def depth_sheet(st=VCB, n=10):
    """Bảng trượt từ dưới lên: bước giá đầy đủ (n mức mỗi bên) dạng dư mua trái, dư bán phải, kèm Sàn và Trần (component depth trong offcanvas)."""
    import stock_parts as SP
    asks, bids = levels(st, n)
    return (f'<div class="arg-offcanvas-wrap" id="ord-depth" hidden data-arg-offcanvas><aside class="arg-offcanvas arg-offcanvas--bottom arg-offcanvas--auto" role="dialog" aria-modal="true" aria-labelledby="ord-depth-t">'
            f'<div class="arg-modal__header"><h4 class="arg-modal__title" id="ord-depth-t">Bước giá {st.code}</h4><button class="arg-icon-btn" type="button" data-arg-close aria-label="Đóng">{I("x", "i--20")}</button></div>'
            f'<div class="arg-modal__body">{SP.depth(st, bids, asks, limits=True)}</div></aside></div>')
