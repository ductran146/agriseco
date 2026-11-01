"""Markup cho màn Thông tin cổ phiếu (bấm vào một mã), dựng từ component ARG:
appbar, symbol, pricehead, statrow, statgrid, chip-tab, chart, depth, tabs, bars, dtable, news, actionbar.
Mọi hàm nhận một mã (stocks.Stock, mặc định VCB). Dữ liệu mẫu trong stocks.py, khớp màn Giao dịch của cùng mã."""
import random

import detail_parts as DP
import trade_parts as TP
from stocks import VCB, WHEN

I, vn = DP.I, DP.vn
num = lambda n: f'{n:,}'.replace(',', '.')
ARROW = {'up': 'caret-up-fill', 'down': 'caret-down-fill', 'ref': 'minus'}


def appbar(st=VCB):
    return (f'<header class="arg-appbar arg-appbar--sticky arg-appbar--condense" data-arg-condense=".arg-pricehead"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I("caret-left")}</button>'
            f'<div class="arg-appbar__stack"><h1 class="arg-appbar__title">{st.code}</h1><div class="arg-appbar__info" aria-hidden="true"><span class="arg-appbar__name">{st.code}</span>'
            f'<div class="arg-appbar__quote arg-{st.kind}"><b>{vn(st.last)}</b><span>{I(ARROW[st.kind])}{vn(abs(st.chg))} ({vn(st.pct, 2, True)}%)</span></div></div></div>'
            f'<div class="arg-appbar__tools"><button class="arg-appbar__tool" type="button" data-arg-fav-toggle aria-pressed="false" aria-label="Thêm {st.code} vào danh mục theo dõi" data-label-on="Bỏ {st.code} khỏi danh mục theo dõi" data-label-off="Thêm {st.code} vào danh mục theo dõi"><span class="arg-fav__on">{I("star-fill")}</span><span class="arg-fav__off">{I("star")}</span></button><button class="arg-appbar__tool" type="button" aria-label="Chia sẻ">{I("share-network")}</button></div></header>')


def symbol_bar(st=VCB):
    return TP.symbol(st.code, st.ex, right='<span class="arg-live"><i class="arg-live__dot"></i>Phiên liên tục</span>')


def price(st=VCB):
    return (f'<div class="arg-pricehead arg-pricehead--lg arg-pricehead--{st.kind}"><div class="arg-pricehead__row">'
            f'<div class="arg-pricehead__main"><b class="arg-pricehead__value">{vn(st.last)}</b>'
            f'<span class="arg-pricehead__change"><span>{I(ARROW[st.kind])}{vn(abs(st.chg))}</span><span class="arg-badge arg-badge--{st.kind}">{vn(st.pct, 2, True)}%</span></span></div>'
            f'</div></div>')


def holding(st=VCB):
    """Cổ phiếu đang nắm giữ; mã không sở hữu thì không hiện hàng này."""
    if not st.hold: return ''
    qty, cost = st.hold
    pl = round((st.last - cost) * qty * 1000)
    rows = [('Đang sở hữu', f'{num(qty)} CP', ''), ('Lãi/lỗ tạm tính', ('+' if pl > 0 else '') + num(pl), 'arg-up' if pl > 0 else 'arg-down' if pl < 0 else ''), ('Giá vốn', vn(cost), '')]
    return '<dl class="arg-kv arg-stock-hold">' + ''.join(f'<div class="arg-kv__row"><dt>{l}</dt><dd{f" class=\"{c}\"" if c else ""}>{v}</dd></div>' for l, v, c in rows) + '</dl>'


def statgrid(items, more=None, uid='', label='Xem thêm chỉ số'):
    """items, more: [(nhãn, giá trị, lớp màu)]. more là phần thu gọn được, mở sẵn."""
    grid = lambda xs: '<dl class="arg-statgrid__grid">' + ''.join(f'<div class="arg-statgrid__item"><dt>{l}</dt><dd{f" class=\"{c}\"" if c else ""}>{v}</dd></div>' for l, v, c in xs) + '</dl>'
    out = grid(items)
    if more:
        out += (f'<div class="arg-collapse is-open" id="{uid}"><div>{grid(more)}</div></div>'
                f'<button class="arg-icon-btn arg-collapse-toggle arg-statgrid__more" type="button" data-arg-collapse aria-controls="{uid}" aria-expanded="true" aria-label="{label}">{I("caret-down")}</button>')
    return f'<div class="arg-statgrid">{out}</div>'


