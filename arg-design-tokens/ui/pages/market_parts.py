"""Markup màn Thị trường, dựng từ component ARG: appbar, tabs (--lg, --pill), chip-tab, donut, fchart, hbars, share, flow, bars, statgrid,
quote (--rank, --board, --fav), listbar, suggest, fab, dtable, kv. Dữ liệu mẫu trong market.py, stocks.py, account_parts.py."""
import ring as RING
import detail_parts as DP
import info_parts as IP
import account_parts as AP
import stock_parts as SP
import unicodedata
import themes as TM
from spark import spark
from stocks import STOCKS
from market import EXCHANGES, EX, BINS, THEMES, DAYS, SESS, FULL, universe, times, netflow, net10

I, vn = DP.I, DP.vn
num = lambda n: f'{round(n):,}'.replace(',', '.')
sg = lambda v, d=2: vn(v, d, True)
KCLS = {'up': 'arg-up', 'down': 'arg-down', 'ref': 'arg-ref', 'ceil': 'arg-ceil', 'floor': 'arg-floor'}


def code_link(r):
    return f'<a class="arg-dtable__link" href="#" data-arg-go="{r.go}">{r.code}</a>' if r.go else r.code


# ---------- Tổng quan · Biến động ----------
def breadth(ex):
    up, ref, down = EX[ex]['breadth']; total = up + ref + down
    rows = [('Tăng', up, 'var(--arg-trading-up-light-increase)'), ('Giảm', down, 'var(--arg-trading-down-light-increase)'), ('Đứng', ref, 'var(--arg-trading-flat-flat)')]
    seg, off = '', 0
    for n, c, col in rows:
        p = c / total * 100
        seg += RING.seg(col, off, p, n, f'{c} mã')
        off += p
    leg = ''.join(f'<li style="--c:{col}"><i class="arg-donut__key"></i><span class="arg-donut__name">{n}</span><span class="arg-donut__pct">{c} mã</span>'
                  f'<span class="arg-donut__sub">{vn(c / total * 100, 1)}% số mã</span></li>' for n, c, col in rows)
    return (f'<div class="arg-donut"><div class="arg-donut__chart" role="img" aria-label="{up} mã tăng, {down} mã giảm, {ref} mã đứng giá">'
            f'<svg viewBox="0 0 42 42" aria-hidden="true"><circle class="bg" cx="21" cy="21" r="15.915" pathLength="100"/>{seg}</svg>'
            f'<div class="arg-donut__center"><b>{total}</b><span>mã giao dịch</span></div></div><ul class="arg-donut__legend">{leg}</ul></div>')


def capital(ex):
    up, ref, down = EX[ex]['flow']
    return IP.fchart(['Nhóm tăng', 'Nhóm đứng', 'Nhóm giảm'], [up, ref, down], lambda v: vn(v, 1), [], kinds=['up', 'ref', 'down'], label='Giá trị khớp theo nhóm mã')


def impact(ex):
    rows = universe(ex)
    pos = sorted([r for r in rows if r.impact > 0], key=lambda r: -r.impact)[:8]
    neg = sorted([r for r in rows if r.impact < 0], key=lambda r: r.impact)[:8][::-1]
    m = max(abs(r.impact) for r in pos + neg)
    code = lambda r: f'<a class="arg-hbars__code" href="#" data-arg-go="{r.go}">{r.code}</a>' if r.go else f'<span class="arg-hbars__code">{r.code}</span>'
    li = ''.join(f'<li class="arg-hbars__row{" arg-hbars__row--down" if r.impact < 0 else ""}">{code(r)}<span class="arg-hbars__track"><span class="arg-hbars__bar" style="--w:{abs(r.impact) / m * 100:.0f}"></span>'
                 f'<span class="arg-hbars__val">{sg(r.impact)}</span></span></li>' for r in pos + neg[::-1])
    tp, tn = EX[ex]['impact']
    w = tp / (tp - tn) * 100
    ratio = (f'<div class="arg-share" role="img" aria-label="Tổng điểm kéo lên {sg(tp)}, kéo xuống {sg(tn)}, thay đổi {sg(tp + tn)} điểm"><div class="arg-share__bar">'
             f'<span class="arg-share__seg arg-share__seg--up" style="--w:{w:.1f}">{sg(tp)}</span><span class="arg-share__seg arg-share__seg--down" style="--w:{100 - w:.1f}">{sg(tn)}</span></div></div>')
    return f'<ul class="arg-hbars">{li}</ul>{ratio}'


def nice(v):
    for s in (5, 10, 20, 25, 50, 100, 200, 250, 500):
        if v / s <= 2: return s
    return 1000


