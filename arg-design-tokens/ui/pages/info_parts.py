"""Markup cho các tab Tin tức, Sự kiện, Tài chính, Doanh nghiệp, Kỹ thuật của trang thông tin mã, dựng từ component ARG:
title (thu gọn khối), news, events, accordion, kv, statgrid, tabs, fchart, donut, dtable, badge, gauge. Dữ liệu mẫu trong company.py."""
import ring as RING
import detail_parts as DP
from company import Company, verdict, vnf, pct, dong, WEEK, RANGE

I = DP.I


# ---------- chung ----------
def title(text, cid=None, sub=None, right=''):
    """Tiêu đề khối; cid: id vùng .arg-collapse để nút mũi tên thu gọn cả khối."""
    tool = (f'<button class="arg-title__tool arg-collapse-toggle" type="button" data-arg-collapse aria-controls="{cid}" aria-expanded="true" '
            f'aria-label="Thu gọn hoặc mở {text}">{I("caret-down")}</button>') if cid else ''
    s = f'<span class="arg-title__sub">{sub}</span>' if sub else ''
    return (f'<div class="arg-title arg-title--md{" arg-title--stacked" if sub else ""}"><div class="arg-title__left"><div class="arg-title__main">'
            f'<div class="arg-title__text" role="heading" aria-level="2">{text}</div>{s}</div></div>'
            + (f'<div class="arg-title__right">{right}{tool}</div>' if (tool or right) else '') + '</div>')


def block(text, body, cid=None, sub=None):
    """Một khối trắng có tiêu đề; có cid thì nội dung nằm trong .arg-collapse (mở sẵn) để thu gọn."""
    inner = f'<div class="arg-stack">{body}</div>'
    if cid: inner = f'<div class="arg-collapse is-open" id="{cid}"><div>{inner}</div></div>'
    return f'<div class="arg-page__block">{title(text, cid, sub)}{inner}</div>'


def pills(label, items, fill=False, sel=0):
    b = ''.join(f'<button class="arg-tab" role="tab" type="button" aria-selected="{"true" if i == sel else "false"}">{t}</button>' for i, t in enumerate(items))
    return f'<div class="arg-tabs arg-tabs--pill{" arg-tabs--fill" if fill else ""}"><div class="arg-tablist" role="tablist" aria-label="{label}">{b}</div></div>'


def tabset(label, items, sel=0):
    """Tabs --pill chia đều kèm các tabpanel. items: [(nhãn, html)]."""
    panels = ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == sel else " hidden"}>{h}</div>' for i, (_, h) in enumerate(items))
    return f'<div class="arg-stack" data-arg-tabs>{pills(label, [t for t, _ in items], fill=True, sel=sel)}{panels}</div>'


