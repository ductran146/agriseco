"""Markup màn Tài sản (4 tab: Tài sản, Danh mục, Lãi lỗ, Sao kê tiền) cho tiểu khoản ký quỹ 039C101991 - 02.
Dữ liệu mẫu (không phải số thật), thời điểm 10:15 ngày 29/10/2026, mọi con số suy ra từ cùng một bộ khai báo nên khớp nhau:
- Cổ phiếu nắm giữ HPG, VCB, AGR, NVL bám giá trong stocks.py; giá trị cổ phiếu = đang nắm giữ + chờ khớp + quyền chờ về.
- Tiền = tiền có thể rút + lệnh mua chưa khớp + tiền ứng trước khả dụng + tiền đã ứng + khác; số dư cuối kỳ sao kê tiền tại công ty bằng tiền này.
- Tổng tài sản = giá trị cổ phiếu + tiền; tài sản ròng = tổng tài sản - tổng dư nợ.
- Lãi lỗ sao kê = chuỗi ngày sinh theo seed; lãi, lỗ, chênh lệch cộng đúng; phí và thuế bằng khối Phí và thuế của tab Tài sản."""
import ring as RING
import random
from datetime import date, timedelta
from detail_parts import vn
import info_parts as IP
from account_parts import LOGO as _WM
import market_parts as MP
import trade_parts as TP
from stocks import STOCKS, BUYING_POWER

I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'
num = lambda n: f'{round(n):,}'.replace(',', '.')
sgn = lambda n: ('+' if n > 0 else '-' if n < 0 else '') + num(abs(n))
cls = lambda v: 'arg-up' if v > 0 else 'arg-down' if v < 0 else 'arg-ref'
tr = lambda v, sign=False: vn(v / 1e6, 2, sign) + ' tr'
SEC = ' data-arg-secret'

HELD = {'HPG': (3000, 26.00), 'VCB': (500, 90.00), 'AGR': (5000, 18.20), 'NVL': (4000, 15.60)}
BY = {s.code: s for s in STOCKS}
# tiểu khoản ký quỹ đứng đầu (demo chỉ có chứng khoán cơ sở: thường và ký quỹ, không có phái sinh)
ACCOUNTS = [TP.ACCOUNTS[1]] + [a for i, a in enumerate(TP.ACCOUNTS) if i != 1]

# Tiền (đồng): thành phần và thành phần con
CASH = dict(withdraw=18_000_000, buy=12_000_000, adv=(5_000_000, 6_000_000, 4_000_000), cadv=5_000_000, other=(4_000_000, 6_000_000))
UNSETTLED = 7_500_000
PENDING_STOCK, PENDING_RIGHTS = 10_000_000, 3_000_000
DEBT = dict(principal=80_000_000, interest=420_000, overdue=30_000, intra_ok=10_000_000, intra_wait=5_000_000)
FEES = dict(broker=168_000, custody=24_000, tax=120_000)


def figures():
    hold = sum(BY[c].last * q * 1000 for c, (q, _) in HELD.items())
    cost = sum(cv * q * 1000 for q, cv in HELD.values())
    today = sum(BY[c].chg * q * 1000 for c, (q, _) in HELD.items())
    cash = CASH['withdraw'] + CASH['buy'] + sum(CASH['adv']) + CASH['cadv'] + sum(CASH['other'])
    stock = hold + PENDING_STOCK + PENDING_RIGHTS
    total = stock + cash
    intra = DEBT['intra_ok'] + DEBT['intra_wait']
    debt = DEBT['principal'] + DEBT['interest'] + DEBT['overdue'] + intra
    return dict(hold=round(hold), cost=round(cost), unreal=round(hold - cost), unreal_pct=(hold - cost) / cost * 100, today=round(today), today_pct=today / (total - today) * 100,
                cash=cash, stock=round(stock), total=round(total), intra=intra, debt=debt, net=round(total - debt), margin_ratio=(total - debt) / total * 100,
                fee=sum(FEES.values()))


F = figures()


# ---------- khối dùng chung ----------
def mc(label, value, sub='', k='', wide=False):
    return (f'<div class="arg-metric{" arg-metric--" + k if k else ""}{" arg-metric--wide" if wide else ""}"><dt>{label}</dt><dd class="arg-metric__value"{SEC}>{value}</dd>'
            + (f'<dd class="arg-metric__sub">{sub}</dd>' if sub else '') + '</div>')