def flow(values, uid, note=''):
    t = times(); n = len(t)
    step = nice(max(abs(v) for v in values) or 1); top = step * 2
    x = lambda i: i / (n - 1) * 100
    y = lambda v: (top - v) / (2 * top) * 100
    pts = ' '.join(f'{x(i):.2f},{y(v):.2f}' for i, v in enumerate(values))
    last = x(len(values) - 1)
    area = f'0,50 {pts} {last:.2f},50'
    grid = ''.join(f'<line class="grid" x1="0" x2="100" y1="{y(k * step):.2f}" y2="{y(k * step):.2f}"/>' for k in (-2, -1, 1, 2))
    svg = (f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><defs><clipPath id="{uid}-u"><rect x="0" y="0" width="100" height="50"/></clipPath>'
           f'<clipPath id="{uid}-d"><rect x="0" y="50" width="100" height="50"/></clipPath></defs>{grid}<line class="zero" x1="0" x2="100" y1="50" y2="50"/>'
           f'<polygon class="area-up" clip-path="url(#{uid}-u)" points="{area}"/><polygon class="area-down" clip-path="url(#{uid}-d)" points="{area}"/>'
           f'<polyline class="line-up" clip-path="url(#{uid}-u)" points="{pts}"/><polyline class="line-down" clip-path="url(#{uid}-d)" points="{pts}"/></svg>')
    ylab = ''.join(f'<li style="top:{y(k * step):.1f}%">{num(k * step)}</li>' for k in (2, 1, 0, -1, -2))
    xlab = ''.join(f'<li style="left:{x(i):.1f}%">{t[i]}</li>' for i in (0, 12, 24, 31, 43, n - 1))
    end = values[-1]
    return (f'<div class="arg-flow" role="img" aria-label="Dòng tiền chủ động lũy kế, cuối kỳ {sg(end, 1)} tỷ đồng"><div class="arg-flow__body"><ul class="arg-flow__y" aria-hidden="true">{ylab}</ul>'
            f'<div class="arg-flow__plot">{svg}</div></div><ul class="arg-flow__x" aria-hidden="true">{xlab}</ul>'
            f'<ul class="arg-flow__legend"><li><i></i>Dòng tiền vào</li><li><i></i>Dòng tiền ra</li></ul>' + (f'<p class="arg-flow__note">{note}</p>' if note else '') + '</div>')


def netflow_block(ex, p):
    items = []
    for k, (lab, date) in enumerate(DAYS):
        v = netflow(ex, k)
        note = f'Phiên {date}: đến 10:15, lũy kế {sg(v[-1], 1)} tỷ' if k == 0 else f'Phiên {date}: cuối phiên {sg(v[-1], 1)} tỷ'
        items.append((lab, flow(v, f'{p}-fl{k}', note)))
    return IP.block('Dòng tiền chủ động', IP.tabset('Phiên', items), sub='Mua trừ bán chủ động, lũy kế · tỷ đồng')


def distribution(ex):
    up, ref, down = EX[ex]['breadth']
    counts = list(EX[ex]['down']) + [ref] + list(EX[ex]['up'])
    kinds = ['down'] * 5 + ['ref'] + ['up'] * 5
    ch = IP.fchart(list(BINS), counts, lambda v: str(v), [], kinds=kinds, bins=True, label='Số mã theo khoảng thay đổi giá')
    total = up + ref + down
    seg = lambda k, c: f'<span class="arg-share__seg arg-share__seg--{k}" style="--w:{c / total * 100:.1f}"></span>'
    ratio = (f'<div class="arg-share arg-share--thin" role="img" aria-label="{down} mã giảm, {ref} mã đứng, {up} mã tăng"><div class="arg-share__bar">{seg("down", down)}{seg("ref", ref)}{seg("up", up)}</div>'
             f'<ul class="arg-share__legend"><li class="arg-down">Giảm: {down}</li><li class="arg-ref">Đứng: {ref}</li><li class="arg-up">Tăng: {up}</li></ul></div>')
    return ch + ratio


def qhead(kind, mid, right, sub='% so với TC'):
    """Hàng tiêu đề cột của danh sách giá (Quote head): kind 'board' | 'fav' | 'rank'; mid = tiêu đề cột giữa; right = tiêu đề giá trị, dòng dưới là sub."""
    left = {'rank': '<span aria-hidden="true">#</span><span>Mã</span>', 'fav': '<span></span><span>Mã</span>'}.get(kind, '<span>Mã</span>')
    return (f'<div class="arg-quote-head arg-quote-head--{kind}" aria-hidden="true">{left}' + (f'<span class="arg-quote-head__mid">{mid}</span>' if mid else '')
            + f'<span class="arg-quote-head__val"><b>{right}</b><span>{sub}</span></span>' + ('<span></span>' if kind == 'fav' else '') + '</div>')


def rank_list(rows, metric, title='Giá (nghìn đ)'):
    """metric(r) -> (chữ giá trị bên phải, lớp màu hoặc None để dùng màu giá)."""
    out = ''
    for k, r in enumerate(rows, 1):
        idt = (f'<a class="arg-quote__id" href="#" data-arg-go="{r.go}" aria-label="Xem thông tin {r.code}"><b>{r.code}</b><span>{r.name}</span></a>' if r.go
               else f'<div class="arg-quote__id"><b>{r.code}</b><span>{r.name}</span></div>')
        val, cls = metric(r)
        price = (f'<div class="arg-quote__price"><b>{val}</b>' if cls is None else f'<div class="arg-quote__price arg-quote__price--metric"><b class="{cls}">{val}</b>')
        out += (f'<li class="arg-quote arg-quote--{r.kind} arg-quote--rank{" arg-quote--link" if r.go else ""}"><span class="arg-quote__rank">{k}</span>{idt}'
                f'{price}<span class="arg-badge arg-badge--{r.kind}">{sg(r.pct)}%</span></div></li>')
    return qhead('rank', '', title) + f'<ul class="arg-quote-list arg-quote-list--card">{out}</ul>'


