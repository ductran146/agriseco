"""Markup cho trang chi tiết chỉ số, dựng từ component ARG (pricehead, chart, perf, breadth, dtable, bars, heatmap, podium).
Dùng chung cho ví dụ trong ui/components/* và cho pages/build_pages.py. Dữ liệu là dữ liệu mẫu."""
import json, random

I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'


def vn(x, d=2, sign=False):
    s = f'{abs(x):,.{d}f}'.replace(',', '#').replace('.', ',').replace('#', '.')
    return ('+' if x > 0 else '-' if x < 0 else '') + s if sign else ('-' if x < 0 else '') + s


def pricehead(value, change, pct, vol, val, when, k):
    ic = {'up': 'caret-up-fill', 'down': 'caret-down-fill', 'ref': 'minus'}[k]
    return (f'<div class="arg-pricehead arg-pricehead--{k}"><div class="arg-pricehead__row">'
            f'<div class="arg-pricehead__main"><b class="arg-pricehead__value">{vn(value)}</b>'
            f'<span class="arg-pricehead__change"><span>{I(ic)}{vn(abs(change))}</span><span>{vn(pct, 2, True)}%</span></span></div>'
            f'<dl class="arg-pricehead__side"><dt>KLGD</dt><dd>{vn(vol)} tr</dd><dt>GTGD</dt><dd>{vn(val)} tỷ</dd></dl></div>'
            f'<span class="arg-pricehead__meta">{I("clock")}{when}</span></div>')


def candles(seed, k, n=44, ref=0.5):
    r = random.Random(seed)
    p = 0.55 if k != 'down' else 0.45
    drift = {'up': -0.004, 'down': 0.004, 'ref': 0.0}[k]
    rows = []
    for i in range(n):
        o = p
        c = max(0.12, min(0.88, o + r.uniform(-0.05, 0.05) + drift + (0.02 * (r.random() - .5))))
        h = max(o, c) + r.uniform(0.005, 0.035)
        l = min(o, c) - r.uniform(0.005, 0.035)
        v = r.uniform(.2, 1) * (1.3 if abs(c - o) > .04 else 1)
        rows.append((o, h, l, c, v)); p = c
    return rows


def chart(seed, k, sel=24, n=44, base=1300, rng=0, rows=None, opts=None):
    """rows: nến [mở, cao, thấp, đóng, khối lượng 0..1] tự cấp (giá thật, sẽ chuẩn hoá); opts: thuộc tính data-* thêm cho __plot (span, vol, vol-unit, start, end)."""
    W, H, VH = 330, 160, 40
    rows = rows or candles(seed, k, n); n = len(rows)
    lo, hi = min(r[2] for r in rows), max(r[1] for r in rows)
    rows = [tuple((x - lo) / (hi - lo) * .84 + .08 for x in r[:4]) + (r[4],) for r in rows]
    step = W / n
    cx = lambda i: step * (i + .5)
    y = lambda v: H - v * H
    g = ''
    vb = ''
    pts = ' '.join(f'{cx(i):.1f},{y(r[3]):.1f}' for i, r in enumerate(rows))
    for i, (o, h, l, c, v) in enumerate(rows):
        cls = 'up' if c >= o else 'down'
        top, bot = y(max(o, c)), y(min(o, c))
        g += (f'<g class="{cls}"><line x1="{cx(i):.1f}" y1="{y(h):.1f}" x2="{cx(i):.1f}" y2="{y(l):.1f}"/>'
              f'<rect x="{cx(i) - step * .32:.1f}" y="{top:.1f}" width="{step * .64:.1f}" height="{max(1.5, bot - top):.1f}"/></g>')
        vb += f'<rect class="{cls}" x="{cx(i) - step * .32:.1f}" y="{VH - v * VH:.1f}" width="{step * .64:.1f}" height="{v * VH:.1f}"/>'
    data = json.dumps([[round(x, 4) for x in r] for r in rows], separators=(',', ':'))
    price = (f'<svg class="arg-chart__price" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">'
             f'<line class="cur cur--y" x1="0" y1="0" x2="{W}" y2="0"/><line class="cur cur--x" x1="0" y1="0" x2="0" y2="{H}"/>'
             f'<g class="arg-chart__candles">{g}</g><g class="arg-chart__line"><polygon points="{cx(0):.1f},{H} {pts} {cx(n - 1):.1f},{H}"/><polyline points="{pts}"/></g></svg>')
    vol = (f'<svg class="arg-chart__vol" viewBox="0 0 {W} {VH}" preserveAspectRatio="none" aria-hidden="true">'
           f'<line class="cur cur--x" x1="0" y1="0" x2="0" y2="{VH}"/>{vb}</svg>')
    return (f"<div class=\"arg-chart arg-chart--{k}\" data-arg-chart><div class=\"arg-chart__plot\" data-base=\"{base}\" data-date=\"29/10/2026\"{''.join(f' data-{a}="{v}"' for a, v in (opts or {}).items())} data-candles='{data}'>"
            f'<div class="arg-chart__tip" hidden></div><span class="arg-chart__tag" hidden></span><span class="arg-chart__dot" hidden></span>{price}{vol}</div>{chart_range(sel=rng)}</div>')


RANGES = (('1N', '1 ngày'), ('1T', '1 tuần'), ('1Th', '1 tháng'), ('3Th', '3 tháng'), ('1Nm', '1 năm'), ('5Nm', '5 năm'))


