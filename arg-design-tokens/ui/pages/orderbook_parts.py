"""Markup cho màn Sổ lệnh (component orderrow, orderbook, chip-tab, tabs, input, checkbox, actionbar, modal, badge, kv).
Dữ liệu mẫu: lệnh trong ngày 29/10/2026 của tiểu khoản 039C101991 - 01; giá bám bảng giá mẫu (VCB 91,80, AGR 19,75, HPG 27,10...), bước giá HOSE 0,01 / 0,05 / 0,10."""
from detail_parts import vn
from trade_parts import acctsel

num = lambda n: f'{n:,}'.replace(',', '.')
I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'

# (mã lệnh, giờ, mã CK, chiều, loại, giá (None = thị trường), khối lượng, đã khớp, giá khớp TB, trạng thái)
ORDERS = [
    ('LD-290001', '10:42:15', 'VCB', 'buy', 'LO', 91.80, 1000, 600, 91.80, 'partial'),
    ('LD-290002', '10:30:02', 'AGR', 'sell', 'LO', 19.80, 5000, 0, 0, 'pending'),
    ('LD-290003', '10:15:44', 'HPG', 'buy', 'LO', 27.10, 2000, 2000, 27.10, 'matched'),
    ('LD-290004', '10:05:09', 'CTG', 'buy', 'LO', 35.00, 1500, 0, 0, 'pending'),
    ('LD-290005', '09:48:20', 'BID', 'sell', 'MP', None, 800, 800, 40.10, 'matched'),
    ('LD-290006', '09:41:55', 'MSN', 'buy', 'LO', 68.50, 300, 0, 0, 'pending'),
    ('LD-290007', '09:30:12', 'NVL', 'sell', 'LO', 14.90, 3000, 3000, 14.95, 'matched'),
    ('LD-290008', '09:20:47', 'VIC', 'buy', 'LO', 41.00, 1000, 0, 0, 'cancelled'),
]
STATUS = {'pending': ('Chờ khớp', 'yellow'), 'partial': ('Khớp một phần', 'blue'), 'matched': ('Đã khớp', 'success'), 'cancelled': ('Đã huỷ', '')}
CHIPS = [('all', 'Tất cả'), ('pending', 'Chờ khớp'), ('partial', 'Khớp một phần'), ('matched', 'Đã khớp'), ('cancelled', 'Đã huỷ')]


def order_id(o):
    return 'order-' + o[0].lower()


def order_li(o):
    oid, time, code, side, typ, px, qty, matched, avg, status = o
    label, badge = STATUS[status]
    cancel = status in ('pending', 'partial')
    pct = round(matched / qty * 100)
    side_tag = 'M' if side == 'buy' else 'B'
    return (f'<li class="arg-orderrow" data-side="{side}" data-status="{status}" data-code="{code}"{" data-cancelable" if cancel else ""}>'
            + (f'<label class="arg-check arg-orderrow__pick"><input type="checkbox" aria-label="Chọn lệnh {"mua" if side == "buy" else "bán"} {code}"><span class="box">{I("check")}</span></label>' if cancel else '')
            + f'<a class="arg-orderrow__main" href="#" data-arg-go="{order_id(o)}" aria-label="Xem chi tiết lệnh {"mua" if side == "buy" else "bán"} {code}"><span class="arg-orderrow__side">{side_tag}</span><span class="arg-orderrow__id"><b>{code}</b><span>{time[:5]} · {typ}</span></span>'
            f'<span class="arg-badge{" arg-badge--" + badge if badge else ""}">{label}</span><span class="arg-orderrow__px">{vn(px) if px else "Thị trường"}<span> × {num(qty)}</span></span>'
            f'<span class="arg-orderrow__fill">Khớp <b>{num(matched)}</b>/{num(qty)}</span><span class="arg-orderrow__go">{I("caret-right")}</span></a>'
            + (f'<div class="arg-orderrow__bar" style="--v:{pct}"></div>' if status != 'cancelled' else '') + '</li>')