def top_lists(ex, n=5):
    rows = universe(ex)
    pick = [('Khối lượng', sorted(rows, key=lambda r: -r.vol), lambda r: (f'{vn(r.vol, 1)} tr', ''), 'KL khớp (triệu CP)'),
            ('Tăng giá', sorted([r for r in rows if r.pct > 0], key=lambda r: -r.pct), lambda r: (vn(r.price), None), 'Giá (nghìn đ)'),
            ('Giảm giá', sorted([r for r in rows if r.pct < 0], key=lambda r: r.pct), lambda r: (vn(r.price), None), 'Giá (nghìn đ)'),
            ('NN mua ròng', sorted([r for r in rows if r.fnet > 0], key=lambda r: -r.fnet), lambda r: (f'{sg(r.fnet)} tỷ', 'arg-up'), 'Mua ròng (tỷ đ)'),
            ('NN bán ròng', sorted([r for r in rows if r.fnet < 0], key=lambda r: r.fnet), lambda r: (f'{sg(r.fnet)} tỷ', 'arg-down'), 'Bán ròng (tỷ đ)')]
    chips = ''.join(f'<button class="arg-chip-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, (t, _, _, _) in enumerate(pick))
    panels = ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == 0 else " hidden"}>{rank_list(rs[:n], m, ttl)}</div>' for i, (_, rs, m, ttl) in enumerate(pick))
    return f'<div class="arg-chip-tabs arg-chip-tabs--sm" data-arg-tabs><div class="arg-chip-tabs__list" role="tablist" aria-label="Tiêu chí">{chips}</div>{panels}</div>'


def volatility(ex, p):
    up, ref, down = EX[ex]['breadth']
    return (IP.block('Số mã tăng, giảm, đứng', breadth(ex)) + IP.block('Phân bổ dòng tiền', capital(ex), sub='Giá trị khớp theo nhóm mã · tỷ đồng')
            + IP.block('Tác động tới chỉ số', impact(ex), sub='Điểm đóng góp của các mã ảnh hưởng nhất') + netflow_block(ex, p)
            + IP.block('Phân bố tăng giảm', distribution(ex), sub=f'Theo khoảng % thay đổi giá · {up + ref + down} mã') + IP.block('Top cổ phiếu', top_lists(ex)))


# ---------- Tổng quan · Khối ngoại, Tự doanh ----------
def side_flow(ex, key):
    buy, sell = EX[ex][key]; net = round(buy - sell, 2)
    rows = universe(ex)
    val = (lambda r: r.fnet) if key == 'foreign' else (lambda r: r.prop)
    who = 'Khối ngoại' if key == 'foreign' else 'Tự doanh'
    stat = SP.statgrid([('GT mua', f'{vn(buy)} tỷ', ''), ('GT bán', f'{vn(sell)} tỷ', ''), ('GT ròng', f'{sg(net)} tỷ', KCLS['up' if net > 0 else 'down' if net < 0 else 'ref'])])
    def bars_of(sign):
        rs = sorted([r for r in rows if val(r) * sign > 0], key=lambda r: -abs(val(r)))[:8]
        if not rs: return '<p class="arg-note">Không có mã.</p>'
        m = max(abs(val(r)) for r in rs)
        code = lambda r: f'<a class="arg-hbars__code" href="#" data-arg-go="{r.go}">{r.code}</a>' if r.go else f'<span class="arg-hbars__code">{r.code}</span>'
        return '<ul class="arg-hbars">' + ''.join(f'<li class="arg-hbars__row{" arg-hbars__row--down" if sign < 0 else ""}">{code(r)}<span class="arg-hbars__track">'
                                                  f'<span class="arg-hbars__bar" style="--w:{abs(val(r)) / m * 100:.0f}"></span><span class="arg-hbars__val">{sg(val(r))} tỷ</span></span></li>' for r in rs) + '</ul>'
    hist = DP.bars(net10(ex, net, key), lambda v: vn(v, 1, True), f'{who} mua ròng 10 phiên', dense=True)
    return (IP.block(f'{who} hôm nay', stat, sub='Đến 10:15 · tỷ đồng') + IP.block('Mua ròng 10 phiên', hist, sub=f'{who} · tỷ đồng')
            + IP.block('Theo mã', IP.tabset('Chiều', [('Mua ròng', bars_of(1)), ('Bán ròng', bars_of(-1))]), sub=f'{who} · tỷ đồng'))


# ---------- Tổng quan · Thanh khoản ----------
def liquidity(ex):
    e = EX[ex]; today = round(sum(e['flow']), 1); vals = list(e['prev']) + [today]
    chg = [None] + [(b / a - 1) * 100 for a, b in zip(vals, vals[1:])]
    avg = sum(e['prev']) / len(e['prev'])
    d1, d4 = (today / e['prev'][-1] - 1) * 100, (today / avg - 1) * 100
    k = lambda v: 'arg-up' if v > 0 else 'arg-down' if v < 0 else ''
    stat = SP.statgrid([('Giá trị khớp', f'{vn(today, 1)} tỷ', ''), ('Khối lượng khớp', f'{vn(e["vol"], 1)} tr CP', ''),
                        ('So với phiên trước', f'{sg(d1)}%', k(d1)), ('So với TB 4 phiên', f'{sg(d4)}%', k(d4)),
                        ('Số mã giao dịch', str(sum(e['breadth'])), ''), ('Tỷ trọng nhóm tăng', f'{vn(e["flow"][0] / today * 100, 1)}%', '')]).replace('class="arg-statgrid__grid"', 'class="arg-statgrid__grid" style="--cols:2"')
    ch = IP.fchart(list(SESS), vals, lambda v: vn(v, 1), [('Giá trị khớp (tỷ đồng)', 'k1'), ('So với phiên trước (%)', 'line')], line=chg,
                   fmt_line=lambda v: f'{sg(v, 1)}%', label='Giá trị khớp cùng thời điểm 5 phiên')
    return IP.block('Thanh khoản hôm nay', stat, sub='Đến 10:15, so với cùng giờ phiên trước') + IP.block('Giá trị khớp 5 phiên', ch, sub='Cùng thời điểm 10:15 mỗi phiên · tỷ đồng')