def kk(v): return 'up' if v > 0 else 'down' if v < 0 else ''


def assetcard(total=None, today=None, today_pct=None):
    total = F['total'] if total is None else total; today = F['today'] if today is None else today; today_pct = F['today_pct'] if today_pct is None else today_pct
    ic = 'trend-up' if today >= 0 else 'trend-down'
    return (f'<section class="arg-assetcard" aria-label="Tổng tài sản">{_WM.replace("arg-account__wm", "arg-assetcard__wm")}<span class="arg-assetcard__label">Tổng tài sản (đ)<button class="arg-icon-btn" type="button" data-arg-asset-eye aria-label="Ẩn số dư">{I("eye-slash", "i--20")}</button></span>'
            f'<b class="arg-assetcard__amount"{SEC}>{num(total)}</b>'
            f'<span class="arg-assetcard__delta">Lãi/lỗ hôm nay {I(ic)}<b class="{cls(today)}"{SEC}>{sgn(today)}</b><b class="{cls(today)}">({vn(today_pct, 2, True)}%)</b></span></section>')


def debtcard(amount=None):
    amount = F['debt'] if amount is None else amount
    return (f'<section class="arg-debtcard" aria-label="Dư nợ margin"><div class="arg-debtcard__row"><span>Dư nợ margin</span><b{SEC}>{num(amount)}</b></div>'
            f'<button class="arg-btn arg-btn--primary arg-btn--xl arg-btn--block" type="button">Trả nợ</button></section>')


def breakdown(head, total, segs, rows, uid):
    """segs: [(giá trị, màu)]; rows: [(nhãn, giá trị, màu, [(nhãn con, giá trị)])]."""
    s = sum(v for v, _ in segs)
    bar = ''.join(f'<li style="--w:{v / s * 100:.2f};--c:{c}"></li>' for v, c in segs)
    items = ''
    for i, (label, val, c, kids) in enumerate(rows):
        tool = sub = ''
        if kids:
            cid = f'{uid}-{i}'
            tool = (f'<button class="arg-icon-btn arg-collapse-toggle" type="button" data-arg-collapse aria-controls="{cid}" aria-expanded="false" aria-label="Xem chi tiết {label}">{I("caret-down", "i--20")}</button>')
            sub = f'<div class="arg-collapse" id="{cid}"><div><ul class="arg-breakdown__sub">' + ''.join(f'<li><span>{k}</span><b{SEC}>{num(v)}</b></li>' for k, v in kids) + '</ul></div></div>'
        items += f'<li><div class="arg-breakdown__row"><i class="arg-breakdown__key" style="--c:{c}"></i><span>{label}</span><b{SEC}>{num(val)}</b>{tool}</div>{sub}</li>'
    return (f'<div class="arg-breakdown"><div class="arg-breakdown__head"><span>{head}</span><b{SEC}>{num(total)}</b></div><ul class="arg-breakdown__bar" role="img" aria-label="Cơ cấu {head.lower()}">{bar}</ul>'
            f'<ul class="arg-breakdown__list">{items}</ul></div>')


V = lambda n: f'var(--arg-viz-{n})'


def cash_breakdown():
    a, o = CASH['adv'], CASH['other']
    rows = [('Tiền có thể rút', CASH['withdraw'], V(1), None), ('Lệnh mua chưa khớp', CASH['buy'], V(2), None),
            ('Tiền ứng trước khả dụng', sum(a), V(4), [('T1', a[0]), ('T2', a[1]), ('T3', a[2])]), ('Tiền đã ứng trước', CASH['cadv'], V(5), None),
            ('Khác', sum(o), V(6), [('Cổ tức bằng tiền', o[0]), ('Giá trị phong toả', o[1])])]
    rows = [(l, v, c, k or []) for l, v, c, k in rows]
    return breakdown('Tiền', F['cash'], [(v, c) for _, v, c, _ in rows], rows, 'cb')


def stock_breakdown():
    rows = [('Cổ phiếu đang nắm giữ', F['hold'], V(1), []), ('Cổ phiếu chờ khớp', PENDING_STOCK, V(4), []), ('Giá trị quyền chờ về', PENDING_RIGHTS, V(6), [])]
    return breakdown('Giá trị cổ phiếu', F['stock'], [(v, c) for _, v, c, _ in rows], rows, 'sb')