def stats(st=VCB, uid=None):
    main = [('Trần', vn(st.ceil), 'arg-ceil'), ('Tham chiếu', vn(st.ref), 'arg-ref'), ('Sàn', vn(st.floor), 'arg-floor'),
            ('Cao', vn(st.high), st.cls(st.high)), ('Trung bình', vn(st.avg), st.cls(st.avg)), ('Thấp', vn(st.low), st.cls(st.low))]
    more = [('Khối lượng', num(st.vol), ''), ('Giá trị', f'{vn(st.turnover)} tỷ', ''), ('Mở cửa', vn(st.open), st.cls(st.open)),
            ('Cao 52 tuần', vn(st.hi52), ''), ('Thấp 52 tuần', vn(st.lo52), ''), ('Vốn hoá', f'{num(st.cap)} tỷ', '')]
    return statgrid(main, more, uid or st.uid)


def candles_today(st=VCB, n=44):
    """Nến trong phiên 09:00 đến 10:15 theo bước giá của mã: nến đầu mở cửa đúng giá mở, nến cuối đóng đúng giá khớp,
    một nến chạm đúng giá cao nhất và một nến chạm đúng giá thấp nhất; tổng khối lượng = khối lượng khớp."""
    r, s = random.Random(st.seed), st.step
    i_hi, i_lo = (8, 34) if st.last < st.open else (34, 8)
    pts = sorted([(0, st.open), (i_hi, st.high - s), (i_lo, st.low + s), (21, (st.high + st.low) / 2), (n - 1, st.last)])
    def target(i):
        for (a, pa), (b, pb) in zip(pts, pts[1:]):
            if a <= i <= b: return pa + (pb - pa) * (i - a) / (b - a)
    snap = lambda p: min(st.high, max(st.low, round(round(p / s) * s, 2)))
    rows, prev = [], st.open
    for i in range(n):
        c = st.last if i == n - 1 else snap(target(i) + s * r.choice((-1, 0, 0, 1)))
        o = prev
        h = st.high if i == i_hi else snap(max(o, c) + s * r.choice((0, 1)))
        l = st.low if i == i_lo else snap(min(o, c) - s * r.choice((0, 1)))
        rows.append([o, max(h, o, c), min(l, o, c), c, r.uniform(.25, 1) * (1.4 if abs(c - o) > s / 2 else 1)]); prev = c
    top = max(x[4] for x in rows)
    for x in rows: x[4] = round(x[4] / top, 4)
    return rows


def chart(st=VCB):
    rows = candles_today(st)
    lo, hi = min(x[2] for x in rows), max(x[1] for x in rows)     # DP.chart chuẩn hoá lo → 0,08, hi → 0,92
    b = (hi - lo) / .84; base = lo - .08 * b + b / 2               # chart.js: giá = base × (1 − span/2 + t × span)
    vol_k = st.vol / 1000 / sum(x[4] for x in rows)                # khối lượng nến theo nghìn CP, tổng = khối lượng khớp
    return DP.chart(st.seed, st.kind, base=round(base, 4), rng=0, rows=[tuple(x) for x in rows],
                    opts={'span': round(b / base, 6), 'vol': round(vol_k, 3), 'vol-unit': 'nghìn', 'start': 540, 'end': 615})


def depth(st=VCB, bids=None, asks=None, limits=False):
    """Bước giá hai bên. Mặc định 3 mức tốt nhất; truyền bids (giá giảm dần), asks (giá tăng dần) để xem nhiều mức; limits thêm hàng Sàn (trái), Trần (phải)."""
    bids, asks = bids or st.bids, asks or st.asks
    tb, ta = sum(v for _, v in bids), sum(v for _, v in asks)
    pb = round(tb / (tb + ta) * 100); m = max(v for _, v in bids + asks)
    half = lambda k, p, v: (f'<div class="arg-depth__half arg-depth__half--{k}" style="--w:{v / m * 100:.0f}">'
                            + (f'<span class="arg-depth__vol">{num(v)}</span><span class="arg-depth__price {st.cls(p)}">{vn(p)}</span>' if k == 'bid' else
                               f'<span class="arg-depth__price {st.cls(p)}">{vn(p)}</span><span class="arg-depth__vol">{num(v)}</span>') + '</div>')
    empty = lambda k: f'<div class="arg-depth__half arg-depth__half--{k}"></div>'
    rows = ''.join('<div class="arg-depth__row">' + (half('bid', *bids[i]) if i < len(bids) else empty('bid')) + (half('ask', *asks[i]) if i < len(asks) else empty('ask')) + '</div>'
                   for i in range(max(len(bids), len(asks))))
    return (f'<div class="arg-depth" role="group" aria-label="Bước giá: dư mua {num(tb)}, dư bán {num(ta)}">'
            f'<div class="arg-depth__head"><div class="arg-depth__side arg-depth__side--bid"><b>Dư mua</b><span>Tổng {num(tb)} · {pb}%</span></div>'
            f'<div class="arg-depth__side arg-depth__side--ask"><b>Dư bán</b><span>Tổng {num(ta)} · {100 - pb}%</span></div></div>'
            f'<div class="arg-depth__ratio" style="--v:{pb}" aria-hidden="true"></div>{rows}'
            + (f'<div class="arg-depth__limits"><div class="arg-depth__limit arg-depth__limit--floor"><span>Sàn</span><b>{vn(st.floor)}</b></div>'
               f'<div class="arg-depth__limit arg-depth__limit--ceil"><span>Trần</span><b>{vn(st.ceil)}</b></div></div>' if limits else '') + '</div>')