# ---------- khung ----------
def ex_tabs(content, uid):
    """Tabs sàn HOSE, HNX, UPCoM (đồng bộ giữa các chế độ xem). content(ex, p) -> html các khối."""
    head = f'<div class="arg-page__block">{IP.pills("Sàn", [n for _, n in EXCHANGES], fill=True)}</div>'
    panels = ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == 0 else " hidden"}>{content(ex, f"{uid}-{ex}")}</div>' for i, (ex, _) in enumerate(EXCHANGES))
    return f'<div class="arg-page__tabbed" data-arg-tabs data-arg-tabs-sync="market-ex">{head}{panels}</div>'


def overview():
    modes = [('Biến động', lambda ex, p: volatility(ex, p)), ('Khối ngoại', lambda ex, p: side_flow(ex, 'foreign')),
             ('Tự doanh', lambda ex, p: side_flow(ex, 'prop')), ('Thanh khoản', lambda ex, p: liquidity(ex))]
    chips = ''.join(f'<button class="arg-chip-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, (t, _) in enumerate(modes))
    panels = ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == 0 else " hidden"}>{ex_tabs(fn, f"mk{i}")}</div>' for i, (_, fn) in enumerate(modes))
    return (f'<div class="arg-page__tabbed" data-arg-tabs><div class="arg-page__block"><div class="arg-chip-tabs arg-chip-tabs--sm"><div class="arg-chip-tabs__list" role="tablist" aria-label="Chế độ xem">{chips}</div></div></div>'
            f'{panels}</div>')


def plain(head, rows, cols):
    return DP.dtable(head, rows, cols).replace('class="arg-dtable"', 'class="arg-dtable arg-dtable--plain"', 1)


# ---------- Bảng giá và Theo dõi ----------
SORTS = (('def', 'Mặc định'), ('code', 'Mã A đến Z'), ('up', '% tăng nhiều nhất'), ('down', '% giảm nhiều nhất'), ('price', 'Giá cao nhất'), ('vol', 'Khối lượng lớn nhất'))


def sort_tool(sorts=None):
    items = ''.join(f'<button class="arg-menu__item" role="menuitemradio" aria-checked="{"true" if i == 0 else "false"}" data-sort="{k}" type="button">{t}'
                    f'<i data-arg-icon="check" class="end"{"" if i == 0 else " style=\"visibility:hidden\""}></i></button>' for i, (k, t) in enumerate(sorts or SORTS))
    return (f'<div class="arg-dropdown" data-arg-dropdown data-arg-sort><button class="arg-listbar__tool" type="button" aria-haspopup="menu" aria-expanded="false" aria-label="Sắp xếp">{I("sort-ascending")}</button>'
            f'<div class="arg-menu arg-menu--end" role="menu" hidden>{items}</div></div>')


def board_row(r, fav=False):
    """Một dòng của bảng giá: mã và tên, sparkline có đường tham chiếu, giá và phần trăm theo 5 trạng thái; fav thêm nút ngôi sao bỏ theo dõi."""
    k = r.kind
    idt = (f'<a class="arg-quote__id" href="#" data-arg-go="{r.go}" aria-label="Xem thông tin {r.code}"><b>{r.code}</b><span>{r.name}</span></a>' if r.go
           else f'<div class="arg-quote__id"><b>{r.code}</b><span>{r.name}</span></div>')
    star = (f'<button class="arg-fav" type="button" aria-pressed="true" aria-label="Bỏ {r.code} khỏi danh mục theo dõi">'
             f'<span class="arg-fav__on">{I("star-fill")}</span><span class="arg-fav__off">{I("star")}</span></button>') if fav else ''
    grip = (f'<button class="arg-handle" type="button" data-arg-handle aria-label="Đổi thứ tự {r.code}: nhấn giữ rồi kéo, hoặc dùng mũi tên lên xuống">{I("hamburger-menu")}</button>') if fav else ''
    return (f'<li class="arg-quote arg-quote--{k} arg-quote--board{" arg-quote--fav" if fav else ""}{" arg-quote--link" if r.go else ""}" data-code="{r.code}" data-pct="{r.pct}" data-price="{r.price}" data-vol="{r.vol}">'
            f'{grip}{idt}{spark(k, "pb-" + r.code, flat=True)}<div class="arg-quote__price"><b>{vn(r.price)}</b><span class="arg-badge arg-badge--{k}">{sg(r.pct)}%</span></div>'
            f'<span class="arg-quote__vol">{vn(r.vol, 1)} tr</span>{star}</li>')


def priceboard():
    opts = ''.join(f'<option value="{ex}">{n}</option>' for ex, n in EXCHANGES)
    bar = (f'<div class="arg-listbar" data-arg-listbar><div class="arg-listbar__main"><div class="arg-control arg-select"><select class="arg-select-native" data-arg-pane-select aria-label="Sàn giao dịch">{opts}</select>{I("caret-down")}</div></div>'
           f'<div class="arg-listbar__tools">{sort_tool()}</div></div>')
    panes = ''.join(f'<div data-arg-pane="{ex}"{"" if i == 0 else " hidden"}>{qhead("board", "Xu hướng", "Giá (nghìn đ)")}<ul class="arg-quote-list arg-quote-list--card" data-arg-sortable>'
                    f'{"".join(board_row(r) for r in sorted(universe(ex), key=lambda r: r.code))}</ul></div>' for i, (ex, _) in enumerate(EXCHANGES))
    return f'<div class="arg-page__block" data-arg-listbar-scope>{bar}{panes}</div>'


def plain_text(t):
    return unicodedata.normalize('NFD', t.lower().replace('\u0111', 'd')).encode('ascii', 'ignore').decode()