def fee_breakdown():
    rows = [('Phí giao dịch', FEES['broker'], V(1), []), ('Phí lưu ký', FEES['custody'], V(2), []), ('Thuế bán', FEES['tax'], V(5), [])]
    return breakdown('Tổng phí và thuế trong tháng', F['fee'], [(v, c) for _, v, c, _ in rows], rows, 'fb')


def donut(parts, label, uid):
    """parts: [(tên, giá trị)], phần lớn nhất nằm giữa vòng."""
    tot = sum(v for _, v in parts); off = 0; segs = ''; leg = ''
    big = max(parts, key=lambda p: p[1])
    for i, (n, v) in enumerate(parts):
        p = v / tot * 100
        segs += RING.seg(f'var(--arg-viz-{i + 1})', off, p, n, f'{vn(p, 1)}%')
        leg += f'<li style="--c:var(--arg-viz-{i + 1})"><i class="arg-donut__key"></i><span class="arg-donut__name">{n}</span><span class="arg-donut__pct">{vn(p, 1)}%</span><span class="arg-donut__sub"{SEC}>{tr(v)}</span></li>'
        off += p
    return (f'<div class="arg-donut"><div class="arg-donut__chart" role="img" aria-label="{label}"><svg viewBox="0 0 42 42" aria-hidden="true"><circle class="bg" cx="21" cy="21" r="15.915" pathLength="100"/>{segs}</svg>'
            f'<div class="arg-donut__center"><b>{vn(big[1] / tot * 100, 1)}%</b><span>{big[0]}</span></div></div><ul class="arg-donut__legend">{leg}</ul></div>')


def date_pair(uid, a='2026-09-29', b='2026-10-29', compact=False):
    f = lambda i, lab, iso, extra='': (f'<div class="arg-field"><label class="arg-label" for="{uid}-{i}">{lab}</label><div class="arg-control arg-datepicker__field"><input class="arg-input" id="{uid}-{i}" type="text" '
                                       f'value="{iso[8:]}/{iso[5:7]}/{iso[:4]}" data-iso="{iso}"{extra} data-arg-datepicker>{I("calendar-blank")}</div></div>')
    mid = f'<i class="arg-asset-dates__to" aria-hidden="true">{I("arrow-right")}</i>' if compact else ''
    return f'<div class="arg-asset-dates{" arg-asset-dates--compact" if compact else ""}">{f("from", "Từ ngày", a, " data-max=\"2026-10-29\"")}{mid}{f("to", "Đến ngày", b, " data-max=\"2026-10-29\"")}</div>'


# ---------- tab Tài sản ----------
def tab_asset():
    m = '<dl class="arg-metric-row">' + mc('Lãi đã thực hiện', num(6_450_000), 'Từ đầu tháng', 'up') + mc('Lãi chưa thực hiện', sgn(F['unreal']), f'{vn(F["unreal_pct"], 2, True)}%', kk(F['unreal'])) \
        + mc('Tài sản ròng', num(F['net'])) + mc('Tiền có thể rút', num(CASH['withdraw'])) + '</dl>'
    top = f'<div class="arg-page__block"><div class="arg-stack">{assetcard()}{m}{debtcard()}</div></div>'
    struct = IP.block('Cơ cấu tài sản', donut([('Cổ phiếu', F['stock']), ('Tiền', F['cash'])], 'Cơ cấu tài sản', 'ds'), 'as-struct')
    unsettled = f'<div class="arg-breakdown__row"><span>Tiền chưa về</span><b{SEC}>{num(UNSETTLED)}</b></div>'
    btns = '<div class="arg-asset-actions"><button class="arg-btn arg-btn--outline arg-btn--xl" type="button">Rút tiền</button><button class="arg-btn arg-btn--primary arg-btn--xl" type="button">Nộp tiền</button></div>'
    cash = IP.block('Tiền', cash_breakdown() + unsettled + btns, 'as-cash')
    d = DEBT
    rows = [('Tổng dư nợ', F['debt'], ''), ('Nợ trong ngày đã khớp', d['intra_ok'], ''), ('Nợ trong ngày chờ khớp', d['intra_wait'], ''), ('Tổng nợ trong ngày', F['intra'], ' arg-down'),
            ('Gốc nợ còn lại', d['principal'], ''), ('Lãi nợ còn lại', d['interest'], ''), ('Lãi nợ quá hạn', d['overdue'], '')]
    kv = '<dl class="arg-kv arg-kv--lines">' + ''.join(f'<div class="arg-kv__row"><dt>{l}</dt><dd class="{c.strip()}"{SEC}>{num(v)}</dd></div>' for l, v, c in rows) + '</dl>'
    stock = IP.block('Cổ phiếu', stock_breakdown() + f'<div class="arg-stack"><h3 class="arg-asset-sub">Dư nợ</h3>{kv}</div>', 'as-stock')
    fees = IP.block('Phí và thuế', fee_breakdown(), 'as-fee')
    return f'<div class="arg-tabpanel" role="tabpanel" data-arg-secret-scope>{top}{struct}{cash}{stock}{fees}</div>'