def foreign(st=VCB):
    net = st.f_buy - st.f_sell
    sign = lambda x: 'arg-up' if x > 0 else 'arg-down' if x < 0 else ''
    return statgrid([('KL mua', num(st.f_buy), ''), ('KL bán', num(st.f_sell), ''), ('KL mua ròng', ('+' if net > 0 else '') + num(net), sign(net)),
                     ('GT mua', f'{vn(st.f_gb)} tỷ', ''), ('GT bán', f'{vn(st.f_gs)} tỷ', ''), ('GT mua ròng', f'{vn(st.f_gnet, 2, True)} tỷ', sign(st.f_gnet))])


def netbuy_block(st=VCB):
    f = lambda v: vn(v, 1, True)
    tabs = ''.join(f'<button class="arg-tab" role="tab" type="button" aria-selected="{s}">{t}</button>' for t, s in (('Hôm nay', 'false'), ('10 phiên', 'true')))
    return (f'<div class="arg-page__block" data-arg-tabs><div class="arg-title arg-title--md arg-title--stacked"><div class="arg-title__left"><div class="arg-title__main">'
            f'<div class="arg-title__text" role="heading" aria-level="2">Mua ròng</div><span class="arg-title__sub">Khối ngoại · tỷ đồng</span></div></div>'
            f'<div class="arg-title__right"><div class="arg-tabs arg-tabs--pill"><div class="arg-tablist" role="tablist" aria-label="Khoảng thời gian">{tabs}</div></div></div></div>'
            f'<div class="arg-tabpanel" role="tabpanel" hidden>{DP.bars(st.net_today, f, "Khối ngoại mua ròng theo giờ hôm nay")}</div>'
            f'<div class="arg-tabpanel" role="tabpanel">{DP.bars(st.net_10, f, "Khối ngoại mua ròng 10 phiên", dense=True)}</div></div>')


def ticks(st=VCB, n=10):
    body = [[t, (s, 'arg-buy' if s == 'M' else 'arg-sell'), (vn(p), st.cls(p)), (vn(p - st.ref, 2, True), st.cls(p)), num(v)] for t, s, p, v in st.ticks[:n]]
    return DP.dtable(['Thời gian', 'M/B', 'Giá', '+/-', 'KL'], body, '1.2fr .6fr 1fr 1fr 1fr').replace('class="arg-dtable"', 'class="arg-dtable arg-dtable--plain"', 1)


def news_items(st=VCB):
    return [(f'{st.name} công bố kết quả kinh doanh quý III', '29/10/2026', 'Agriseco'), (f'Cổ phiếu {st.code}: diễn biến phiên sáng', '29/10/2026', 'Vietstock'),
            ('Khối ngoại giao dịch sôi động nhóm vốn hoá lớn', '27/10/2026', 'CafeF'), ('Lịch trả cổ tức tuần này', '26/10/2026', 'Tin nhanh')]


def actionbar(st=VCB):
    return (f'<div class="arg-actionbar arg-actionbar--fixed" role="group" aria-label="Đặt lệnh {st.code}">'
            f'<button class="arg-btn arg-btn--buy arg-btn--xl" type="button" data-arg-go="{st.trade_id}" data-arg-side="buy">Mua</button>'
            f'<button class="arg-btn arg-btn--sell arg-btn--xl" type="button" data-arg-go="{st.trade_id}" data-arg-side="sell">Bán</button></div>')