def watch(lists):
    """Tab Theo dõi. lists: [(tên danh mục, [mã])], mã lấy từ sàn HOSE; danh mục không có mã hiện khối gợi ý blue-chip."""
    hose = universe('hose'); by = {r.code: r for r in hose}
    opts = ''.join(f'<option value="w{i}">{n}</option>' for i, (n, _) in enumerate(lists))
    menu = (f'<div class="arg-dropdown" data-arg-dropdown><button class="arg-listbar__tool" type="button" aria-haspopup="menu" aria-expanded="false" aria-label="Tuỳ chọn danh mục">{I("dots-three")}</button>'
            f'<div class="arg-menu arg-menu--end arg-droplist" role="menu" hidden><button class="arg-menu__item arg-droplist__item" role="menuitem" type="button" data-arg-open="watch-new">{I("plus")}Thêm danh sách yêu thích</button><div class="arg-menu__sep"></div>'
            f'<button class="arg-menu__item arg-menu__item--danger arg-droplist__item" role="menuitem" type="button" data-arg-open="watch-clear">{I("trash")}Xoá hết mã</button></div></div>')
    bar = (f'<div class="arg-listbar" data-arg-listbar><div class="arg-listbar__main"><div class="arg-control arg-select"><select class="arg-select-native" data-arg-pane-select aria-label="Danh mục theo dõi">{opts}</select>{I("caret-down")}</div>{menu}</div>'
           f'<div class="arg-listbar__tools">{sort_tool()}<button class="arg-listbar__tool" type="button" data-arg-open="watch-add" aria-label="Thêm mã">{I("plus-circle")}</button></div></div>')
    panes = ''.join(f'<div data-arg-pane="w{i}"{"" if i == 0 else " hidden"}>{qhead("fav", "Xu hướng", "Giá (nghìn đ)")}<ul class="arg-quote-list arg-quote-list--card" data-arg-sortable data-arg-reorder>{"".join(board_row(by[c], True) for c in codes)}</ul></div>' for i, (_, codes) in enumerate(lists))
    cards = ''.join(f'<label class="arg-suggest__card arg-suggest__card--{by[c].kind}"><input type="checkbox" value="{c}"{" checked" if i < 2 else ""}><span class="arg-suggest__code">{c}</span>'
                    f'<span class="arg-suggest__tick">{I("check-circle-fill")}</span><span class="arg-suggest__name">{FULL[c]}</span>'
                    f'<span class="arg-suggest__price"><b>{vn(by[c].price)}</b><span class="arg-badge arg-badge--{by[c].kind}">{sg(by[c].pct)}%</span></span></label>' for i, c in enumerate(('VCB', 'HPG', 'CTG', 'BID')))
    suggest = (f'<div class="arg-suggest" data-arg-suggest hidden><div class="arg-suggest__head"><h3 class="arg-suggest__title">Chưa biết bắt đầu từ đâu?</h3>'
               f'<p class="arg-suggest__text">Chúng tôi chọn sẵn các cổ phiếu blue-chip phổ biến để bạn tham khảo</p></div><div class="arg-suggest__grid">{cards}</div>'
               f'<div class="arg-suggest__actions"><button class="arg-btn arg-btn--text-strong" type="button" data-arg-open="watch-add">Thêm mã khác</button>'
               f'<button class="arg-btn arg-btn--primary" type="button" data-arg-suggest-add>{I("plus-circle")}Thêm vào danh mục<span data-arg-count></span></button></div></div>')
    tpl = ''.join(f'<template data-arg-row="{r.code}">{board_row(r, True)}</template>' for r in hose)
    results = ''.join(f'<li data-q="{plain_text(r.code + " " + FULL.get(r.code, r.name))}"><span class="arg-suggest__who"><b>{r.code}</b><span>{FULL.get(r.code, r.name)}</span></span>'
                      f'<button class="arg-btn arg-btn--sm arg-btn--outline" type="button" data-arg-add="{r.code}"><span class="arg-suggest__off">{I("plus")}Thêm</span><span class="arg-suggest__on">{I("check")}Đã thêm</span></button></li>'
                      for r in sorted(hose, key=lambda r: r.code))
    sheet = (f'<div class="arg-offcanvas-wrap" id="watch-add" hidden data-arg-offcanvas><aside class="arg-offcanvas arg-offcanvas--bottom arg-suggest__sheet" role="dialog" aria-modal="true" aria-labelledby="watch-add-t">'
             f'<div class="arg-modal__header"><h4 class="arg-modal__title" id="watch-add-t">Thêm mã vào danh mục</h4><button class="arg-icon-btn" type="button" data-arg-close aria-label="Đóng">{I("x", "i--20")}</button></div>'
             f'<div class="arg-modal__body"><div class="arg-control">{I("magnifying-glass")}<input class="arg-input" type="search" enterkeyhint="search" placeholder="Tìm mã, tên công ty" aria-label="Tìm mã" data-arg-suggest-search></div>'
             f'<ul class="arg-suggest__results">{results}</ul><p class="arg-note" data-arg-suggest-none hidden>Không có mã phù hợp.</p></div></aside></div>')
    ptpl = f'<template data-arg-pane-tpl>{qhead("fav", "Xu hướng", "Giá (nghìn đ)")}<ul class="arg-quote-list arg-quote-list--card" data-arg-sortable data-arg-reorder></ul></template>'
    newsheet = (f'<div class="arg-offcanvas-wrap" id="watch-new" hidden data-arg-offcanvas><aside class="arg-offcanvas arg-offcanvas--bottom arg-offcanvas--auto" role="dialog" aria-modal="true" aria-labelledby="watch-new-t">'
                f'<div class="arg-modal__header"><h4 class="arg-modal__title" id="watch-new-t">Tạo danh sách yêu thích mới</h4><button class="arg-icon-btn" type="button" data-arg-close aria-label="Đóng">{I("x", "i--20")}</button></div>'
                f'<div class="arg-modal__body arg-newlist"><label class="arg-field"><span class="arg-label">Tên danh sách</span><div class="arg-control"><input class="arg-input" type="text" enterkeyhint="done" maxlength="30" placeholder="Nhập tên danh sách" aria-label="Tên danh sách" data-arg-newlist-input data-arg-autofocus></div></label>'
                f'<button class="arg-btn arg-btn--primary arg-btn--xl arg-btn--block" type="button" data-arg-newlist-ok disabled>Xác nhận</button></div></aside></div>')
    clear = ('<div class="arg-overlay" id="watch-clear" hidden data-arg-modal><div class="arg-modal arg-modal--sm" role="alertdialog" aria-modal="true" aria-labelledby="watch-clear-t">'
             '<div class="arg-modal__header"><h4 class="arg-modal__title" id="watch-clear-t">Xoá hết mã khỏi danh mục?</h4></div>'
             '<div class="arg-modal__body"><span>Tất cả mã trong danh mục đang chọn sẽ bị bỏ. Bạn có thể thêm lại bất cứ lúc nào.</span></div>'
             '<div class="arg-modal__footer"><button class="arg-btn arg-btn--tertiary" type="button" data-arg-close>Giữ lại</button><button class="arg-btn arg-btn--sell" type="button" data-arg-watch-clear>Xoá hết</button></div></div></div>')
    return f'<div class="arg-page__block arg-watch" data-arg-watch data-arg-listbar-scope>{bar}{panes}{suggest}{tpl}{ptpl}{sheet}{newsheet}{clear}</div>'