def detail_screen(o):
    """Màn chi tiết một lệnh: chiều lệnh, trạng thái, mã, các dòng thông tin; chân màn có Huỷ lệnh (nếu còn huỷ được) và Sửa lệnh."""
    from stocks import BY_CODE
    oid, time, code, side, typ, px, qty, matched, avg, status = o
    label, badge = STATUS[status]
    cancel = status in ('pending', 'partial')
    st = BY_CODE[code]
    price = px if px else avg
    value = round(price * qty * 1000)
    fee = round(value * 0.0015)
    kv = lambda k, v, extra='': f'<div class="arg-kv__row"><dt>{k}{extra}</dt><dd>{v}</dd></div>'
    info = f'<button class="arg-icon-btn" type="button" aria-label="Giải thích phí giao dịch">{I("info")}</button>'
    rows = (kv('Số hiệu lệnh', oid) + kv('Thời gian', time) + kv('Loại lệnh', typ) + kv('Giá đặt', vn(px) if px else 'Thị trường') + kv('Giá khớp trung bình', vn(avg) if matched else '-')
            + kv('Khối lượng đặt', num(qty)) + kv('Khối lượng khớp', num(matched) if matched else '-') + kv('Giá trị ước tính', num(value)) + kv('Phí giao dịch ước tính', num(fee), info))
    edit = typ == 'LO' and cancel  # chỉ lệnh LO còn hiệu lực sửa được
    bar = ((f'<button class="arg-btn arg-btn--outline arg-btn--xl" type="button" data-od-cancel>Huỷ lệnh</button>' if cancel else '')
           + (f'<button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-arg-go="modify-{oid.lower()}">Sửa lệnh</button>' if edit
              else '<button class="arg-btn arg-btn--primary arg-btn--xl" type="button" disabled>Sửa lệnh</button>'))
    return f'''<div class="arg-screen arg-screen--plain" data-arg-screen="{order_id(o)}" data-arg-orderdetail hidden>
<header class="arg-appbar arg-appbar--sticky"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I('caret-left')}</button><h1 class="arg-appbar__title">Chi tiết lệnh</h1></header>
<main class="arg-page__main arg-page__main--dense">
  <div class="arg-orderdetail__head" data-side="{side}"><div class="arg-orderdetail__row"><span class="arg-orderdetail__side">Lệnh {"mua" if side == "buy" else "bán"}</span><span class="arg-badge{" arg-badge--" + badge if badge else ""}" data-od-badge>{label}</span></div><b class="arg-orderdetail__code">{code}</b></div>
  <dl class="arg-kv arg-kv--lines">{rows}</dl>
</main>
<div class="arg-actionbar arg-actionbar--fixed">{bar}</div>
<div class="arg-overlay" id="od-cancel" hidden data-arg-modal data-od-modal><div class="arg-modal arg-modal--sm" role="alertdialog" aria-modal="true" aria-labelledby="od-cancel-t">
  <div class="arg-modal__body" style="padding-top:var(--arg-space-6x);justify-items:center;text-align:center"><span class="arg-modal__icon">{I('trash')}</span><h4 class="arg-modal__title" id="od-cancel-t">Huỷ lệnh này?</h4><span>Lệnh {"mua" if side == "buy" else "bán"} {code} sẽ bị huỷ và không thể khôi phục.</span></div>
  <div class="arg-modal__footer arg-ordermodal__actions"><button class="arg-btn arg-btn--tertiary arg-btn--xl" type="button" data-arg-close>Giữ lại</button><button class="arg-btn arg-btn--sell arg-btn--xl" type="button" data-od-ok>Huỷ lệnh</button></div></div></div>
</div>'''


def screen(tabbar_html):
    counts = {k: sum(1 for o in ORDERS if k == 'all' or o[9] == k) for k, _ in CHIPS}
    chips = ''.join(f'<button class="arg-chip-tab" type="button" data-ob-status="{k}" aria-pressed="{"true" if k == "all" else "false"}">{t} <span data-ob-n>{counts[k]}</span></button>' for k, t in CHIPS)
    sides = ''.join(f'<button class="arg-tab" role="tab" type="button" data-ob-side="{k}" aria-selected="{"true" if k == "all" else "false"}">{t}</button>' for k, t in (('all', 'Tất cả'), ('buy', 'Mua'), ('sell', 'Bán')))
    return f'''<div class="arg-screen arg-screen--plain" data-arg-screen="orderbook" data-arg-orderbook hidden>
<header class="arg-appbar arg-appbar--sticky" style="justify-content:flex-start;gap:var(--arg-space-2x)"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I('caret-left')}</button>{acctsel()}<button class="arg-btn arg-btn--text" type="button" data-ob-select style="margin-left:auto">Chọn</button></header>
<main class="arg-page__main arg-page__main--dense">
  <div class="arg-orderbook__search"><div class="arg-control">{I('magnifying-glass')}<input class="arg-input" type="search" enterkeyhint="search" placeholder="Tìm mã" aria-label="Tìm mã" data-ob-search></div></div>
  <div class="arg-chip-tabs arg-chip-tabs--sm arg-orderbook__chips"><div class="arg-chip-tabs__list" role="group" aria-label="Trạng thái lệnh">{chips}</div></div>
  <div class="arg-orderbook__head"><span class="arg-orderbook__count" data-ob-count>{len(ORDERS)} lệnh</span><div class="arg-tabs arg-tabs--pill"><div class="arg-tablist" role="tablist" aria-label="Chiều lệnh">{sides}</div></div></div>
  <ul class="arg-orderrow-list">{''.join(order_li(o) for o in ORDERS)}</ul>
  <p class="arg-orderbook__empty" data-ob-empty hidden>Không có lệnh phù hợp.</p>
</main>
{tabbar_html}
<div class="arg-actionbar arg-actionbar--fixed" data-ob-bar><label class="arg-check"><input type="checkbox" data-ob-all aria-label="Chọn tất cả lệnh đang hiện"><span class="box">{I('check')}</span>Tất cả</label><button class="arg-btn arg-btn--sell arg-btn--xl" type="button" data-ob-cancel disabled>Huỷ lệnh</button></div>
<div class="arg-overlay" id="ob-cancel" hidden data-arg-modal data-ob-modal><div class="arg-modal arg-modal--sm" role="alertdialog" aria-modal="true" aria-labelledby="ob-cancel-t">
  <div class="arg-modal__body" style="padding-top:var(--arg-space-6x);justify-items:center;text-align:center"><span class="arg-modal__icon">{I('trash')}</span><h4 class="arg-modal__title" id="ob-cancel-t" data-ob-title>Huỷ lệnh này?</h4><span data-ob-text>Lệnh sẽ bị huỷ và không thể khôi phục.</span></div>
  <div class="arg-modal__footer arg-ordermodal__actions"><button class="arg-btn arg-btn--tertiary arg-btn--xl" type="button" data-arg-close>Giữ lại</button><button class="arg-btn arg-btn--sell arg-btn--xl" type="button" data-ob-ok>Huỷ lệnh</button></div></div></div>
</div>'''