def chart_range(labels=RANGES, sel=0):
    b = ''.join(f'<button class="arg-chip-tab" role="tab" type="button" aria-label="{full}" aria-selected="{"true" if i == sel else "false"}">{short}</button>' for i, (short, full) in enumerate(labels))
    return (f'<div class="arg-chart__range"><div class="arg-chip-tabs arg-chip-tabs--xs" data-arg-tabs><div class="arg-chip-tabs__list" role="tablist" aria-label="Khoảng thời gian">{b}</div></div>'
            f'<span class="arg-chart__tools"><button class="arg-icon-btn" type="button" data-arg-chart-mode aria-label="Chuyển sang biểu đồ đường">{I("wave-sine")}</button>'
            f'<button class="arg-icon-btn" type="button" aria-label="Toàn màn hình">{I("arrows-out-simple")}</button></span></div>')


def perf_row(items):
    return '<div class="arg-perf-row">' + ''.join(
        f'<div class="arg-perf"><span class="arg-perf__label">{t}</span><span class="arg-badge arg-badge--{k}">{I("caret-up-fill" if k == "up" else "caret-down-fill")}{vn(abs(p))}%</span></div>'
        for t, p, k in items) + '</div>'


def breadth(up, ref, down):
    def it(k, ic, label, n): return (f'<div class="arg-breadth__item arg-breadth__item--{k}"><span class="arg-breadth__icon">{I(ic)}</span>'
                                    f'<span class="arg-breadth__label">{label}</span><b class="arg-breadth__value">{n}<small> mã</small></b></div>')
    return ('<div class="arg-breadth">' + it('up', 'trend-up', 'Giá tăng', up) + it('ref', 'minus', 'Giá đứng', ref) + it('down', 'trend-down', 'Giá giảm', down) + '</div>')


def dtable(head, rows, cols):
    h = f'<div class="arg-dtable__row arg-dtable__row--head" role="row">' + ''.join(f'<span role="columnheader">{c}</span>' for c in head) + '</div>'
    body = ''
    for r in rows:
        body += '<div class="arg-dtable__row" role="row">' + ''.join(f'<span role="cell"{f" class=\"{c[1]}\"" if isinstance(c, tuple) else ""}>{c[0] if isinstance(c, tuple) else c}</span>' for c in r) + '</div>'
    return f'<div class="arg-dtable" role="table" style="--cols:{cols}">{h}{body}</div>'


def bars(items, fmt=None, label='Giá trị mua ròng theo phiên', dense=False):
    m = max(abs(v) for _, v in items)
    out = ''
    for d, v in items:
        pct = abs(v) / m * 100
        lab = fmt(v) if fmt else f'{"+" if v > 0 else "-"}{abs(v)}tr'
        if v >= 0:
            pos = f'<span class="arg-bar__val arg-up">{lab}</span><span class="arg-bar__fill arg-bar__fill--up" style="--v:{pct:.0f}"></span>'; neg = ''
        else:
            pos = ''; neg = f'<span class="arg-bar__fill arg-bar__fill--down" style="--v:{pct:.0f}"></span><span class="arg-bar__val arg-down">{lab}</span>'
        out += f'<div class="arg-bar"><div class="arg-bar__half arg-bar__half--pos">{pos}</div><div class="arg-bar__half arg-bar__half--neg">{neg}</div><span class="arg-bar__date">{d}</span></div>'
    return f'<div class="arg-bars{" arg-bars--dense" if dense else ""}" style="--n:{len(items)}" role="img" aria-label="{label}">{out}</div>'


HEAT = [('VCB', '0,56', 'up', '1/5/1/5'), ('TPB', '0,56', 'ceil', '1/5/5/9'), ('CTG', '0,00', 'ref', '5/11/1/3'), ('TCB', '0,56', 'up', '11/13/1/3'),
        ('GAS', '0,56', 'ceil', '5/9/3/5'), ('VHM', '0,56', 'floor', '9/13/3/5'), ('MBB', '-0,56', 'down', '5/7/5/9'), ('MSN', '0,56', 'up', '7/9/5/7'),
        ('ACB', '-0,56', 'down', '9/11/5/7'), ('VIC', '-0,56', 'down', '11/13/5/7'), ('MWG', '0,56', 'up', '7/9/7/9'), ('STB', '0,56', 'up', '9/11/7/9'), ('VIB', '0,56', 'up', '11/13/7/9')]


def heatmap():
    t = ''
    for code, pct, k, a in HEAT:
        c0, c1, r0, r1 = a.split('/')
        t += f'<div class="arg-heat__tile arg-heat__tile--{k}" style="grid-column:{c0}/{c1};grid-row:{r0}/{r1}"><b>{code}</b><span>{pct}%</span></div>'
    return f'<div class="arg-heat" role="img" aria-label="Bản đồ nhiệt các mã vốn hoá lớn">{t}</div>'


def podium(items):
    """items: [(code, pct)] theo thứ tự hạng 1, 2, 3; hiển thị 2 - 1 - 3."""
    def it(rank, code, pct):
        return (f'<div class="arg-podium__item arg-podium__item--{rank}"><span class="arg-podium__rank">{I("medal")}</span>'
                f'<b class="arg-podium__code">{code}</b><span class="arg-podium__pct arg-up">+ {pct}%</span><span class="arg-podium__bar"></span></div>')
    a, b, c = items
    return f'<div class="arg-podium">{it(2, *b)}{it(1, *a)}{it(3, *c)}</div>'