SUBS = [  # tiểu khoản mẫu: (id, số tài khoản, loại, {mã: (khối lượng, giá vốn)}, tiền mặt, số danh mục người dùng tạo)
    ('x1', 'C040899 - X1', 'Tiểu khoản thường', {s.code: s.hold for s in STOCKS if s.hold}, 125_000_000),
    ('m1', 'C040899 - M1', 'Tiểu khoản ký quỹ', {'HPG': (3000, 26.00), 'VCB': (500, 90.00)}, 40_000_000),
]
FOLDERS = [('Dài hạn', ['VCB']), ('Lướt sóng', ['HPG']), ('Cổ tức', ['AGR'])]  # danh mục do người dùng tạo, lọc theo mã đang nắm giữ


def acct_menu():
    """Chọn tiểu khoản bằng Select gốc cỡ nhỏ (32px) đặt ở bên phải tiêu đề khối Tài sản; chữ option gồm mã và loại (X1 · Thường, M1 · Ký quỹ), số tài khoản đầy đủ ở dòng phụ của tiêu đề."""
    cap = lambda kind: kind.replace('Tiểu khoản ', '').capitalize()
    opts = ''.join(f'<option value="{sid}" data-sub="{no} · {cap(kind)}">{no.split(" - ")[1]} · {cap(kind)}</option>' for sid, no, kind, _, _ in SUBS)
    return (f'<div class="arg-control arg-control--sm arg-select arg-acct-select"><select class="arg-select-native" data-arg-acct aria-label="Tiểu khoản">{opts}</select>{I("caret-down")}</div>')


def portfolio_pane(sid, no, kind, held, cash):
    """Nội dung của một tiểu khoản: (tóm tắt tài sản gồm dòng tài khoản và 3 thẻ một hàng, cổ phiếu đang nắm giữ gồm chip danh mục và sắp xếp)."""
    by = {x.code: x for x in STOCKS}
    stock = round(sum(by[c].last * q * 1000 for c, (q, _) in held.items())); cost = round(sum(cv * q * 1000 for q, cv in held.values()))
    today = round(sum(by[c].chg * q * 1000 for c, (q, _) in held.items())); total = cash + stock
    pl = stock - cost; pl_pct = pl / cost * 100 if cost else 0; today_pct = today / (total - today) * 100
    tr = lambda v, sign=False: (vn(v / 1e6, 2, True) if sign else vn(v / 1e6, 2)) + ' tr'
    kk = lambda v: 'up' if v > 0 else 'down' if v < 0 else ''
    mc = lambda cls, l, v, sub: f'<div class="arg-metric{cls}"><dt>{l}</dt><dd class="arg-metric__value">{v}</dd><dd class="arg-metric__sub">{sub}</dd></div>'
    stat = ('<dl class="arg-metric-row arg-metric-row--inline">' + mc('', 'Giá trị CP', tr(stock), f'{round(stock / total * 100)}% tài sản')
            + mc(f' arg-metric--{kk(pl)}', 'Lãi/lỗ', tr(pl, True), f'{sg(pl_pct)}%')
            + mc(f' arg-metric--{kk(today)}', 'Hôm nay', tr(today, True), f'{sg(today_pct)}%') + '</dl>')
    cards = {}
    for c, (q, cv) in held.items():
        s = by[c]; p = round((s.last - cv) * q * 1000); pk = 'up' if p > 0 else 'down' if p < 0 else 'ref'
        cards[c] = (f'<li class="arg-holding" data-code="{c}" data-pl="{p}" data-val="{round(s.last * q * 1000)}"><a class="arg-holding__id" href="#" data-arg-go="{s.id}"><b>{c}</b><span class="arg-holding__last {s.cls(s.last)}">{vn(s.last)}</span>'
                    f'<span class="arg-holding__meta">{num(q)} CP · Vốn {vn(cv)}</span></a>'
                    f'<div class="arg-holding__pl"><b class="arg-{pk}">{("+" if p > 0 else "") + num(p)}</b><span class="arg-badge arg-badge--{pk}">{sg((s.last / cv - 1) * 100)}%</span></div></li>')
    groups = [('Tất cả', list(cards))] + [(n, [c for c in codes if c in cards]) for n, codes in FOLDERS if any(c in cards for c in codes)]
    chips = ''.join(f'<button class="arg-chip-tab" type="button" data-arg-pane-tab="pf{i}" aria-pressed="{"true" if i == 0 else "false"}">{n}</button>' for i, (n, _) in enumerate(groups))
    sorts = (('def', 'Mặc định'), ('code', 'Mã A đến Z'), ('pl', 'Lãi nhiều nhất'), ('loss', 'Lỗ nhiều nhất'), ('val', 'Giá trị lớn nhất'))
    bar = (f'<div class="arg-listbar" data-arg-listbar><div class="arg-listbar__main"><div class="arg-chip-tabs"><div class="arg-chip-tabs__list" role="group" aria-label="Danh mục đầu tư">{chips}</div></div></div>'
           f'<div class="arg-listbar__tools">{sort_tool(sorts)}</div></div>')
    panes = ''.join(f'<div data-arg-pane="pf{i}"{"" if i == 0 else " hidden"}><ul class="arg-holding-list" data-arg-sortable>{"".join(cards[c] for c in codes)}</ul></div>' for i, (_, codes) in enumerate(groups))
    return stat, f'{bar}{panes}'