# ---------- tab Danh mục ----------
def tab_portfolio():
    m = ('<dl class="arg-metric-row">' + mc('Giá trị cổ phiếu', num(F['hold'])) + mc('Lãi/lỗ chưa thực hiện', tr(F['unreal'], True), f'{vn(F["unreal_pct"], 2, True)}%', kk(F['unreal']))
         + mc('Sức mua', num(BUYING_POWER)) + mc('Tỷ lệ ký quỹ', f'{vn(F["margin_ratio"], 1)}%') + '</dl>')
    parts = sorted([(c, BY[c].last * q * 1000) for c, (q, _) in HELD.items()], key=lambda p: -p[1])
    alloc = IP.block('Phân bổ danh mục', donut(parts, 'Phân bổ danh mục theo mã', 'dp'))
    pl = sorted([(c, round((BY[c].last - cv) * q * 1000)) for c, (q, cv) in HELD.items()], key=lambda p: -p[1])
    mx = max(abs(v) for _, v in pl)
    bars = ''
    for c, v in pl:
        k = 'up' if v > 0 else 'down'; h = round(abs(v) / mx * 100); lab = vn(v / 1e6, 2, True) + 'tr'
        pos = f'<div class="arg-bar__half arg-bar__half--pos"><span class="arg-bar__val arg-up">{lab}</span><span class="arg-bar__fill arg-bar__fill--up" style="--v:{h}"></span></div><div class="arg-bar__half arg-bar__half--neg"></div>'
        neg = f'<div class="arg-bar__half arg-bar__half--pos"></div><div class="arg-bar__half arg-bar__half--neg"><span class="arg-bar__fill arg-bar__fill--down" style="--v:{h}"></span><span class="arg-bar__val arg-down">{lab}</span></div>'
        bars += f'<div class="arg-bar">{pos if v > 0 else neg}<span class="arg-bar__date">{c}</span></div>'
    perf = IP.block('Hiệu quả theo mã', f'<div class="arg-bars" style="--n:{len(pl)}" role="img" aria-label="Lãi lỗ chưa thực hiện theo mã">{bars}</div>', sub='Lãi/lỗ chưa thực hiện, đơn vị triệu đồng')
    hold = MP.portfolio_pane('m1', '039C101991 - 02', 'Tiểu khoản ký quỹ', HELD, CASH['withdraw'])[1]
    held = IP.block('Cổ phiếu nắm giữ', f'<div class="arg-stack" data-arg-listbar-scope>{hold}</div>', sub='Giá nghìn đồng · Lãi/lỗ tính theo giá vốn, đơn vị đồng')
    return f'<div class="arg-tabpanel" role="tabpanel" hidden><div class="arg-page__block">{m}</div>{alloc}{perf}{held}</div>'


# ---------- tab Lãi lỗ ----------
def trading_days():
    d, out = date(2026, 9, 29), []
    while d <= date(2026, 10, 29):
        if d.weekday() < 5: out.append(d)
        d += timedelta(days=1)
    return out


DAYS = trading_days()
_r = random.Random('asset-pl')
DAILY = [round(_r.gauss(80_000, 900_000) / 10_000) * 10_000 for _ in DAYS]
CUM = [sum(DAILY[:i + 1]) for i in range(len(DAYS))]
PROFIT = sum(v for v in DAILY if v > 0); LOSS = sum(v for v in DAILY if v < 0)