def kv(rows):
    return '<dl class="arg-kv arg-kv--lines">' + ''.join(f'<div class="arg-kv__row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'


# ---------- Tin tức ----------
NEWS_IMGS = 10  # ảnh minh hoạ mẫu: pages/news/news-1.webp ... news-10.webp (ảnh stock miễn phí, chưa gắn với nội dung bài; xem news.md)


def news_thumb(i=0):
    return f'<img class="arg-news-item__img" src="assets/news/news-{i % NEWS_IMGS + 1}.webp" alt="" width="88" height="64" loading="lazy" decoding="async">'


def news_item(t, dt, src, i=0, rank=None):
    lead = f'<span class="arg-news-item__rank">{rank}</span>' if rank else f'<span class="arg-news-item__thumb">{news_thumb(i)}</span>'
    cls = 'arg-news-item arg-news-item--rank' if rank else 'arg-news-item arg-news-item--thumb'
    return (f'<li><a class="{cls}" href="#">{lead}<span class="arg-news-item__body"><span class="arg-news-item__title">{t}</span>'
            f'<span class="arg-news-item__meta">{dt} · <b>{src}</b></span></span></a></li>')


def more_button(cid):
    return (f'<button class="arg-collapse-more" type="button" data-arg-collapse aria-controls="{cid}" aria-expanded="false">'
            f'<span class="arg-collapse-more__open">Xem thêm</span><span class="arg-collapse-more__close">Thu gọn</span>{I("caret-down")}</button>')


def news_tab(st, c):
    n, p = c.news(), st.code.lower()
    ul = lambda items, start=0: '<ul class="arg-news-list arg-news-list--plain">' + ''.join(news_item(*x, i=start + k) for k, x in enumerate(items)) + '</ul>'
    latest = (f'<div class="arg-page__block">{ul(n[:5])}<div class="arg-collapse" id="{p}-news-more"><div>{ul(n[5:10], 5)}</div></div>{more_button(p + "-news-more")}</div>')
    ranked = '<ul class="arg-news-list arg-news-list--plain">' + ''.join(news_item(*x, rank=k + 1) for k, x in enumerate([n[0], n[3], n[2], n[4], n[7]])) + '</ul>'
    return latest + block('Đọc nhiều nhất', ranked, f'{p}-news-top') + block('Xu hướng', ul(n[10:15], 2), f'{p}-news-trend')


# ---------- Sự kiện ----------
def events_tab(st, c):
    p, ev = st.code.lower(), c.events()
    # Ô ngày dùng Datepicker: hiển thị dd/mm/yyyy (định dạng Việt Nam), giá trị chuẩn ở data-iso
    field = lambda key, lab, val: (f'<div class="arg-field"><label class="arg-label" for="{p}-ev-{key}">{lab}</label><div class="arg-control arg-datepicker__field">'
                                   f'<input class="arg-input" id="{p}-ev-{key}" type="text" value="{val.strftime("%d/%m/%Y")}" data-iso="{val.isoformat()}" data-arg-datepicker data-arg-events-{key}>{I("calendar-blank")}</div></div>')
    counts = ('<div class="arg-statgrid"><dl class="arg-statgrid__grid" style="--cols:2">'
              '<div class="arg-statgrid__item"><dt>Sự kiện cổ tức</dt><dd data-arg-events-count="dividend">0</dd></div>'
              '<div class="arg-statgrid__item"><dt>Trong tuần này</dt><dd data-arg-events-count="week">0</dd></div></dl></div>')
    items = ''
    for k, (kind, dt, name, rows) in enumerate(ev):
        cid, open_ = f'{p}-ev-{k}', WEEK[0] <= dt <= WEEK[1]
        items += (f'<div class="arg-accordion" data-date="{dt.isoformat()}" data-type="{kind}"><div class="arg-accordion__item"><h3 class="arg-accordion__head">'
                  f'<button class="arg-accordion__btn" type="button" data-arg-collapse aria-expanded="{str(open_).lower()}" aria-controls="{cid}"><span>{name}<small>{dt.strftime("%d/%m/%Y")}</small></span>{I("caret-down")}</button></h3>'
                  f'<div class="arg-collapse{" is-open" if open_ else ""}" id="{cid}" role="region"><div>{kv(rows)}</div></div></div></div>')
    return (f'<div class="arg-page__block"><div class="arg-events" data-arg-events data-week-start="{WEEK[0].isoformat()}" data-week-end="{WEEK[1].isoformat()}">'
            f'<div class="arg-events__range">{field("from", "Từ ngày", RANGE[0])}{field("to", "Đến ngày", RANGE[1])}</div>{counts}'
            f'<div class="arg-accordion-list">{items}</div><p class="arg-events__empty" data-arg-events-empty hidden>Không có sự kiện trong khoảng ngày đã chọn.</p></div></div>')


# ---------- Tài chính ----------
def fchart(periods, s1, fmt1, legend, s2=None, fmt2=None, line=None, fmt_line=None, line_color=True, pn=False, label='', line_range=None, kinds=None, bins=False):
    """Biểu đồ cột (1 hoặc 2 chuỗi, hoặc âm dương) và đường % theo trục riêng. legend: [(tên, 'k1'|'k2'|'line'|'pos')].
    line_range: (min, max) cố định cho trục đường (ví dụ 0..100 cho tỷ lệ), mặc định theo dữ liệu."""
    n = len(periods); w = 100 / n
    vals = s1 + (s2 or [])
    lo, hi = min(0, min(vals)), max(0, max(vals)); span = (hi - lo) or 1
    y = lambda v: 6 + (hi - v) / span * 90
    rects = ''
    def bar(cls, x, v, bw):
        # cột HTML (không co giãn theo khung) để bo góc đúng bán kính; cột âm bo phía dưới
        return f'<span class="arg-fchart__bar {cls}{" arg-fchart__bar--neg" if v < 0 else ""}" style="left:{x:.2f}%;top:{min(y(v), y(0)):.2f}%;width:{bw:.2f}%;height:{max(.6, abs(y(v) - y(0))):.2f}%"></span>'
    for i, v in enumerate(s1):
        if s2 is None:
            bw = w * .42; x = i * w + (w - bw) / 2
            cls = kinds[i] if kinds else ('pos' if v >= 0 else 'neg') if pn else 's1'
            rects += bar(cls, x, v, bw)
        else:
            bw = w * .3
            for cls, vv, x in (('s1', v, i * w + w / 2 - bw - .5), ('s2', s2[i], i * w + w / 2 + .5)):
                rects += bar(cls, x, vv, bw)
    poly, dots = '', ''
    if line:
        pts = [(i, v) for i, v in enumerate(line) if v is not None]
        if pts:
            llo, lhi = line_range or (min(v for _, v in pts), max(v for _, v in pts)); ls = (lhi - llo) or 1
            ly = lambda v: 14 + (lhi - v) / ls * 72
            poly = '<polyline class="line" points="' + ' '.join(f'{(i + .5) * w:.2f},{ly(v):.2f}' for i, v in pts) + '"/>'
            dots = ''.join(f'<span class="arg-fchart__dot" style="left:{(i + .5) * w:.2f}%;top:{ly(v):.2f}%"></span>' for i, v in pts)
    svg = (f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><line class="base" x1="0" y1="{y(0):.2f}" x2="100" y2="{y(0):.2f}"/>{poly}</svg>')
    cols = ''
    for i, per in enumerate(periods):
        cell = f'<span class="arg-fchart__period">{per}</span><b>{fmt1(s1[i])}</b>'
        if s2 is not None: cell += f'<span class="s2">{fmt2(s2[i])}</span>'
        if line:
            lv = line[i]
            cls = ('arg-up' if lv and lv > 0 else 'arg-down' if lv and lv < 0 else '') if line_color else ''
            cell += f'<span class="{cls}">{fmt_line(lv) if lv is not None else "–"}</span>'
        cols += f'<div class="arg-fchart__col">{cell}</div>'
    keys = {'k1': '<i class="arg-fchart__key"></i>', 'k2': '<i class="arg-fchart__key" style="--c:var(--arg-viz-2)"></i>', 'line': '<i class="arg-fchart__key arg-fchart__key--line"></i>',
            'pos': '<i class="arg-fchart__key" style="--c:var(--arg-trading-up-light-increase)"></i>', 'neg': '<i class="arg-fchart__key" style="--c:var(--arg-trading-down-light-increase)"></i>'}
    leg = ('<ul class="arg-fchart__legend">' + ''.join(f'<li>{keys[k]}{t}</li>' for t, k in legend) + '</ul>') if legend else ''
    return (f'<div class="arg-fchart{" arg-fchart--bins" if bins else ""}" style="--n:{n}" role="img" aria-label="{label}"><div class="arg-fchart__plot">{svg}{rects}{dots}</div>'
            f'<div class="arg-fchart__cols">{cols}</div>{leg}</div>')


def fin_panel(st, c, mode):
    p, per = f'{st.code.lower()}-{mode}', [x[0] for x in c.periods(mode)]
    yo = lambda v: f'{"+" if v > 0 else ""}{vnf(v, 1)}%'
    one = lambda key, name, fmt, unit: fchart(per, c.series(key, mode)[0], fmt, [(f'{name} ({unit})', 'k1'), ('So với cùng kỳ (%)', 'line')],
                                              line=c.series(key, mode)[1], fmt_line=yo, label=f'{name} theo kỳ')
    perf = tabset('Chỉ tiêu', [('ROE', one('roe', 'ROE', pct, '%')), ('ROA', one('roa', 'ROA', pct, '%')), ('EPS', one('eps', 'EPS 4 quý', dong, 'đ'))])
    inc = tabset('Chỉ tiêu', [('Lợi nhuận', one('ni', 'Lợi nhuận ròng', dong, 'tỷ đồng')),
                              ('Doanh thu' if not c.p['bank'] else 'Thu nhập', one('rev', 'Doanh thu' if not c.p['bank'] else 'Tổng thu nhập hoạt động', dong, 'tỷ đồng')),
                              ('Trước thuế', one('opp', 'Lợi nhuận trước thuế', dong, 'tỷ đồng'))])
    a, l = c.series('assets', mode)[0], c.series('liab', mode)[0]
    bal = fchart(per, a, dong, [('Tổng tài sản', 'k1'), ('Nợ phải trả', 'k2'), ('Nợ / Tài sản (%)', 'line')], s2=l, fmt2=dong,
                 line=[x / y * 100 for x, y in zip(l, a)], fmt_line=lambda v: vnf(v, 1) + '%', line_color=False, line_range=(0, 100), label='Tổng tài sản và nợ phải trả theo kỳ')
    cf = lambda key, name: fchart(per, c.series(key, mode)[0], dong, [(f'{name} dương', 'pos'), (f'{name} âm', 'neg')], pn=True, label=f'Lưu chuyển tiền {name.lower()}')
    cash = tabset('Hoạt động', [('Kinh doanh', cf('cfo', 'Kinh doanh')), ('Đầu tư', cf('cfi', 'Đầu tư')), ('Tài chính', cf('cff', 'Tài chính'))])
    unit = 'Đơn vị: tỷ đồng · ' + ('5 quý gần nhất' if mode == 'q' else '5 năm gần nhất')
    return (block('Hiệu quả tài chính', perf, f'{p}-perf') + block('Kết quả kinh doanh', inc, f'{p}-inc', sub=unit)
            + block('Cân đối kế toán', bal, f'{p}-bal', sub=unit) + block('Lưu chuyển tiền tệ', cash, f'{p}-cf', sub=unit))


def financial_tab(st, c):
    p = st.code.lower()
    head = (f'<div class="arg-page__block"><div class="arg-title arg-title--sm"><div class="arg-title__left"><div class="arg-title__main"><div class="arg-title__text">Xem theo</div></div></div>'
            f'<div class="arg-title__right">{pills("Kỳ báo cáo", ["Quý", "Năm"])}</div></div></div>')
    period = (f'<div class="arg-page__tabbed" data-arg-tabs>{head}<div class="arg-tabpanel" role="tabpanel">{fin_panel(st, c, "q")}</div>'
              f'<div class="arg-tabpanel" role="tabpanel" hidden>{fin_panel(st, c, "y")}</div></div>')
    ratios = ''.join(block(name, kv(rows), f'{p}-ratio-{k}', sub='4 quý gần nhất' if k == 0 else None) for k, (name, rows) in enumerate(c.ratios))
    return period + ratios


# ---------- Doanh nghiệp ----------
VIZ = ['var(--arg-viz-1)', 'var(--arg-viz-2)', 'var(--arg-viz-3)', 'var(--arg-viz-4)', 'var(--arg-viz-5)', 'var(--arg-viz-6)']


def donut(rows, label, side=False):
    """rows: [(tên, %, số CP hoặc chuỗi phụ)] theo thứ tự lớn đến nhỏ; side: biểu đồ bên trái, chú giải bên phải."""
    seg, off = '', 0
    for k, (nm, pc, _) in enumerate(rows):
        seg += RING.seg(VIZ[k], off, pc, nm, vnf(pc, 1) + '%')
        off += pc
    top = rows[0]
    leg = ''.join(f'<li style="--c:{VIZ[k]}"><i class="arg-donut__key"></i><span class="arg-donut__name">{n}</span><span class="arg-donut__pct">{vnf(pc)}%</span>'
                  f'<span class="arg-donut__sub">{sh if isinstance(sh, str) else dong(sh) + " CP"}</span></li>' for k, (n, pc, sh) in enumerate(rows))
    return (f'<div class="arg-donut{" arg-donut--side" if side else ""}"><div class="arg-donut__chart" role="img" aria-label="{label}"><svg viewBox="0 0 42 42" aria-hidden="true">'
            f'<circle class="bg" cx="21" cy="21" r="15.915" pathLength="100"/>{seg}</svg><div class="arg-donut__center"><b>{vnf(top[1], 1)}%</b><span>{top[0]}</span></div></div>'
            f'<ul class="arg-donut__legend">{leg}</ul></div>')


def company_tab(st, c):
    p = st.code.lower()
    intro = (f'<div class="arg-page__block">{title(f"{st.code} - {c.p["full"]}").replace("arg-title arg-title--md", "arg-title arg-title--md arg-title--wrap", 1)}<p class="arg-clamp" id="{p}-desc">{c.p["desc"]}</p>{more_button(p + "-desc")}</div>')
    rows = [[f'<b>{nm}</b><small>{role}</small>', dt, f'<span class="arg-badge arg-badge--{side}">{"Mua" if side == "buy" else "Bán"}</span><small>{dong(v)}</small>']
            for nm, role, dt, side, v in c.insiders()]
    ins = DP.dtable(['Người giao dịch', 'Ngày', 'Loại / KL'], rows, '1.6fr 1fr 1fr').replace('class="arg-dtable"', 'class="arg-dtable arg-dtable--plain"', 1)
    return (intro + block('Cơ cấu sở hữu', donut(c.ownership(), 'Cơ cấu sở hữu theo nhóm cổ đông'), f'{p}-own')
            + block('Cổ đông lớn', donut(c.major(), 'Tỷ lệ nắm giữ của cổ đông lớn'), f'{p}-major')
            + block('Giao dịch nội bộ', ins, f'{p}-insider') + block('Thông tin niêm yết', kv(c.listing()), f'{p}-listing'))


# ---------- Kỹ thuật ----------
ZONES = (('Bán mạnh', 162), ('Bán', 126), ('Trung lập', 90), ('Mua', 54), ('Mua mạnh', 18))


def gauge(vd):
    import math
    zones = ''.join(f'<path class="zone z{k + 1}" d="M 70 140 A 90 90 0 0 1 250 140" pathLength="100" stroke-dasharray="19.2 100" stroke-dashoffset="{-(k * 20 + .4):.1f}"/>' for k in range(5))
    labels = ''
    for name, a in ZONES:
        x, yy = 160 + 112 * math.cos(math.radians(a)), 140 - 112 * math.sin(math.radians(a))
        anchor = 'end' if a > 100 else 'start' if a < 80 else 'middle'
        labels += f'<text x="{x:.1f}" y="{yy:.1f}" text-anchor="{anchor}" dominant-baseline="middle">{name}</text>'
    dial = (f'<svg class="arg-gauge__dial" viewBox="0 0 320 160" role="img" aria-label="Tín hiệu {vd["word"].lower()}: {vd["sell"]} bán, {vd["neutral"]} trung lập, {vd["buy"]} mua">'
            f'{zones}{labels}<g class="arg-gauge__needle"><line x1="160" y1="140" x2="160" y2="66"/><circle cx="160" cy="140" r="5"/></g></svg>')
    counts = (f'<dl class="arg-gauge__counts"><div><dt>Bán</dt><dd class="arg-sell">{vd["sell"]}</dd></div><div><dt>Trung lập</dt><dd>{vd["neutral"]}</dd></div>'
              f'<div><dt>Mua</dt><dd class="arg-buy">{vd["buy"]}</dd></div></dl>')
    return f'<div class="arg-gauge" style="--v:{vd["v"]}">{dial}<b class="arg-gauge__verdict {vd["cls"]}">{vd["word"].upper()}</b>{counts}</div>'


def signal_table(rows):
    lab = {'buy': ('Mua', 'arg-buy'), 'sell': ('Bán', 'arg-sell'), 'neutral': ('Trung lập', '')}
    body = [[n, v, (lab[s][0], lab[s][1]) if lab[s][1] else lab[s][0]] for n, v, s in rows]
    return DP.dtable(['Chỉ báo', 'Giá trị', 'Tín hiệu'], body, '1.6fr 1fr 1fr').replace('class="arg-dtable"', 'class="arg-dtable arg-dtable--plain"', 1)


def technical_tab(st, c):
    osc, ma = c.technical()
    p = st.code.lower()
    sets = tabset('Nhóm chỉ báo', [('Tổng hợp', gauge(verdict(osc + ma))), ('Dao động', gauge(verdict(osc)) + signal_table(osc)),
                                   ('Đường MA', gauge(verdict(ma)) + signal_table(ma))])
    return block('Tín hiệu kỹ thuật', sets, sub='Khung ngày · cập nhật 10:15 29/10/2026')


TABS = (('Tin tức', news_tab), ('Sự kiện', events_tab), ('Tài chính', financial_tab), ('Doanh nghiệp', company_tab), ('Kỹ thuật', technical_tab))


def panels(st):
    c = Company(st)
    return [(name, fn(st, c)) for name, fn in TABS]