def portfolio():
    """Hai khối cố định, nội dung đổi theo tiểu khoản chọn ở chip cạnh tiêu đề khối Tài sản."""
    done = [portfolio_pane(sid, no, kind, held, cash) for sid, no, kind, held, cash in SUBS]
    assets = IP.title('Tài sản của bạn', sub=f'<span data-arg-acct-sub>{SUBS[0][1]} · {SUBS[0][2].replace("Tiểu khoản ", "").capitalize()}</span>', right=acct_menu())
    stat = ''.join(f'<div class="arg-stack" data-arg-acct-pane="{SUBS[i][0]}"{"" if i == 0 else " hidden"}>{d[0]}</div>' for i, d in enumerate(done))
    held = ''.join(f'<div class="arg-stack" data-arg-acct-pane="{SUBS[i][0]}" data-arg-listbar-scope{"" if i == 0 else " hidden"}>{d[1]}</div>' for i, d in enumerate(done))
    return (f'<div class="arg-page__block">{assets}{stat}</div>'
            + IP.block('Cổ phiếu nắm giữ', held, sub='Giá nghìn đồng · Lãi/lỗ tính theo giá vốn, đơn vị đồng'))


def top_tab():
    return ex_tabs(lambda ex, p: IP.block('Top cổ phiếu', top_lists(ex, 10)), 'tp')


def theme_item(t):
    ic = {'up': 'caret-up-fill', 'down': 'caret-down-fill', 'ref': 'minus'}[t['kind']]
    return (f'<li class="arg-theme" style="--tint:{t["tint"]}"><img class="arg-theme__img" src="assets/themes/{t["slug"]}.jpg" alt="" width="64" height="64">'
            f'<a class="arg-theme__id" href="#" data-arg-go="{t["id"]}"><span class="arg-theme__name">{t["name"]}</span><span class="arg-theme__sub">{t["up"]}/{len(t["rows"])} mã tăng</span></a>'
            f'<span class="arg-badge arg-badge--{t["kind"]}">{I(ic)}{sg(t["avg"]).lstrip("+") if t["avg"] == 0 else sg(t["avg"])}%</span></li>')


def themes():
    data = TM.THEME_DATA
    up, down = sum(t['avg'] > 0 for t in data), sum(t['avg'] < 0 for t in data)
    mc = lambda cls, l, v: f'<div class="arg-metric{cls}"><dt>{l}</dt><dd class="arg-metric__value">{v}</dd></div>'
    stat = '<dl class="arg-metric-row">' + mc(' arg-metric--up', 'Chủ đề tăng', up) + mc(' arg-metric--down', 'Chủ đề giảm', down) + '</dl>'
    lst = '<ul class="arg-theme-list">' + ''.join(theme_item(t) for t in data) + '</ul>'
    return IP.block('Chủ đề thị trường Việt Nam', stat + lst, sub='Khám phá cơ hội đầu tư theo ngành và chủ đề · sàn HOSE, số mẫu')