def plchart(uid):
    lo, hi = min(min(CUM), 0), max(max(CUM), 0); pad = (hi - lo) * .12; lo -= pad; hi += pad
    n = len(CUM); x = lambda i: i / (n - 1) * 100; y = lambda v: (hi - v) / (hi - lo) * 100
    line = 'M' + ' L'.join(f'{x(i):.2f},{y(v):.2f}' for i, v in enumerate(CUM)); y0 = y(0)
    area = f'{line} L100,{y0:.2f} L0,{y0:.2f} Z'
    g = lambda k, c: f'<g class="{k}" clip-path="url(#{uid}-{k})"><path class="area" d="{area}"/><path class="line" d="{line}"/></g>'
    clips = f'<clipPath id="{uid}-up"><rect x="0" y="0" width="100" height="{y0:.2f}"/></clipPath><clipPath id="{uid}-down"><rect x="0" y="{y0:.2f}" width="100" height="{100 - y0:.2f}"/></clipPath>'
    full = [d.strftime('%d/%m/%Y') for d in DAYS]
    axis = ''.join(f'<span>{DAYS[round(i * (n - 1) / 4)].strftime("%d/%m")}</span>' for i in range(5))
    import json
    return (f'<div class="arg-plchart"><div class="arg-plchart__plot" data-arg-plchart data-points=\'{json.dumps(CUM)}\' data-dates=\'{json.dumps(full)}\' data-min="{lo:.0f}" data-max="{hi:.0f}" role="img" aria-label="Lãi lỗ luỹ kế theo ngày">'
            f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><defs>{clips}</defs><line class="base" x1="0" x2="100" y1="{y0:.2f}" y2="{y0:.2f}"/>{g("up", "")}{g("down", "")}</svg>'
            f'<i class="arg-plchart__cur"></i><i class="arg-plchart__dot"></i><div class="arg-plchart__tip"></div></div><div class="arg-plchart__axis" aria-hidden="true">{axis}</div></div>')


def stmt_pl(date_s, kind, amount, text):
    return (f'<li class="arg-stmt"><div class="arg-stmt__head"><span>{date_s}</span><span class="arg-stmt__type">{kind}</span></div>'
            f'<dl class="arg-stmt__rows"><div class="arg-stmt__row"><dt>Số tiền</dt><dd class="{cls(amount)}">{sgn(amount)}</dd></div></dl><p class="arg-stmt__title">{text}</p></li>')


def tab_pl():
    diff = PROFIT + LOSS
    m = ('<dl class="arg-metric-row">' + mc('Tổng lãi', sgn(PROFIT), '', 'up') + mc('Tổng lỗ', sgn(LOSS), '', 'down') + mc('Chênh lệch lãi lỗ', sgn(diff), '', kk(diff))
         + mc('Tổng phí và thuế', num(F['fee'])) + mc('Lãi lỗ ròng sau thuế', sgn(diff - F['fee']), '', kk(diff - F['fee']), wide=True) + '</dl>')
    rows = [('27/10/2026', 'Bán cổ phiếu', 3_250_000, 'Bán 1.000 HPG giá 27,10'), ('20/10/2026', 'Bán cổ phiếu', -1_950_000, 'Bán 3.000 NVL giá 14,95'),
            ('15/10/2026', 'Bán cổ phiếu', 1_800_000, 'Bán 500 VCB giá 91,80'), ('08/10/2026', 'Bán cổ phiếu', 2_325_000, 'Bán 1.500 AGR giá 19,75')]
    top = f'<div class="arg-page__block">{date_pair("pl")}{plchart("plc")}</div>'
    return (f'<div class="arg-tabpanel" role="tabpanel" hidden>{top}<div class="arg-page__block">{m}</div>'
            f'{IP.block("Lệnh đã bán", "<ul class=\"arg-stmt-list\">" + "".join(stmt_pl(*r) for r in rows) + "</ul>", sub="Các lệnh bán đã khớp trong kỳ, số mẫu")}</div>')


# ---------- tab Sao kê tiền ----------
# (ngày, loại, ghi có, ghi nợ, phí, thuế, nội dung): sắp theo thời gian, số dư chạy từ số dư đầu kỳ
OPEN_CO = 51_998_500
ROWS_CO = [('02/10/2026', 'Nộp tiền ký quỹ', 20_000_000, 0, 0, 0, 'Nộp tiền vào tiểu khoản ký quỹ'), ('08/10/2026', 'Mua cổ phiếu', 0, 26_000_000, 39_000, 0, 'Mua 1.000 HPG giá 26,00'),
           ('15/10/2026', 'Bán cổ phiếu', 54_200_000, 0, 81_300, 54_200, 'Bán 600 VCB giá 90,33'), ('20/10/2026', 'Phí lưu ký', 0, 24_000, 0, 0, 'Phí lưu ký tháng 10'),
           ('27/10/2026', 'Rút tiền', 0, 40_000_000, 0, 0, 'Rút tiền về ngân hàng')]