def theme_screen(t, tabbar_html):
    """Trang chi tiết một chủ đề: ảnh đầu trang, tên và thay đổi, 4 chỉ số, danh sách mã (có sao yêu thích), cơ cấu sở hữu, tin mới."""
    k, rows = t['kind'], t['rows']
    ic = {'up': 'trend-up', 'down': 'trend-down', 'ref': 'minus'}[k]
    cls = {'up': 'arg-up', 'down': 'arg-down', 'ref': 'arg-ref'}[k]
    mc = lambda l, v: f'<div class="arg-metric"><dt>{l}</dt><dd class="arg-metric__value">{v}</dd></div>'
    metrics = ('<dl class="arg-metric-row">' + mc('Vốn hoá', f'{num(t["cap"])} tỷ') + mc('KL khớp', f'{vn(t["vol"], 1)} tr CP') + mc('P/E trung bình', vn(t['pe'], 1)) + mc('P/B trung bình', vn(t['pb'], 1)) + '</dl>')
    head = (f'<div class="arg-theme-head"><div class="arg-title__text" role="heading" aria-level="1">{t["name"]}</div><div class="arg-theme-head__meta">'
            f'<span class="arg-theme-head__chg {cls}">{I(ic)}{sg(t["avg"])}%</span><span>Số mã: {len(rows)}</span></div></div>')
    fav = {'VCB', 'HPG', 'NVL', 'AGR', 'DXG'}   # mã đang nằm trong danh mục theo dõi mẫu
    def srow(r):
        on = 'true' if r.code in fav else 'false'
        idt = (f'<a class="arg-stockrow__id" href="#" data-arg-go="{r.go}" aria-label="Xem thông tin {r.code}"><b>{r.code}</b><span>{r.name}</span></a>' if r.go
               else f'<a class="arg-stockrow__id" href="#"><b>{r.code}</b><span>{r.name}</span></a>')
        star = (f'<button class="arg-fav" type="button" data-arg-fav-toggle aria-pressed="{on}" aria-label="{"Bỏ" if on == "true" else "Thêm"} {r.code} {"khỏi" if on == "true" else "vào"} danh mục theo dõi" '
                f'data-label-on="Bỏ {r.code} khỏi danh mục theo dõi" data-label-off="Thêm {r.code} vào danh mục theo dõi"><span class="arg-fav__on">{I("star-fill")}</span><span class="arg-fav__off">{I("star")}</span></button>')
        return (f'<li class="arg-stockrow">{idt}<div class="arg-stockrow__price"><b class="{KCLS[r.kind]}">{vn(r.price)}</b><span class="arg-badge arg-badge--{r.kind}">{sg(r.pct)}%</span></div>'
                f'<span class="arg-stockrow__vol">{vn(r.vol, 1)}</span>{star}</li>')
    stocks = '<ul class="arg-stockrow-list">' + ''.join(srow(r) for r in rows) + '</ul>'
    segs = ''.join(f'<li class="arg-splitbar__seg" style="--w:{v};--c:var(--arg-viz-{i + 1})"></li>' for i, (_, v) in enumerate(t['own']))
    leg = ''.join(f'<li style="--c:var(--arg-viz-{i + 1})"><i class="arg-splitbar__key"></i>{n}: <b>{vn(v, 1)}%</b></li>' for i, (n, v) in enumerate(t['own']))
    own = f'<div class="arg-splitbar"><ul class="arg-splitbar__bar" role="img" aria-label="Cơ cấu sở hữu của chủ đề {t["name"]}">{segs}</ul><ul class="arg-splitbar__legend">{leg}</ul></div>'
    heads = [f'{t["name"]}: dòng tiền ngoại tập trung vào nhóm vốn hoá lớn', f'Lợi nhuận quý III của nhóm {t["name"].lower()} cải thiện so với cùng kỳ',
             f'Khối lượng khớp nhóm {t["name"].lower()} tăng mạnh trong phiên sáng', f'Điểm tin nhóm {t["name"].lower()}: cổ tức, kế hoạch phát hành mới', f'Chuyên gia nhận định triển vọng nhóm {t["name"].lower()} cuối năm']
    news = '<ul class="arg-news-list arg-news-list--plain">' + ''.join(IP.news_item(h, '29/10/2026', ('Vietstock', 'CafeF', 'Agriseco')[i % 3], i) for i, h in enumerate(heads)) + '</ul>'
    blk = lambda inner: f'<div class="arg-page__block">{inner}</div>'
    return f'''<div class="arg-screen arg-screen--sections" data-arg-screen="{t["id"]}" hidden>
<div class="arg-hero" style="--tint:{t["tint"]}"><div class="arg-hero__bar"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I("caret-left")}</button><button class="arg-appbar__tool" type="button" aria-label="Tìm kiếm">{I("magnifying-glass")}</button></div>
<img class="arg-hero__img" src="assets/themes/{t["slug"]}.jpg" alt="" width="168" height="168"></div>
<main class="arg-page__main">
  {blk(head + metrics)}
  {IP.block("Cổ phiếu trong chủ đề", stocks, sub="Giá nghìn đồng · KL triệu CP")}
  {IP.block("Cơ cấu sở hữu", own)}
  {IP.block("Tin mới nhất", news)}
</main>
{tabbar_html}
</div>'''


def indexes(index_rows):
    rows = [[f'<a class="arg-dtable__link" href="#" data-arg-go="idx-{sid}">{name}</a>', (vn(val), KCLS[k]), (sg(chg), KCLS[k]), (f'{sg(pct)}%', KCLS[k]), vn(tv, 1)]
            for sid, name, val, chg, pct, vol, tv, k, *_ in index_rows]
    return IP.block('Chỉ số', plain(['Chỉ số', 'Điểm', '+/-', '%', 'GTGD (tỷ)'], rows, '1fr 1fr .8fr .8fr 1fr'), sub='Bấm tên chỉ số để xem chi tiết')


def screen(tabbar_html, watch_lists, index_rows):
    tabs = [('Tổng quan', overview()), ('Bảng giá', priceboard()), ('Danh mục', portfolio()), ('Yêu thích', watch(watch_lists)),
            ('Top cổ phiếu', top_tab()), ('Chủ đề', themes()), ('Chỉ số', indexes(index_rows))]
    head = ''.join(f'<button class="arg-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, (t, _) in enumerate(tabs))
    panels = ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == 0 else " hidden"}>{h}</div>' for i, (_, h) in enumerate(tabs))
    return f'''<div class="arg-screen arg-screen--sections" data-arg-screen="market" hidden>
<header class="arg-appbar arg-appbar--sticky"><h1 class="arg-appbar__title">Thị trường</h1><div class="arg-appbar__tools"><button class="arg-appbar__tool" type="button" data-arg-go="search" aria-label="Tìm kiếm">{I('magnifying-glass')}</button></div></header>
<main class="arg-page__main">
  <div class="arg-page__tabbed" data-arg-tabs>
    <div class="arg-page__block arg-page__block--sticky"><div class="arg-tabs arg-tabs--lg"><div class="arg-tablist" role="tablist" aria-label="Thị trường">{head}</div></div></div>
    {panels}
  </div>
</main>
{tabbar_html}
</div>'''