OPEN_VSD = 1_500_000
ROWS_VSD = [('12/10/2026', 'Cổ tức bằng tiền', 2_500_000, 0, 0, 0, 'Cổ tức HPG đợt 1'), ('22/10/2026', 'Phí lưu ký', 0, 500_000, 0, 0, 'Phí lưu ký VSD')]


def with_balance(open_, rows):
    out, bal = [], open_
    for r in rows:
        bal += r[2] - r[3] - r[4] - r[5]; out.append(r + (bal,))
    return out, bal


def stmt_cash(r, uid):
    """Một giao dịch tiền dạng hàng gọn: dòng trên là nội dung và số tiền ròng (tô màu), dòng dưới là ngày, loại và số dư; bấm để xem ghi có, ghi nợ, phí, thuế."""
    d, kind, cr, db, fee, tax, text, bal = r
    net = cr - db
    kv = lambda l, v, c='': f'<div class="arg-stmt__row"><dt>{l}</dt><dd class="{c}">{v}</dd></div>'
    extra = kv('Ghi có', num(cr), 'arg-up' if cr else '') + kv('Ghi nợ', num(db), 'arg-down' if db else '') + kv('Phí', num(fee)) + kv('Thuế', num(tax))
    return (f'<li class="arg-stmt arg-stmt--compact"><button class="arg-stmt__main" type="button" data-arg-collapse aria-controls="{uid}" aria-expanded="false" aria-label="Xem chi tiết giao dịch">'
            f'<span class="arg-stmt__title">{text}</span><b class="arg-stmt__amt {cls(net)}">{sgn(net)}</b>'
            f'<span class="arg-stmt__meta">{d} · {kind}</span><span class="arg-stmt__bal">Số dư {num(bal)}</span></button>'
            f'<div class="arg-collapse" id="{uid}"><div><dl class="arg-stmt__rows">{extra}</dl></div></div></li>')


def cash_pane(uid, open_, rows):
    done, end = with_balance(open_, rows)
    m = f'<dl class="arg-cashsum"><div><dt>Đầu kỳ</dt><dd{SEC}>{num(open_)}</dd></div><i aria-hidden="true">{I("arrow-right")}</i><div><dt>Cuối kỳ</dt><dd{SEC}>{num(end)}</dd></div></dl>'
    lst = '<ul class="arg-stmt-list">' + ''.join(stmt_cash(r, f'{uid}-{i}') for i, r in enumerate(reversed(done))) + '</ul>'
    return f'<div class="arg-stack">{date_pair(uid, compact=True)}{m}{lst}</div>'


def tab_cash():
    assert with_balance(OPEN_CO, ROWS_CO)[1] == F['cash']   # số dư cuối kỳ tiền tại công ty bằng khối Tiền
    names = ['Tiền tại công ty', 'Tiền tại VSD']
    head = IP.pills('Nguồn tiền', names, fill=True)
    panes = [cash_pane('cc', OPEN_CO, ROWS_CO), cash_pane('cv', OPEN_VSD, ROWS_VSD)]
    body = ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == 0 else " hidden"}><div class="arg-page__block">{p}</div></div>' for i, p in enumerate(panes))
    return f'<div class="arg-tabpanel" role="tabpanel" hidden><div class="arg-page__tabbed" data-arg-tabs><div class="arg-page__block">{head}</div>{body}</div></div>'


def screen(tabbar_html):
    tabs = [('Tài sản', tab_asset()), ('Danh mục', tab_portfolio()), ('Lãi lỗ', tab_pl()), ('Sao kê tiền', tab_cash())]
    chips = ''.join(f'<button class="arg-tab arg-sidepanel__item" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, (t, _) in enumerate(tabs))
    return f'''<div class="arg-screen arg-screen--sections" data-arg-screen="asset" hidden>
<header class="arg-appbar arg-appbar--sticky">{TP.acctsel(ACCOUNTS)}</header>
<main class="arg-page__main">
  <div class="arg-page__tabbed arg-page__tabbed--side" data-arg-tabs>
    <div class="arg-page__block arg-sidepanel"><div class="arg-tabs arg-tabs--lg"><div class="arg-tablist" role="tablist" aria-label="Nội dung tài sản">{chips}</div></div></div>
    {''.join(h for _, h in tabs)}
  </div>
</main>
{tabbar_html}
</div>'''
