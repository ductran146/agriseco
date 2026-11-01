"""Dựng trang chủ từ component ARG và khung xem Mobile / Tablet.
Chạy sau ui/build.py:  python3 -I ui/pages/build_pages.py
Ra: ui/dist/arg-home.html (trang chủ độc lập), ui/dist/arg-home-preview.html (khung xem có chọn thiết bị)."""
import base64, json, math, random, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import detail_parts as DP
import trade_parts as TP
import stock_parts as SP
import account_parts as AP
import info_parts as IP
import market_parts as MP
import themes as TM
import orderbook_parts as OB
import search_parts as SRP
import asset_parts as AST
from specs import specs_for
from spark import spark
from stocks import STOCKS, BY_CODE

UI = Path(__file__).resolve().parent.parent
D = UI / 'dist'
I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'


def title(text, action=None, tool=None):
    right = ''
    if action: right = f'<div class="arg-title__right"><button class="arg-title__action" type="button">{action}{I("caret-right")}</button></div>'
    if tool: right = f'<div class="arg-title__right"><button class="arg-title__tool" type="button" aria-label="{tool}">{I("caret-right")}</button></div>'
    return f'<div class="arg-title arg-title--md"><div class="arg-title__left"><div class="arg-title__main"><div class="arg-title__text" role="heading" aria-level="2">{text}</div></div></div>{right}</div>'


def index(name, val, pct, k, s, sid=None):
    return (f'<a class="arg-index arg-index--{k}" href="#" data-arg-go="idx-{sid}" aria-label="Xem chi tiết {name}"><div class="arg-index__head"><span class="arg-index__name">{name}</span><b class="arg-index__value">{val}</b>'
            f'<span class="arg-index__badge">{pct}</span></div>{spark(k, s)}</a>')


def quote(code, name, price, pct, k, s, vol, go=None):
    """go: id màn thông tin mã; có thì cả dòng bấm được (Quote --link)."""
    idt = f'<a class="arg-quote__id" href="#" data-arg-go="{go}" aria-label="Xem thông tin {code}"><b>{code}</b><span>{name}</span></a>' if go else f'<div class="arg-quote__id"><b>{code}</b><span>{name}</span></div>'
    return (f'<li class="arg-quote arg-quote--{k}{" arg-quote--link" if go else ""}">{idt}{spark(k, s)}'
            f'<div class="arg-quote__price"><b>{price}</b><span class="arg-badge arg-badge--{k}">{pct}</span></div><span class="arg-quote__vol">{vol}</span></li>')


def news(t, d, s, thumb=False):
    th = f'<span class="arg-news-item__thumb">{I("image", "i--24")}</span>' if thumb else ''
    return (f'<li><a class="arg-news-item{" arg-news-item--thumb" if thumb else ""}" href="#">{th}<span class="arg-news-item__body">'
            f'<span class="arg-news-item__title">{t}</span><span class="arg-news-item__meta">{d} · <b>{s}</b></span></span></a></li>')


def chips(label, items):
    b = ''.join(f'<button class="arg-chip-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, t in enumerate(items))
    return f'<div class="arg-chip-tabs__list" role="tablist" aria-label="{label}">{b}</div>'


def qrow(code, spark_seed):
    """Dòng danh mục theo dõi lấy số từ stocks.py; bấm mở trang thông tin của mã."""
    st = BY_CODE[code]
    return (code, st.name, DP.vn(st.last), f'{DP.vn(st.pct, 2, True)}%', st.kind, spark_seed, f'{DP.vn(st.vol / 1e6, 1)} tr', st.id)


QUOTES = [qrow('AGR', 1), qrow('HPG', 2), qrow('VIC', 3), qrow('MSN', 4), qrow('NVL', 5), qrow('VCB', 6)]
SERVICES = [('chart-line-duotone', 'Sổ lệnh'), ('piggy-bank-duotone', 'Nộp tiền'), ('bank-duotone', 'Chuyển khoản'), ('receipt-duotone', 'Sao kê tiền'), ('download-simple-duotone', 'Lưu ký'), ('upload-simple-duotone', 'Rút lưu ký')]
NEWS = [('Thị trường phiên sáng đi ngang, dòng tiền phân hoá', '29/10/2026', 'Agriseco'), ('Khối ngoại quay lại mua ròng nhóm ngân hàng', '29/10/2026', 'Vietstock'),
        ('Lợi nhuận quý III của nhóm bất động sản cải thiện', '28/10/2026', 'CafeF'), ('Điểm tin chứng khoán đầu tuần', '28/10/2026', 'Tin nhanh')]
account = AP.account()

LOGO = re.sub(r'\s+', ' ', (UI / 'pages/logo-agriseco.svg').read_text().replace('width="78" height="80" ', 'class="arg-logo" aria-hidden="true" ', 1)).strip()

# (nhãn, loại, mã, lãi/lỗ %, số để sắp xếp, giá mục tiêu): mua thì mục tiêu trên giá hiện tại, bán thì dưới, giữ thì sát giá
RECO = [('B', 'sell', 'CTG', '7,25', '-7.25', '32,00'), ('M', 'buy', 'VCB', '7,25', '7.25', '105,00'), ('G', 'hold', 'BID', '7,25', '0.1', '41,50'), ('M', 'buy', 'VCB', '7,25', '7.25', '105,00'), ('B', 'sell', 'CTG', '7,25', '-7.25', '32,00')]
RECO_NAME = {'sell': 'Nên bán', 'buy': 'Nên mua', 'hold': 'Nên giữ'}


def reco_card(name='Chuyên viên phân tích khuyến nghị'):
    rows = ''.join(f'<div class="arg-reco__item arg-reco__item--link" data-pl="{p}"><a class="arg-reco__sym" href="#" data-arg-go="{BY_CODE[t].id}" aria-label="Xem thông tin {t}"><span class="arg-rating arg-rating--{k}" aria-label="{RECO_NAME[k]}">{l}</span>{t}</a><span class="arg-reco__pl">{pl}%</span><span>{tg}</span></div>' for l, k, t, pl, p, tg in RECO)
    return (f'<div class="arg-reco"><a class="arg-reco__head" href="#"><span>{name}</span>{I("caret-right")}</a>'
            f'<div class="arg-reco__cols"><span></span><button class="arg-reco__sort" type="button" aria-sort="none">Lãi/lỗ<span class="arg-reco__arrows">{I("caret-up-fill")}{I("caret-down-fill")}</span></button><span>Giá mục tiêu</span></div>'
            f'<div class="arg-reco__body">{rows}</div></div>')


RECO_LEGEND = '<ul class="arg-rating-legend">' + ''.join(f'<li><span class="arg-rating arg-rating--sm arg-rating--{k}">{l}</span>{RECO_NAME[k]}</li>' for l, k in (('B', 'sell'), ('G', 'hold'), ('M', 'buy'))) + '</ul>'


# ---- trang chi tiết chỉ số: (id, tên, giá, thay đổi, %, KLGD tr, GTGD tỷ, trạng thái, seed, (tăng, đứng, giảm), hiệu suất)
INDEXES = [
    ('vn30', 'VN30', 1312.07, 5.36, 0.41, 184.7, 5092.3, 'up', 21, (18, 3, 9), [('7 ngày', 1.04, 'up'), ('1 tháng', -1.04, 'down'), ('1 năm', 12.30, 'up'), ('5 năm', 38.60, 'up')]),
    ('hnx30', 'HNX30', 598.42, -2.46, -0.41, 41.3, 823.1, 'down', 22, (11, 4, 15), [('7 ngày', -0.62, 'down'), ('1 tháng', 1.80, 'up'), ('1 năm', 6.10, 'up'), ('5 năm', -4.20, 'down')]),
    ('hnx', 'HNX', 234.85, 0.0, 0.0, 87.2, 1523.7, 'ref', 23, (96, 70, 94), [('7 ngày', 0.12, 'up'), ('1 tháng', -0.45, 'down'), ('1 năm', 3.20, 'up'), ('5 năm', 9.80, 'up')]),
    ('upcom', 'UPCoM', 98.15, 0.22, 0.22, 156.4, 1102.8, 'up', 24, (210, 150, 130), [('7 ngày', 0.56, 'up'), ('1 tháng', 2.04, 'up'), ('1 năm', -1.30, 'down'), ('5 năm', 21.40, 'up')]),
]
TOP = ['DIG', 'MWG', 'SSI', 'VIX', 'VND', 'CTG', 'BID', 'SHN', 'HPG', 'VCB']


def seg(label, items):
    b = ''.join(f'<button class="arg-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, t in enumerate(items))
    return f'<div class="arg-tabs arg-tabs--pill" data-arg-tabs><div class="arg-tablist" role="tablist" aria-label="{label}">{b}</div></div>'


def panels(items, first_hidden=False):
    return ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == 0 else " hidden"}>{h}</div>' for i, h in enumerate(items))


def netbuy(sid):
    foreign = DP.dtable(['', 'Mua', 'Bán', 'Ròng'], [['KL', '3.468.357', '4.680.123', ('-1.211.766', 'arg-down')], ['GT', '97 tỷ', '99 tỷ', ('-2 tỷ', 'arg-down')]], '.45fr 1fr 1fr 1fr')
    allm = DP.dtable(['', 'Mua', 'Bán', 'Ròng'], [['KL', '184.470.000', '181.920.000', ('+2.550.000', 'arg-up')], ['GT', '5.092 tỷ', '4.981 tỷ', ('+111 tỷ', 'arg-up')]], '.45fr 1.1fr 1.1fr 1fr')
    b1 = DP.bars([('18/06', 28), ('19/06', 14), ('20/06', -28), ('21/06', -19), ('27/06', 57)])
    b2 = DP.bars([('18/06', 120), ('19/06', -64), ('20/06', 88), ('21/06', 35), ('27/06', -42)])
    n1 = '<p class="arg-note">Trong 5 phiên giao dịch gần nhất, khối ngoại đã mua ròng <b class="arg-up">109 tỷ đồng</b>.</p>'
    n2 = '<p class="arg-note">Trong 5 phiên giao dịch gần nhất, toàn thị trường mua ròng <b class="arg-up">137 tỷ đồng</b>.</p>'
    return (f'<div class="arg-chip-tabs" data-arg-tabs>{chips("Đối tượng", ["Khối ngoại", "Toàn thị trường"])}'
            + panels([f'<div class="arg-stack">{foreign}{b1}{n1}</div>', f'<div class="arg-stack">{allm}{b2}{n2}</div>']) + '</div>')


def topstocks(seed):
    r = random.Random(seed)
    def one(k):
        codes = r.sample(TOP, 8); pcts = sorted((round(r.uniform(1.2, 23.7), 2) for _ in range(8)), reverse=True)
        rows = [[c, (f'+{DP.vn(p)}%', 'arg-up'), DP.vn(r.uniform(14, 90)), DP.vn(r.uniform(14, 90)), f'{r.randint(100, 999) * 1000 + r.randint(0, 999):,}'.replace(',', '.')] for c, p in zip(codes[3:], pcts[3:])]
        return f'<div class="arg-stack">{DP.podium([(codes[0], DP.vn(pcts[0])), (codes[1], DP.vn(pcts[1])), (codes[2], DP.vn(pcts[2]))])}{DP.dtable(["Mã", "%", "Mở cửa", "Hiện tại", "Giá trị"], rows, ".9fr .9fr 1fr 1fr 1.4fr")}</div>'
    return (f'<div class="arg-chip-tabs" data-arg-tabs>{chips("Tiêu chí", ["Giá trị", "Khối lượng", "Khối ngoại mua ròng"])}'
            + panels([one(0), one(1), one(2)]) + '</div>')


def detail(d):
    sid, name, val, chg, pct, vol, tv, k, seed, br, perf = d
    return f'''<div class="arg-screen arg-screen--sections" data-arg-screen="idx-{sid}" hidden>
<header class="arg-appbar arg-appbar--sticky arg-appbar--condense" data-arg-condense=".arg-pricehead"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I('caret-left')}</button><div class="arg-appbar__stack"><h1 class="arg-appbar__title">{name}</h1><div class="arg-appbar__info" aria-hidden="true"><span class="arg-appbar__name">{name}</span><div class="arg-appbar__quote arg-{k}"><b>{DP.vn(val)}</b><span>{I({'up': 'caret-up-fill', 'down': 'caret-down-fill', 'ref': 'minus'}[k])}{DP.vn(abs(chg))} ({DP.vn(pct, 2, True)}%)</span></div></div></div><div class="arg-appbar__tools"><button class="arg-appbar__tool" type="button" data-arg-fav-toggle aria-pressed="false" aria-label="Thêm {name} vào danh mục theo dõi" data-label-on="Bỏ {name} khỏi danh mục theo dõi" data-label-off="Thêm {name} vào danh mục theo dõi"><span class="arg-fav__on">{I('star-fill')}</span><span class="arg-fav__off">{I('star')}</span></button><button class="arg-appbar__tool" type="button" aria-label="Chia sẻ">{I('share-network')}</button></div></header>
<main class="arg-page__main">
  <div class="arg-page__block">{DP.pricehead(val, chg, pct, vol, tv, 'Phiên liên tục 10:15 29/10/2026', k)}{DP.chart(seed, k, base=val)}</div>
  <div class="arg-page__block">{DP.perf_row(perf)}{DP.breadth(*br)}</div>
  <div class="arg-page__cols">
    <div class="arg-page__block">{title('Giá trị mua ròng 5 phiên')}{netbuy(sid)}</div>
    <div class="arg-page__block">{title('Bản đồ nhiệt', tool='Xem tất cả')}{DP.heatmap()}</div>
  </div>
  <div class="arg-page__block">{title('Top cổ phiếu', tool='Xem tất cả')}{topstocks(seed)}</div>
</main>
</div>'''

TABS = [('house-duotone', 'Trang chủ', 'home'), ('chart-line-duotone', 'Thị trường', 'market'), ('arrows-left-right-duotone', 'Giao dịch', 'trade'), ('wallet-duotone', 'Tài sản', 'asset'), ('squares-four-duotone', 'Thêm', None)]


def tabbar(active):
    items = ''.join(f'<a class="arg-tabbar__item" href="#"{f" data-arg-go=\"{go}\" data-arg-root" if go else ""}{" aria-current=\"page\"" if i == active else ""}>{I(ic)}<span>{t}</span></a>' for i, (ic, t, go) in enumerate(TABS))
    return f'<nav class="arg-tabbar arg-tabbar--fixed" aria-label="Điều hướng chính">{items}</nav>'


def seg_tabs(items, cls=''):
    b = ''.join(f'<button class="arg-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, t in enumerate(items))
    return f'<div class="arg-tabs{cls}" data-arg-tabs><div class="arg-tablist" role="tablist" aria-label="Loại lệnh">{b}</div>' + ''.join(f'<div class="arg-tabpanel" role="tabpanel"{"" if i == 0 else " hidden"}></div>' for i, _ in enumerate(items)) + '</div>'


def trade_screen(st):
    """Màn đặt lệnh của một mã. VCB là màn gốc 'trade' của thanh tab Giao dịch; mã khác mở từ nút Mua, Bán trên trang thông tin mã."""
    return f'''<div class="arg-screen arg-screen--plain" data-arg-screen="{st.trade_id}" data-mode="pro" hidden>
<header class="arg-appbar arg-appbar--sticky">{TP.acctsel()}<div class="arg-appbar__tools"><button class="arg-appbar__tool" type="button" data-arg-go="orderbook" aria-label="Sổ lệnh">{I('calendar-check')}</button><button class="arg-appbar__tool" type="button" aria-label="Tài sản">{I('chart-pie-slice')}</button></div></header>
<main class="arg-page__main arg-page__main--dense arg-page__main--fit">
  {TP.symbol(st.code, st.ex)}
  {TP.quote_head(st)}
  {TP.stats(st)}
  <div class="arg-trade--pro">{TP.order_panel(st)}</div>
  <div class="arg-trade--lite">{TP.lite_panel(st)}</div>
</main>
{tabbar(2)}
{TP.order_modals()}
{TP.depth_sheet(st)}
{TP.type_sheet()}
</div>'''


def stock_screen(st):
    """Trang thông tin một mã, mở khi bấm mã ở trang chủ hoặc Thông tin CP ở màn đặt lệnh."""
    extra = IP.panels(st)
    names = ['Thông tin giao dịch'] + [n for n, _ in extra]
    tabs = ''.join(f'<button class="arg-chip-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{n}</button>' for i, n in enumerate(names))
    more = ''.join(f'<div class="arg-tabpanel" role="tabpanel" hidden>{h}</div>' for _, h in extra)
    return f'''<div class="arg-screen arg-screen--sections" data-arg-screen="{st.id}" hidden>
{SP.appbar(st)}
<main class="arg-page__main">
  <div class="arg-page__block">{SP.symbol_bar(st)}{SP.price(st)}{SP.holding(st)}{SP.stats(st)}</div>
  <div class="arg-page__tabbed" data-arg-tabs>
    <div class="arg-page__block"><div class="arg-chip-tabs"><div class="arg-chip-tabs__list" role="tablist" aria-label="Nội dung">{tabs}</div></div></div>
    <div class="arg-tabpanel" role="tabpanel">
      <div class="arg-page__block">{SP.chart(st)}</div>
      <div class="arg-page__block">{title('Bước giá')}{SP.depth(st)}</div>
      <div class="arg-page__block">{title('Giao dịch khối ngoại')}{SP.foreign(st)}</div>
      {SP.netbuy_block(st)}
      <div class="arg-page__block">{title('Khớp lệnh', tool='Xem tất cả')}{SP.ticks(st)}</div>
    </div>
    {more}
  </div>
</main>
{SP.actionbar(st)}
</div>'''


# Danh mục theo dõi của tab Theo dõi: ba danh mục giống Trang chủ, thêm một danh mục mới còn trống
WATCH = [('Của tôi', [q[0] for q in QUOTES[:5]]), ('Xây dựng', [QUOTES[1][0], QUOTES[4][0]]), ('Tài chính', [QUOTES[0][0], QUOTES[5][0], QUOTES[3][0]]), ('Danh mục mới', [])]
MARKET = MP.screen(tabbar(1), WATCH, INDEXES)

HOME = f'''<div class="arg-screen" data-arg-screen="home">
<header class="arg-appbar arg-appbar--sticky"><h1 class="arg-appbar__logo" aria-label="Agriseco">{LOGO}</h1><div class="arg-appbar__tools"><button class="arg-appbar__tool" type="button" data-arg-go="search" aria-label="Tìm kiếm">{I('magnifying-glass')}</button><button class="arg-appbar__tool" type="button" aria-label="Tài khoản">{I('user')}</button><button class="arg-appbar__tool" type="button" aria-label="Thông báo">{I('bell')}</button></div></header>
<main class="arg-page__main">
  <div class="arg-promo"><span class="arg-promo__media">{I('chart-bar')}</span><div class="arg-promo__body"><span class="arg-promo__title">Giao dịch chứng khoán ngay trên điện thoại</span><span class="arg-promo__text">Cài đặt ứng dụng Agriseco để đặt lệnh nhanh.</span></div><button class="arg-promo__close" type="button" data-arg-dismiss=".arg-promo" aria-label="Đóng">{I('x')}</button></div>
  <div class="arg-index-row">{index('VN30', '1.312,07', '+0,41%', 'up', 11, 'vn30')}{index('HNX30', '598,42', '-0,41%', 'down', 12, 'hnx30')}{index('HNX', '234,85', '0,00%', 'ref', 13, 'hnx')}{index('UPCoM', '98,15', '+0,22%', 'up', 14, 'upcom')}</div>
  <div class="arg-page__cols">
    <div class="arg-page__block">{account}</div>
    <div class="arg-page__block">{title('Dịch vụ yêu thích', action='Tuỳ chỉnh')}<div class="arg-service-grid arg-service-grid--card">{''.join(f'<a class="arg-service" href="#"><span class="arg-service__icon">{I(i)}</span><span class="arg-service__label">{t}</span></a>' for i, t in SERVICES)}</div></div>
  </div>
  <div class="arg-page__block">{title('Khuyến nghị', tool='Xem tất cả')}
    <div class="arg-reco-row">{reco_card()}{reco_card()}</div>
    {RECO_LEGEND}
  </div>
  <div class="arg-page__cols">
    <div class="arg-page__block">{title('Danh mục theo dõi', tool='Xem tất cả')}
      <div class="arg-chip-tabs" data-arg-tabs>{chips('Danh mục', ['Của tôi', 'Xây dựng', 'Tài chính'])}
        <div class="arg-tabpanel" role="tabpanel"><ul class="arg-quote-list">{''.join(quote(*q) for q in QUOTES[:5])}</ul></div>
        <div class="arg-tabpanel" role="tabpanel" hidden><ul class="arg-quote-list">{''.join(quote(*q) for q in (QUOTES[1], QUOTES[4]))}</ul></div>
        <div class="arg-tabpanel" role="tabpanel" hidden><ul class="arg-quote-list">{''.join(quote(*q) for q in (QUOTES[0], QUOTES[5], QUOTES[3]))}</ul></div></div></div>
    <div class="arg-page__block">{title('Tin tức', tool='Xem tất cả')}
      <div class="arg-chip-tabs" data-arg-tabs>{chips('Tin tức', ['Mới nhất', 'Danh mục'])}
        <div class="arg-tabpanel" role="tabpanel"><ul class="arg-news-list">{news(*NEWS[0], thumb=True)}{''.join(news(*n) for n in NEWS[1:])}</ul></div>
        <div class="arg-tabpanel" role="tabpanel" hidden><ul class="arg-news-list">{''.join(news(*n) for n in NEWS[2:])}</ul></div></div></div>
  </div>
</main>
{tabbar(0)}
</div>'''

# Mỗi màn hình một file: (id, html, tên hiển thị)
SCREENS = ([('home', HOME, 'Trang chủ'), ('market', MARKET, 'Thị trường'), ('orderbook', OB.screen(tabbar(2)), 'Sổ lệnh'), ('search', SRP.screen(), 'Tìm kiếm'), ('asset', AST.screen(tabbar(3)), 'Tài sản')]
           + [(st.trade_id, trade_screen(st), f'Giao dịch {st.code}') for st in STOCKS]
           + [(st.id, stock_screen(st), f'Thông tin {st.code}') for st in STOCKS]
           + [(f'idx-{d[0]}', detail(d), f'Chỉ số {d[1]}') for d in INDEXES]
           + [(t['id'], MP.theme_screen(t, tabbar(1)), f"Chủ đề {t['name']}") for t in TM.THEME_DATA]
           + [(OB.order_id(o), OB.detail_screen(o), f'Lệnh {o[2]} {o[1][:5]}') for o in OB.ORDERS])

BG = re.search(r'--arg-p-neutral-50:\s*(#[0-9a-fA-F]{6})', (D / 'arg-tokens.css').read_text()).group(1)  # nền trang, khớp --arg-ui-background-background
def no_hover(src):
    """Demo mobile không có con trỏ: bỏ mọi selector :hover khỏi CSS của trang demo (thư viện dist/arg-ui.css vẫn giữ hover cho viewer)."""
    import re
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    def rule(m):
        keep = [x for x in m.group(1).split(',') if ':hover' not in x]
        return (','.join(keep) + '{' + m.group(2) + '}') if keep else ''
    return re.sub(r'([^{}]+)\{([^{}]*)\}', rule, src)


SHELL = r'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="theme-color" content="#ffffff" id="tc"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Agriseco"><title>__TITLE__</title><link rel="stylesheet" href="assets/arg.css"><script>var THEME = 'light'; try { THEME = sessionStorage.getItem('arg-theme') || (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? 'dark' : 'light'); } catch (e) {} document.documentElement.setAttribute("data-theme", THEME);</script>
<style>
:root { --brand: var(--arg-p-brand-header-start); --brand2: var(--arg-p-brand-header-end); --bg: color-mix(in srgb, var(--brand) 5%, var(--arg-ui-background-surface)); --ink: var(--arg-ui-text-on-bright-text-title); --line: var(--arg-ui-divider-stroke); --on: var(--arg-ui-state-layer-on-bright-hovered); --onc: var(--arg-action-text-button-link-text-button); }
:root[data-theme="dark"] { color-scheme: dark; }
* { box-sizing: border-box; } body { margin: 0; background: var(--bg); color: var(--ink); font: var(--arg-font-font-weight-regular) var(--arg-font-font-size-body-4)/var(--arg-font-line-height-body-4) var(--arg-font-family-family); height: 100vh; display: flex; flex-direction: column; }
.bar { display: flex; justify-content: center; align-items: center; gap: var(--arg-space-2x); flex-wrap: wrap; padding: var(--arg-space-3x) var(--arg-gutter); background: var(--arg-ui-background-surface); border-bottom: 1px solid var(--line); }
.bar button { --h: var(--arg-border-height-size-height-normal); display: inline-flex; align-items: center; gap: var(--arg-space-2x); height: var(--h); padding: 0 var(--arg-space-4x); border: 1px solid var(--line); border-radius: var(--arg-radius-control); background: transparent; color: var(--ink); font: var(--arg-font-font-weight-medium) var(--arg-font-font-size-body-4)/var(--arg-font-line-height-body-4) var(--arg-font-family-family); cursor: pointer; }
.bar button:hover { background: var(--on); } .bar button[aria-pressed="true"]:hover { background: var(--arg-gradient-primary-button); }
.bar button:focus-visible { outline: 2px solid var(--onc); outline-offset: 2px; }
.bar button .ic { width: 20px; height: 20px; fill: currentColor; }
.bar button[aria-pressed="true"] { background: var(--arg-gradient-primary-button); border-color: transparent; color: #fff; }
.stage { flex: 1; min-height: 0; overflow: hidden; display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: start; column-gap: 24px; padding: 24px 16px; }
.devwrap { grid-column: 2; position: relative; }
.stage { position: relative; }
/* Danh sách màn hình: cột sát mép trái trình duyệt, dạng cây (mục lớn, thư mục gập được, màn có icon đánh dấu), ô tìm ở trên, màn đang xem là nút tối */
.nav { position: absolute; z-index: 3; left: 0; top: 0; bottom: 0; width: 260px; display: flex; flex-direction: column; box-sizing: border-box; padding: var(--arg-space-4x) var(--arg-space-3x) var(--arg-space-3x); border-right: 1px solid color-mix(in srgb, var(--brand) 12%, var(--arg-ui-background-surface)); background: color-mix(in srgb, var(--brand) 2%, var(--arg-ui-background-surface)); color: var(--arg-ui-text-on-bright-text-content); font: var(--arg-font-font-weight-regular) var(--arg-font-font-size-body-4)/var(--arg-font-line-height-body-4) var(--arg-font-family-family); overflow: hidden; }
.nav .arg-control { flex: none; margin: 0 0 var(--arg-space-4x); }
.nav .tree { flex: 1; min-height: 0; overflow: auto; scrollbar-width: none; margin: 0 -4px; padding: 0 4px; }
.nav .tree::-webkit-scrollbar { display: none; }
.nav h2 { display: flex; align-items: center; gap: var(--arg-space-2x); margin: 0 0 var(--arg-space-1x); padding: var(--arg-space-1x); font: var(--arg-font-font-weight-bold) var(--arg-font-font-size-body-4)/var(--arg-font-line-height-body-4) var(--arg-font-family-family); text-transform: uppercase; letter-spacing: .02em; color: var(--arg-ui-text-on-bright-text-content-lv2); cursor: pointer; }
.nav .ic { flex: none; width: 18px; height: 18px; fill: currentColor; }
.nav .chev { margin-left: auto; margin-right: 2px; transition: transform .15s; } .nav details[open] > summary .chev, .nav:not([data-closed]) h2 .chev { transform: rotate(180deg); }
.nav .bend { width: 14px; height: 14px; opacity: .55; }
.nav details { margin: 0; } .nav summary { display: flex; align-items: center; gap: var(--arg-space-2x); padding: var(--arg-space-1-5x) var(--arg-space-1x); border-radius: var(--arg-radius-xs); cursor: pointer; list-style: none; color: var(--arg-ui-text-on-bright-text-title); }
.nav summary::-webkit-details-marker { display: none; } .nav summary .open { display: none; } .nav details[open] > summary .open { display: block; } .nav details[open] > summary .shut { display: none; }
.nav ul { list-style: none; margin: 0 0 var(--arg-space-1x); padding: 0 0 0 10px; display: grid; gap: 1px; }
.nav a { display: flex; align-items: center; gap: var(--arg-space-2x); padding: var(--arg-space-1-5x) var(--arg-space-2x); border-radius: var(--arg-radius-xs); color: inherit; text-decoration: none; }
.nav a span { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.nav a:hover, .nav summary:hover { background: var(--arg-ui-state-layer-on-bright-hovered); }
.nav a[aria-current="page"] { background: var(--arg-ui-text-on-bright-text-content); color: var(--arg-ui-background-surface); font-weight: var(--arg-font-font-weight-semibold); }
.nav [hidden] { display: none; }
/* Ghi chú bên phải: cột sát mép phải trình duyệt, cùng kiểu và nền với danh sách màn hình bên trái */
.info { position: absolute; z-index: 3; right: 0; top: 0; bottom: 0; width: 300px; overflow: auto; scrollbar-width: none; box-sizing: border-box; padding: var(--arg-space-4x); border-left: 1px solid color-mix(in srgb, var(--brand) 12%, var(--arg-ui-background-surface)); background: color-mix(in srgb, var(--brand) 2%, var(--arg-ui-background-surface)); font-size: var(--arg-font-font-size-body-4); line-height: var(--arg-font-line-height-body-4); }
.info::-webkit-scrollbar { display: none; }
.info .tag { display: inline-flex; align-items: center; gap: 6px; padding: 0; background: none; color: var(--onc); font-size: var(--arg-font-font-size-label-1); font-weight: var(--arg-font-font-weight-semibold); letter-spacing: .04em; text-transform: uppercase; }
.info .tag::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--brand); }
.info h2 { margin: 6px 0 4px; font: var(--arg-font-font-weight-bold) var(--arg-font-font-size-title-3)/var(--arg-font-line-height-title-3) var(--arg-font-family-family); }
.info p { margin: 0 0 10px; color: var(--arg-ui-text-on-bright-text-content-lv2); }
.info h3 { margin: 0 0 4px; padding-top: 10px; border-top: 1px dashed var(--line); font: var(--arg-font-font-weight-semibold) var(--arg-font-font-size-label-1)/var(--arg-font-line-height-label-1) var(--arg-font-family-family); text-transform: uppercase; letter-spacing: .04em; color: var(--arg-ui-text-on-bright-text-content-lv2); }
.info ul { color: var(--arg-ui-text-on-bright-text-content); margin: 0 0 10px; padding: 0 0 0 16px; display: grid; gap: 3px; }
.info li::marker { color: var(--brand); }
.info li[hidden] { display: none; }
.info .more { margin: 0 0 10px; padding: 0; border: 0; background: none; color: var(--onc); font: inherit; font-weight: var(--arg-font-font-weight-semibold); cursor: pointer; }
@media (max-width: 1000px) { .info, .nav { display: none; } .stage { display: flex; justify-content: center; } .all { display: inline; } }
body[data-d="full"] .info { display: none; }
.dev { position: relative; flex: none; transform-origin: top left; background: var(--arg-ui-background-surface); border-radius: 28px; box-shadow: var(--arg-shadow-soft-shadow); overflow: hidden; }
.dev iframe { display: block; width: 100%; height: 100%; border: 0; }
body[data-d="full"] .stage { display: block; padding: 0; } body[data-d="full"] .nav { display: none; } body[data-d="full"] .dev { border-radius: 0; box-shadow: none; }
.sbar { position: absolute; top: 0; left: 0; right: 0; z-index: 2; height: 44px; display: flex; justify-content: space-between; pointer-events: none; color: var(--arg-ui-text-on-bright-text-title); }
.sb-time { position: absolute; top: 0; left: 0; width: 127px; height: 44px; display: grid; place-items: center; padding-top: 3px; font: var(--arg-font-font-weight-semibold) 17px/1 var(--arg-font-family-family); letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
.sbar svg { display: block; flex: none; }
.hind { position: absolute; left: 50%; bottom: 8px; z-index: 2; width: 134px; height: 5px; margin-left: -67px; border-radius: 100px; background: var(--arg-ui-text-on-bright-text-title); pointer-events: none; }
body[data-d="full"] .hind { display: none; }
body[data-d="full"] .sbar { display: none; }
/* Xem trên điện thoại (cửa sổ hẹp): chỉ hiện giao diện prototype toàn màn hình, không thanh công cụ, khung thiết bị, danh sách màn, ghi chú, đặc tả */
body[data-bare] { height: 100vh; height: 100dvh; } body[data-bare] .bar, body[data-bare] .spec-layer, body[data-bare] .nav, body[data-bare] .info { display: none; }
.all { display: none; align-self: center; margin-left: var(--arg-space-2x); color: var(--onc); font-size: var(--arg-font-font-size-body-4); text-decoration: none; }
.spec-sw, .theme-sw { margin-left: var(--arg-space-3x); padding-left: var(--arg-space-4x); border-left: 1px solid var(--line); font: var(--arg-font-font-weight-medium) var(--arg-font-font-size-body-4)/var(--arg-font-line-height-body-4) var(--arg-font-family-family); color: var(--ink); }
.theme-sw + .spec-sw { margin-left: var(--arg-space-4x); padding-left: 0; border-left: 0; }
body[data-d="full"] .spec-sw { display: none; } @media (max-width: 1000px) { .spec-sw { display: none; } }
/* Lớp đặc tả kiểu ghi chú Figma: chấm đánh số trên thành phần, đường nét đứt nối tới bong bóng nằm ở hai bên khung thiết bị */
.spec-layer { position: absolute; inset: 0; z-index: 2; pointer-events: none; }
.spec-layer svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.spec-layer path { fill: none; stroke: var(--brand); stroke-width: 1.5; stroke-dasharray: 4 3; opacity: .85; }
.spec-layer path.in { stroke-dasharray: none; opacity: .6; }
.spec-dot { position: absolute; width: 8px; height: 8px; margin: -4px 0 0 -4px; border-radius: 50%; background: var(--brand); border: 2px solid #fff; box-sizing: border-box; }
.spec-pin { position: absolute; display: grid; place-items: center; width: 20px; height: 20px; margin: -10px 0 0 -10px; border-radius: 50%; background: var(--brand); color: #fff; font: var(--arg-font-font-weight-bold) 11px/1 var(--arg-font-family-family); box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 25%, transparent); }
.spec-note { position: absolute; display: flex; gap: var(--arg-space-2x); box-sizing: border-box; padding: var(--arg-space-2-5x) var(--arg-space-3x); border-radius: var(--arg-radius); background: var(--arg-ui-background-surface); color: var(--arg-ui-text-on-bright-text-title); box-shadow: var(--arg-shadow-sharp-shadow); font: var(--arg-font-font-weight-regular) var(--arg-font-font-size-label-1)/var(--arg-font-line-height-label-1) var(--arg-font-family-family); pointer-events: auto; }
.spec-note i { flex: none; display: grid; place-items: center; width: 18px; height: 18px; border-radius: 50%; background: var(--brand); color: #fff; font: var(--arg-font-font-weight-bold) 10px/1 var(--arg-font-family-family); font-style: normal; }
.spec-box { position: absolute; border: 1.5px dashed var(--brand); border-radius: 6px; background: color-mix(in srgb, var(--brand) 8%, transparent); opacity: 0; transition: opacity .12s; }
.spec-box.on { opacity: 1; }
.lbl { align-self: center; color: var(--arg-ui-text-on-bright-text-content-lv2); font-size: var(--arg-font-font-size-label-1); margin-left: var(--arg-space-2x); }
</style></head><body data-d="mobile">
<div class="bar" role="toolbar" aria-label="Chọn thiết bị">
  <button type="button" data-d="mobile" aria-pressed="true">__IC_MOBILE__Mobile</button>
  <button type="button" data-d="tablet" aria-pressed="false">__IC_TABLET__Tablet</button>
  <label class="arg-check arg-switch theme-sw"><span>Chế độ tối</span><input type="checkbox" role="switch" id="theme-toggle" aria-label="Chuyển giao diện sáng hoặc tối"><span class="track"></span></label>
  <label class="arg-check arg-switch spec-sw"><span>Đặc tả</span><input type="checkbox" role="switch" id="spec-toggle" aria-label="Hiện hoặc ẩn đặc tả trên giao diện"><span class="track"></span></label>
  <span class="lbl" id="lbl"></span><a class="all" href="index.html" id="all">Tất cả màn hình</a>
</div>
<div id="safe" aria-hidden="true" style="position:fixed;left:0;top:0;width:0;height:0;visibility:hidden;padding:env(safe-area-inset-top, 0px) 0 env(safe-area-inset-bottom, 0px)"></div>
<div class="stage" id="stage">__NAV__<div class="spec-layer" id="spec"></div><div class="devwrap" id="devwrap"><div class="dev" id="dev">__SB__<div class="hind" aria-hidden="true"></div><iframe id="fr" aria-label="__TITLE__" srcdoc="__PAGE__"></iframe></div></div><aside class="info" id="info" aria-live="polite"></aside></div>
<script>
(function () {
  var S = { mobile: [375, 812], tablet: [768, 1068] }, st = document.getElementById('stage'), dev = document.getElementById('dev'), wrap = document.getElementById('devwrap'), info = document.getElementById('info'), nav = document.querySelector('.nav'), cur = (location.hash.match(/d=(mobile|tablet|full)/) || [])[1] || 'mobile', START = '__ID__';
  var sbt = document.getElementById('sbtime');
  function tick() { var n = new Date(); sbt.textContent = String(n.getHours()).padStart(2, '0') + ':' + String(n.getMinutes()).padStart(2, '0'); }
  tick(); setInterval(tick, 15000);
  var fr = document.getElementById('fr'), BARE = matchMedia('(max-width: 600px)'), tt = document.getElementById('theme-toggle');
  if (cur === 'full') cur = 'mobile';
  tt.checked = THEME === 'dark';
  function theme() { try { fr.contentDocument.documentElement.setAttribute('data-theme', THEME); } catch (e) {} }
  tt.addEventListener('change', function () { THEME = tt.checked ? 'dark' : 'light'; document.documentElement.setAttribute('data-theme', THEME); try { sessionStorage.setItem('arg-theme', THEME); } catch (e) {} theme(); tint(); });
  function safe(d) { try { var st = fr.contentDocument.documentElement.style, p = getComputedStyle(document.getElementById('safe')); st.setProperty('--arg-safe-top', d === 'full' ? (BARE.matches ? p.paddingTop : '0px') : '44px'); st.setProperty('--arg-safe-bottom', d === 'full' ? (BARE.matches ? p.paddingBottom : '0px') : '34px'); } catch (e) {} }
  /* Xem trên điện thoại: màu vùng ngoài (thanh trạng thái, vùng kéo quá mép) trùng nền của ứng dụng */
  function tint() { if (!BARE.matches) return; try { var c = getComputedStyle(fr.contentDocument.documentElement).getPropertyValue('--arg-ui-background-surface').trim(); if (c) { document.getElementById('tc').setAttribute('content', c); document.body.style.background = c; } } catch (e) {} }
  fr.addEventListener('load', function () { theme(); safe(BARE.matches ? 'full' : cur); tint(); });
  var INFO = {"home": {"name": "Trang chủ", "desc": "Tổng quan trong một màn hình: thị trường, tài khoản của bạn và các dịch vụ hay dùng.", "feat": ["Theo dõi nhanh các chỉ số VN30, HNX30, HNX, UPCoM cùng xu hướng trong ngày.", "Xem tổng tài sản, lãi lỗ trong ngày, tỷ lệ ký quỹ, nạp tiền nhanh; chuyển giữa các tiểu khoản X1, M1, D1, Ảo.", "Truy cập nhanh dịch vụ yêu thích: sổ lệnh, nộp tiền, chuyển khoản, sao kê, lưu ký, rút lưu ký.", "Khuyến nghị của chuyên viên phân tích: nên mua, giữ, bán kèm lãi/lỗ và giá mục tiêu.", "Danh mục theo dõi theo nhóm và tin tức mới nhất."], "try": ["Bấm vào một chỉ số để xem chi tiết; bấm một mã cổ phiếu để xem thông tin mã.", "Bấm Thị trường ở thanh dưới để xem toàn cảnh thị trường.", "Bấm Giao dịch ở thanh dưới để đặt lệnh.", "Bấm X để tắt thông báo quảng bá.", "Vuốt ngang để xem thêm chỉ số và khuyến nghị.", "Bấm Lãi/lỗ trên thẻ khuyến nghị để sắp xếp."]}, "detail": {"name": "Chi tiết chỉ số", "desc": "Xem toàn cảnh một chỉ số: giá, biểu đồ, sức mạnh thị trường và dòng tiền.", "feat": ["Giá hiện tại, mức tăng giảm, khối lượng và giá trị giao dịch theo phiên.", "Biểu đồ nến hoặc biểu đồ đường kèm khối lượng, chọn khoảng thời gian từ 1 ngày đến 5 năm.", "Hiệu suất theo kỳ: 7 ngày, 1 tháng, 1 năm, 5 năm.", "Số mã tăng, đứng, giảm trong chỉ số.", "Giá trị mua ròng 5 phiên của khối ngoại và toàn thị trường.", "Bản đồ nhiệt các mã vốn hoá lớn và top cổ phiếu theo giá trị, khối lượng, khối ngoại mua ròng."], "try": ["Rê chuột lên biểu đồ (hoặc chạm giữ rồi kéo trên điện thoại) để xem giá từng thời điểm.", "Bấm nút sóng hoặc nến cạnh biểu đồ để đổi kiểu biểu đồ.", "Cuộn xuống: giá hiện ngay trên thanh tiêu đề.", "Bấm mũi tên trái để quay về."]}, "trade": {"name": "Giao dịch", "desc": "Đặt lệnh mua bán cổ phiếu ngay trên một màn hình, không cần cuộn.", "feat": ["Xem giá khớp, giá trần, sàn, tham chiếu và khối lượng giao dịch của mã.", "Sổ lệnh có hai kiểu xem: độ sâu 3 mức giá tốt nhất kèm khối lượng, hoặc danh sách 4 mức mua và 4 mức bán kèm tổng khối lượng và tỷ lệ mua bán.", "Bấm \"Xem đầy đủ\" dưới sổ lệnh để mở bảng bước giá 10 mức mua và bán, kèm giá sàn và giá trần.", "Chọn loại lệnh (LO, MP, ATO, ATC) trong bảng trượt từ dưới lên, mỗi loại có mô tả ngắn; nhập giá và khối lượng bằng nút trừ, cộng theo đúng bước giá và bước khối lượng.", "Xem sức mua, tỷ lệ ký quỹ, khối lượng mua tối đa và giá trị ước tính của lệnh.", "Đổi tiểu khoản giao dịch ngay đầu màn hình.", "Chế độ Lite đặt lệnh nhanh, không cần xem sổ lệnh: chọn nhanh giá Sàn, Tham chiếu, Trần và khối lượng theo 25%, 50%, 75%, tối đa sức mua.", "Bấm Mua hoặc Bán sẽ hiện hộp xác nhận lệnh (mã, loại lệnh, giá, khối lượng, giá trị ước tính); xác nhận xong có thông báo đặt lệnh thành công."], "try": ["Ở góc trên cột trái, bấm biểu tượng danh sách để xem sổ lệnh dạng danh sách.", "Bấm Mua hoặc Bán: nút đặt lệnh đổi màu theo chiều lệnh.", "Bấm Lite ở góc trên phải để đặt lệnh nhanh, bấm Pro để quay lại sổ lệnh.", "Ở Lite: bấm Sàn, TC, Trần để đặt giá; bấm 25%, 50%, 75%, Tối đa để đặt khối lượng.", "Bấm trừ hoặc cộng để đổi giá, khối lượng; giá trị ước tính cập nhật theo.", "Bấm Trang chủ ở thanh dưới để quay lại.", "Bấm Thông tin CP để xem trang thông tin của mã.", "Bấm ô Giá (phím số có dấu phẩy) hoặc ô Khối lượng (phím số) để bàn phím trượt lên; bấm Xong để hạ xuống.", "Bấm nút Mua hoặc Bán ở cuối màn hình, kiểm tra thông tin rồi bấm xác nhận.", "Bấm biểu tượng lịch ở góc trên bên phải để mở Sổ lệnh.", "Bấm \"Xem đầy đủ\" dưới sổ lệnh để xem đủ 10 mức giá mua bán.", "Bấm ô Loại lệnh để mở bảng chọn, chọn ATO hay ATC rồi xem loại lệnh hiện trong hộp xác nhận."]}, "stock": {"name": "Thông tin cổ phiếu", "desc": "Toàn cảnh một mã cổ phiếu trên một trang: giá, cổ phiếu bạn đang nắm giữ, biểu đồ, bước giá, giao dịch khối ngoại và khớp lệnh.", "feat": ["Giá khớp, mức tăng giảm và trạng thái phiên.", "Số cổ phiếu đang sở hữu, giá vốn và lãi/lỗ tạm tính.", "Giá trần, tham chiếu, sàn, cao, thấp, trung bình; thêm khối lượng, giá trị, giá mở cửa, cao thấp 52 tuần và vốn hoá.", "Biểu đồ nến hoặc đường kèm khối lượng, chọn khoảng thời gian.", "Bước giá: 3 mức mua bán tốt nhất, tổng dư mua, dư bán và tỷ lệ.", "Khối lượng, giá trị mua bán của khối ngoại hôm nay; mua ròng theo giờ và 10 phiên gần nhất.", "Danh sách khớp lệnh gần nhất: mua chủ động (M) hoặc bán chủ động (B).", "Tin tức mới, tin đọc nhiều nhất và tin xu hướng của mã.", "Lịch sự kiện: cổ tức, công bố kết quả kinh doanh, đại hội cổ đông; lọc theo khoảng ngày.", "Tài chính theo quý hoặc năm: ROE, ROA, EPS, lợi nhuận, doanh thu, cân đối kế toán, lưu chuyển tiền tệ; các chỉ số định giá, sinh lời, sức mạnh tài chính.", "Doanh nghiệp: giới thiệu, cơ cấu sở hữu, cổ đông lớn, giao dịch nội bộ, thông tin niêm yết.", "Tín hiệu kỹ thuật tổng hợp từ các chỉ báo dao động và đường trung bình động.", "Nút Mua, Bán luôn ở đáy màn."], "try": ["Mở trang: bấm một mã trong Danh mục theo dõi hoặc Khuyến nghị ở Trang chủ, hoặc bấm Thông tin CP ở màn Giao dịch.", "Bấm mũi tên dưới lưới giá để thu gọn hoặc mở thêm chỉ số.", "Bấm Tin tức để xem tin của mã, bấm Thông tin giao dịch để quay lại.", "Rê chuột lên biểu đồ (hoặc chạm giữ rồi kéo) để xem giá từng thời điểm.", "Bấm Hôm nay hoặc 10 phiên ở mục Mua ròng của khối ngoại.", "Bấm Mua hoặc Bán: mở màn đặt lệnh của đúng mã đó, chiều lệnh chọn sẵn.", "Cuộn xuống: giá hiện ngay trên thanh tiêu đề.", "Bấm mũi tên trái để quay về.", "Vuốt dải tab dưới giá để chuyển Tin tức, Sự kiện, Tài chính, Doanh nghiệp, Kỹ thuật.", "Tin tức: bấm Xem thêm để mở thêm tin; bấm mũi tên ở tiêu đề mục để thu gọn.", "Sự kiện: đổi Từ ngày, Đến ngày để lọc; bấm từng sự kiện để xem chi tiết.", "Tài chính: bấm Quý hoặc Năm; bấm ROE, ROA, EPS và các nhóm chỉ tiêu để đổi biểu đồ.", "Doanh nghiệp: bấm Xem thêm để đọc hết phần giới thiệu.", "Kỹ thuật: bấm Tổng hợp, Dao động, Đường MA để xem tín hiệu từng nhóm."]}, "market": {"name": "Thị trường", "desc": "Toàn cảnh thị trường trong phiên: độ rộng, dòng tiền, tác động tới chỉ số, giao dịch khối ngoại, tự doanh và thanh khoản theo từng sàn.", "feat": ["Tổng quan theo 4 góc nhìn: Biến động, Khối ngoại, Tự doanh, Thanh khoản; chọn sàn HOSE, HNX, UPCoM.", "Số mã tăng, giảm, đứng và giá trị khớp theo từng nhóm.", "Các mã kéo chỉ số lên, xuống nhiều nhất và tổng điểm đóng góp.", "Dòng tiền chủ động trong phiên hôm nay và 5 phiên trước.", "Phân bố số mã theo khoảng thay đổi giá.", "Top cổ phiếu theo khối lượng, tăng giá, giảm giá, khối ngoại mua bán ròng.", "Bảng giá theo sàn có biểu đồ nhỏ và đủ 5 trạng thái giá (tăng, giảm, đứng, trần, sàn); sắp xếp theo mã, % thay đổi, giá, khối lượng.", "Danh mục theo dõi nhiều nhóm: bỏ mã bằng nút tim, thêm mã bằng ô tìm kiếm, gợi ý cổ phiếu blue-chip khi danh mục còn trống.", "Danh mục đang nắm giữ, chủ đề ngành và các chỉ số."], "try": ["Vuốt dải tab trên cùng: Tổng quan, Bảng giá, Danh mục, Theo dõi, Top cổ phiếu, Chủ đề, Chỉ số.", "Bấm Biến động, Khối ngoại, Tự doanh, Thanh khoản để đổi góc nhìn; sàn đã chọn được giữ nguyên.", "Ở Tổng quan, bấm HOSE, HNX, UPCoM để đổi sàn; ở Bảng giá, chọn sàn trong ô chọn.", "Ở Dòng tiền chủ động, bấm T, T-1 đến T-5 để xem từng phiên.", "Bấm mã có liên kết (VCB, HPG, CTG...) để mở trang thông tin mã.", "Bấm tên chỉ số ở tab Chỉ số để xem chi tiết chỉ số.", "Bảng giá: bấm nút sắp xếp ở góc phải để xếp lại; bấm nút tròn góc phải dưới để xem khối lượng thay cho biểu đồ.", "Theo dõi: đổi danh mục trong ô chọn; bấm tim để bỏ mã; bấm dấu cộng để tìm và thêm mã; bấm nút ba chấm để thêm mã hoặc xoá hết mã.", "Theo dõi: chọn Danh mục mới để thấy gợi ý, tích chọn các mã rồi bấm Thêm vào danh mục.", "Ở bảng Thêm mã, bấm ô tìm kiếm để hiện bàn phím chữ (phím 123 đổi sang số và ký hiệu)."]}, "theme": {"name": "Chủ đề", "desc": "Xem một nhóm ngành: biến động trung bình, các chỉ số chính và danh sách cổ phiếu trong nhóm.", "feat": ["Ảnh minh hoạ và biến động trung bình của chủ đề trong phiên.", "Bốn chỉ số chính: vốn hoá, khối lượng khớp, P/E và P/B trung bình.", "Danh sách cổ phiếu trong chủ đề với giá, phần trăm thay đổi và khối lượng; bấm ngôi sao để thêm hoặc bỏ khỏi danh mục theo dõi.", "Cơ cấu sở hữu theo nước ngoài, tổ chức, cá nhân và các tin mới nhất của nhóm."], "try": ["Bấm ngôi sao ở một mã để đổi trạng thái yêu thích (sao vàng là đã theo dõi).", "Bấm một mã có sẵn thông tin để mở trang cổ phiếu.", "Bấm mũi tên quay lại để về danh sách chủ đề."]}, "search": {"name": "Tìm kiếm", "desc": "Tìm nhanh một mã chứng khoán theo mã hoặc tên công ty, rồi theo dõi hoặc mở thông tin mã.", "feat": ["Chưa gõ gì thì hiện các mã bạn tìm gần đây; xoá từng mã hoặc xoá cả danh sách.", "Gõ mã hoặc tên công ty, kết quả lọc ngay khi gõ, mã khớp đầu tiên nằm trên cùng.", "Bấm ngôi sao để thêm hoặc bỏ mã khỏi danh mục theo dõi (sao vàng là đang theo dõi).", "Bấm một mã để mở trang thông tin mã."], "try": ["Bấm một mã trong tìm gần đây để điền vào ô tìm.", "Gõ VC hoặc Hòa Phát vào ô tìm.", "Bấm ngôi sao ở một kết quả.", "Bấm mã VCB hoặc HPG để mở thông tin mã."]}, "asset": {"name": "Tài sản", "desc": "Toàn bộ tài sản của một tiểu khoản: tổng tài sản, tiền, cổ phiếu, dư nợ, danh mục đang nắm giữ và các sao kê.", "feat": ["Tab Tài sản: tổng tài sản kèm lãi lỗ hôm nay (bấm con mắt để ẩn số), lãi đã thực hiện, tài sản ròng, tiền có thể rút và cảnh báo dư nợ margin.", "Cơ cấu tài sản giữa cổ phiếu và tiền; chi tiết từng khoản tiền, giá trị cổ phiếu, dư nợ, phí và thuế.", "Tab Danh mục: phân bổ theo mã, lãi lỗ từng mã và danh sách cổ phiếu đang nắm giữ.", "Tab Lãi lỗ: đường lãi lỗ luỹ kế theo ngày trong kỳ chọn, tổng lãi, lỗ, phí thuế và các lệnh đã bán.", "Tab Sao kê tiền: số dư đầu kỳ, cuối kỳ và từng giao dịch tiền tại công ty hoặc tại VSD."], "try": ["Bấm con mắt cạnh Tổng tài sản để ẩn hoặc hiện số.", "Bấm mũi tên ở dòng Tiền ứng trước khả dụng để xem T1, T2, T3.", "Bấm Danh mục, Lãi lỗ, Sao kê tiền ở dải tab đầu trang.", "Rê chuột lên đường lãi lỗ để xem từng ngày.", "Bấm ô ngày để đổi kỳ sao kê; bấm mũi tên ở một dòng sao kê để xem phí, thuế."]}, "orderbook": {"name": "Sổ lệnh", "desc": "Theo dõi các lệnh đã đặt trong ngày và huỷ lệnh còn hiệu lực, một hoặc nhiều lệnh cùng lúc.", "feat": ["Mỗi lệnh hiện gọn: chiều lệnh Mua hoặc Bán, mã, giờ, giá và khối lượng đặt, trạng thái và tiến độ khớp.", "Lọc nhanh theo trạng thái (Chờ khớp, Khớp một phần, Đã khớp, Đã huỷ, kèm số lệnh), theo Mua hoặc Bán và theo mã.", "Bấm vào một lệnh (nút mũi tên bên phải) để mở màn chi tiết lệnh.", "Bấm Chọn để chọn nhiều lệnh còn hiệu lực, rồi huỷ cùng lúc có hộp xác nhận."], "try": ["Bấm các nhãn trạng thái ở đầu danh sách để lọc.", "Gõ một mã (ví dụ VCB) vào ô tìm.", "Bấm một lệnh để mở màn chi tiết lệnh.", "Bấm Chọn (hoặc nhấn giữ một lệnh còn hiệu lực), tích vài lệnh hoặc Tất cả, rồi bấm Huỷ lệnh."]}, "orderdetail": {"name": "Chi tiết lệnh", "desc": "Xem đầy đủ thông tin một lệnh và huỷ lệnh nếu còn hiệu lực.", "feat": ["Chiều lệnh Mua hoặc Bán, trạng thái và mã chứng khoán nổi bật ở đầu màn.", "Các thông tin của lệnh: số hiệu, thời gian, loại lệnh, giá đặt, giá khớp trung bình, khối lượng đặt và khớp, giá trị ước tính, phí giao dịch ước tính.", "Huỷ lệnh có hộp xác nhận (chỉ với lệnh chờ khớp hoặc khớp một phần); Sửa lệnh mở màn Giao dịch của mã, chọn sẵn chiều lệnh."], "try": ["Bấm Huỷ lệnh rồi xác nhận, trạng thái chuyển thành Đã huỷ.", "Bấm Sửa lệnh để sang màn Giao dịch của mã.", "Bấm mũi tên quay lại để về Sổ lệnh."]}};
  var esc = function (t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
  function show(id) {
    var k = id === 'home' ? 'home' : id.indexOf('trade') === 0 ? 'trade' : id.indexOf('stock-') === 0 ? 'stock' : id === 'market' ? 'market' : id === 'orderbook' ? 'orderbook' : id === 'search' ? 'search' : id === 'asset' ? 'asset' : id.indexOf('order-') === 0 ? 'orderdetail' : id.indexOf('theme-') === 0 ? 'theme' : 'detail', d = INFO[k], name = d.name;
    if (k === 'detail' || k === 'stock' || k === 'theme' || k === 'orderdetail') name += ' ' + (fr.contentDocument.querySelector('[data-arg-screen="' + id + '"] .arg-appbar__title, [data-arg-screen="' + id + '"] .arg-theme-head .arg-title__text') || { textContent: '' }).textContent;
    var li = function (arr, max) { return '<ul>' + arr.map(function (x, i) { return '<li' + (max && i >= max ? ' hidden data-more' : '') + '>' + esc(x) + '</li>'; }).join('') + '</ul>' + (max && arr.length > max ? '<button class="more" type="button" data-n="' + (arr.length - max) + '">Xem thêm ' + (arr.length - max) + ' mục</button>' : ''); };
    info.innerHTML = '<span class="tag">Đang xem</span><h2>' + esc(name) + '</h2><p>' + esc(d.desc) + '</p><h3>Tính năng</h3>' + li(d.feat, 4) + '<h3>Thử ngay</h3>' + li(d.try, 3);
  }
  info.addEventListener('click', function (e) { var b = e.target.closest('.more'); if (!b) return; var open = b.dataset.open !== '1'; b.dataset.open = open ? '1' : '0'; b.previousElementSibling.querySelectorAll('[data-more]').forEach(function (x) { x.hidden = !open; }); b.textContent = open ? 'Thu gọn' : 'Xem thêm ' + b.dataset.n + ' mục'; });
  function bind() { try { fr.contentDocument.addEventListener('arg:screen', function (e) { show(e.detail.id); }); show(START); } catch (e) {} }
  fr.addEventListener('load', bind); if (fr.contentDocument && fr.contentDocument.readyState === 'complete') bind();
  function fit() {
    var bare = BARE.matches, d = bare ? 'full' : cur, b = document.body; b.dataset.d = d; if (bare) b.dataset.bare = '1'; else { delete b.dataset.bare; b.style.background = ''; } safe(d); tint();
    document.querySelectorAll('.bar button').forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.d === d)); });
    if (!bare) try { history.replaceState(null, '', '#d=' + d); } catch (e) {}
    if (d === 'full') { wrap.style.cssText = 'width:100%;height:' + st.clientHeight + 'px'; dev.style.cssText = 'width:100%;height:100%'; document.getElementById('lbl').textContent = ''; return; }
    var w = S[d][0], h = S[d][1], side = window.innerWidth > 1000 ? 2 * Math.max(nav.offsetWidth, info.offsetWidth) + 48 : 0, k = Math.min(1, (st.clientWidth - 32 - side) / w, (st.clientHeight - 48) / h);
    wrap.style.cssText = 'width:' + w * k + 'px;height:' + h * k + 'px';
    dev.style.cssText = 'width:' + w + 'px;height:' + h + 'px;transform:scale(' + k + ')';
    document.getElementById('lbl').textContent = k < 1 ? 'Đang xem ' + Math.round(k * 100) + '%' : '';
  }
  document.querySelectorAll('.bar button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      cur = btn.dataset.d; document.querySelectorAll('.bar button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === btn)); }); fit();
    });
  });
  var q = nav.querySelector('.search'), fold = function (t) { return t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').toLowerCase(); };
  q.addEventListener('input', function () {
    var k = fold(q.value.trim());
    nav.querySelectorAll('details').forEach(function (g) {
      var any = false;
      g.querySelectorAll('li').forEach(function (li) { var on = !k || fold(li.textContent).indexOf(k) >= 0; li.hidden = !on; if (on) any = true; });
      g.hidden = !any; if (k && any) g.open = true;
    });
  });
  nav.querySelector('h2').addEventListener('click', function () { nav.toggleAttribute('data-closed'); nav.querySelector('.tree').hidden = nav.hasAttribute('data-closed'); });
  nav.addEventListener('click', function (e) { var a = e.target.closest('a'); if (!a) return; e.preventDefault(); location.href = a.getAttribute('href') + '#d=' + cur; });
  document.getElementById('all').addEventListener('click', function (e) { e.preventDefault(); location.href = 'index.html#d=' + cur; });
  /* Đặc tả: bật bằng công tắc trên thanh đầu (nhớ trạng thái trong phiên). Chấm đánh số nằm trên thành phần trong màn hình, bong bóng nằm ở hai bên khung thiết bị, nối bằng đường nét đứt. */
  var SPECS = __SPECS__, layer = document.getElementById('spec'), tg = document.getElementById('spec-toggle'), SIDEKEY = 'arg-spec';
  try { tg.checked = sessionStorage.getItem(SIDEKEY) === '1'; } catch (e) {}
  function renderSpec() {
    layer.innerHTML = '';
    var doc = null; try { doc = fr.contentDocument; } catch (e) {}
    if (!tg.checked || !doc || cur === 'full' || window.innerWidth < 1000 || !SPECS.length) return;
    var scr = doc.querySelector('[data-arg-screen]:not([hidden])') || doc, dr = dev.getBoundingClientRect(), sr = st.getBoundingClientRect(), nr = nav.getBoundingClientRect(), ir = info.getBoundingClientRect();
    var k = dr.width / fr.clientWidth, vh = doc.documentElement.clientHeight, vw = fr.clientWidth, X = dr.left - sr.left, XR = dr.right - sr.left;
    var room = { l: X - (nr.right - sr.left) - 36, r: (ir.left - sr.left) - XR - 36 }, items = [];
    SPECS.forEach(function (sp, n) {
      var el = null; try { el = scr.querySelector(sp.s); } catch (e) {}
      if (!el) return;
      var r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2 || r.bottom < 8 || r.top > vh - 8) return;
      var top = Math.max(r.top, 0), bot = Math.min(r.bottom, vh), side = sp.side;
      if (room.l < 150 || room.r < 150) return;   /* hai bên đủ chỗ thì mới hiện, tránh bong bóng dồn một phía */
      items.push({ sp: sp, n: n + 1, side: side, ex: side === 'l' ? X + Math.max(r.left, 0) * k : X + Math.min(r.right, vw) * k, ax: side === 'l' ? X : XR, ay: dr.top - sr.top + ((top + bot) / 2) * k, box: [X + r.left * k, dr.top - sr.top + r.top * k, r.width * k, r.height * k] });
    });
    items.forEach(function (it, i) { it.n = i + 1; });   /* đánh số liền theo các mục đang hiện */
    if (!items.length) { var tip = document.createElement('div'); tip.className = 'spec-note'; tip.style.cssText = 'left:50%;bottom:16px;transform:translateX(-50%);width:auto;max-width:420px'; tip.textContent = 'Chưa đủ chỗ hiện đặc tả ở khung này: chọn Mobile hoặc mở rộng cửa sổ trình duyệt.'; layer.appendChild(tip); return; }
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); layer.appendChild(svg);
    ['l', 'r'].forEach(function (sd) {
      var list = items.filter(function (it) { return it.side === sd; }).sort(function (a, b) { return a.ay - b.ay; }), w = Math.min(250, room[sd]), prev = 0;
      var made = list.map(function (it) {
        var note = document.createElement('div'); note.className = 'spec-note'; note.style.width = w + 'px';
        note.innerHTML = '<i>' + it.n + '</i><span></span>'; note.lastChild.textContent = it.sp.t;
        note.style.left = (sd === 'l' ? X - 24 - w : XR + 24) + 'px'; note.style.top = '0px'; layer.appendChild(note);
        return { it: it, note: note, h: note.offsetHeight, y: 0 };
      });
      made.forEach(function (m) { m.y = Math.max(m.it.ay - m.h / 2, prev + 8, 8); prev = m.y + m.h; });
      var H = st.clientHeight, next = H - 8;                     /* kéo ngược lên nếu tràn đáy khung */
      for (var q = made.length - 1; q >= 0; q--) { made[q].y = Math.min(made[q].y, next - made[q].h); next = made[q].y - 8; }
      made.forEach(function (m) {
        var it = m.it, y = Math.max(m.y, 8), bx = sd === 'l' ? X - 24 : XR + 24, by = y + m.h / 2;
        m.note.style.top = y + 'px';
        if (Math.abs(it.ex - it.ax) > 6) {
          var pi = document.createElementNS('http://www.w3.org/2000/svg', 'path'); pi.setAttribute('class', 'in'); pi.setAttribute('d', 'M' + it.ex + ' ' + it.ay + ' L' + it.ax + ' ' + it.ay); svg.appendChild(pi);
          var dot = document.createElement('div'); dot.className = 'spec-dot'; dot.style.left = it.ex + 'px'; dot.style.top = it.ay + 'px'; layer.appendChild(dot);
        }
        var p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', 'M' + it.ax + ' ' + it.ay + ' L' + bx + ' ' + by); svg.appendChild(p);
        var pin = document.createElement('div'); pin.className = 'spec-pin'; pin.textContent = it.n; pin.style.left = it.ax + 'px'; pin.style.top = it.ay + 'px'; layer.appendChild(pin);
        var box = document.createElement('div'); box.className = 'spec-box'; box.style.cssText = 'left:' + it.box[0] + 'px;top:' + it.box[1] + 'px;width:' + it.box[2] + 'px;height:' + it.box[3] + 'px'; layer.appendChild(box);
        m.note.addEventListener('mouseenter', function () { box.classList.add('on'); }); m.note.addEventListener('mouseleave', function () { box.classList.remove('on'); });
      });
    });
  }
  tg.addEventListener('change', function () { try { sessionStorage.setItem(SIDEKEY, tg.checked ? '1' : '0'); } catch (e) {} renderSpec(); });
  var fit0 = fit; fit = function () { fit0(); renderSpec(); };
  fr.addEventListener('load', function () { try { fr.contentWindow.addEventListener('scroll', renderSpec); fr.contentDocument.addEventListener('click', function () { setTimeout(renderSpec, 350); }); } catch (e) {} setTimeout(renderSpec, 300); });
  window.addEventListener('resize', fit); fit();
})();
</script></body></html>'''

# ---- Xuất: mỗi màn hình một file trong dist/screens/, dùng chung dist/screens/assets/ ----
S = D / 'screens'
A = S / 'assets'
A.mkdir(parents=True, exist_ok=True)
tokens = (D / 'arg-tokens.css').read_text(); css = no_hover((D / 'arg-ui.css').read_text()); js = (D / 'arg-ui.js').read_text()
(A / 'PretendardVariable.woff2').write_bytes((UI / 'viewer/fonts/PretendardVariable.woff2').read_bytes())
(A / 'arg.css').write_text(f'''@font-face {{ font-family: "Pretendard"; font-weight: 45 920; font-display: swap; src: url(PretendardVariable.woff2) format("woff2"); }}
body {{ margin: 0; }}
html {{ scrollbar-width: none; background: var(--arg-ui-background-surface); }} html[data-theme="dark"] {{ color-scheme: dark; }}
html {{ scrollbar-width: none; }} ::-webkit-scrollbar {{ display: none; }}
{tokens}
{css}''')
(A / 'arg.js').write_text(js)
(A / 'themes').mkdir(exist_ok=True)
for t in TM.THEME_DATA:
    (A / 'themes' / f"{t['slug']}.jpg").write_bytes((UI.parent.parent / 'images/themes' / f"Property 1={t['img']}.jpg").read_bytes())

IDS = [x[0] for x in SCREENS]
SHIM = r"""/* Mỗi màn một file: [data-arg-go] sang màn khác thì mở file của màn đó (trong khung xem), [data-arg-back] quay lại trang trước; link giữ chỗ href="#" không điều hướng */
(function () {
  var IDS = __IDS__, cur = document.querySelector('[data-arg-screen]').getAttribute('data-arg-screen');
  function open(id) { var d = (parent.location.hash.match(/d=\w+/) || [''])[0]; parent.location.href = id + '.html' + (d ? '#' + d : ''); }
  document.addEventListener('click', function (e) {
    var g = e.target.closest('[data-arg-go]');
    if (g) { e.preventDefault(); e.stopPropagation(); var id = g.getAttribute('data-arg-go'); if (id !== cur && IDS.indexOf(id) >= 0) open(id); return; }
    if (e.target.closest('[data-arg-back]')) { e.preventDefault(); e.stopPropagation(); if (parent.history.length > 1) parent.history.back(); else open('home'); return; }
    var a = e.target.closest('a[href="#"]'); if (a) e.preventDefault();
  }, true);
})();""".replace('__IDS__', json.dumps(IDS))

sb = (UI / 'pages/statusbar-ios.svg').read_text()
sb_inner = re.search(r'<svg[^>]*>(.*)</svg>', sb, re.S).group(1)
sb_inner = re.sub(r'<path d="M45\.4603[^>]*/>', '', sb_inner).replace('#111111', 'currentColor')   # bỏ giờ vẽ sẵn (giờ thật vẽ bằng chữ), màu theo chữ của hệ thống để đổi theo chế độ sáng, tối
statusbar = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="sb">' + sb_inner + '</g></defs></svg>'
             '<div class="sbar" id="sbar" aria-hidden="true"><svg viewBox="0 0 187.5 44" width="187.5" height="44"><use href="#sb"/></svg>'
             '<svg viewBox="187.5 0 187.5 44" width="187.5" height="44"><use href="#sb"/></svg><span class="sb-time" id="sbtime"></span></div>')
BRAND = [re.search(r'--arg-p-brand-header-' + n + r':\s*(#[0-9a-fA-F]{6})', (D / 'arg-tokens.css').read_text()).group(1) for n in ('start', 'end')]  # màu nhận diện Agriseco (gradient header web)
names = {sid: n for sid, _, n in SCREENS}
groups = [('Màn chính', ['home', 'market', 'trade', 'orderbook', 'asset', 'search']), ('Thông tin mã', [x for x in IDS if x.startswith('stock-')]),
          ('Đặt lệnh theo mã', [x for x in IDS if x.startswith('trade-')]), ('Chi tiết chỉ số', [x for x in IDS if x.startswith('idx-')]), ('Chi tiết chủ đề', [x for x in IDS if x.startswith('theme-')]), ('Chi tiết lệnh', [x for x in IDS if x.startswith('order-')])]


ico = lambda n, cls='': re.sub(r'<metadata>.*?</metadata>', '', re.sub(r'<svg[^>]*>', lambda m: '<svg class="ic ' + cls + '" viewBox="' + re.search(r'viewBox="([^"]+)"', m.group(0)).group(1) + '" aria-hidden="true">', (UI / f'pages/nav-icons/{n}.svg').read_text(), count=1), flags=re.S)


def nav_html(cur):
    """Cột danh sách màn hình sát mép trái: ô tìm, mục lớn, mỗi nhóm là một thư mục gập được (nhóm chứa màn đang xem mở sẵn), màn đang xem đánh dấu aria-current."""
    chev, shut, opn, mark, bend = ico('caret-down', 'chev'), ico('folder', 'shut'), ico('folder-open', 'open'), ico('file-text'), ico('arrow-bend-down-right', 'bend')
    out = ''
    for g, ids in groups:
        links = ''.join(f'<li><a href="{i}.html"{" aria-current=\"page\"" if i == cur else ""}>{bend}{mark}<span>{re.sub(r"^(Chủ đề|Chỉ số|Thông tin|Giao dịch|Lệnh) ", "", names[i]) if g != "Màn chính" else names[i]}</span></a></li>' for i in ids)
        out += f'<details{" open" if cur in ids else ""}><summary>{shut}{opn}<span>{g}</span>{chev}</summary><ul>{links}</ul></details>'
    return (f'<nav class="nav arg-ui" aria-label="Danh sách màn hình"><div class="arg-control"><input class="arg-input search" type="search" placeholder="Tìm màn hình..." aria-label="Tìm màn hình"></div>'
            f'<h2><span>Màn hình demo</span>{chev}</h2><div class="tree">{out}</div></nav>')


SHELL_TPL = SHELL.replace('__IC_MOBILE__', ico('device-mobile')).replace('__IC_TABLET__', ico('device-tablet')).replace('__IC_FULL__', ico('arrows-out-simple')).replace('__SB__', statusbar).replace('__BRAND__', BRAND[0]).replace('__BRAND2__', BRAND[1])
for sid, html, name in SCREENS:
    html = re.sub(r'(data-arg-screen="' + re.escape(sid) + r'"[^>]*?)\s+hidden', r'\1', html, count=1)
    doc = f'''<!doctype html>
<html lang="vi" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agriseco · {name}</title><link rel="stylesheet" href="assets/arg.css"></head><body class="arg-ui">
<div class="arg-page" data-arg-today="2026-10-29">{html}</div>
<script src="assets/arg.js"></script>
<script>{SHIM}</script></body></html>'''
    esc = doc.replace('&', '&amp;').replace('"', '&quot;')
    (S / f'{sid}.html').write_text(SHELL_TPL.replace('__NAV__', nav_html(sid)).replace('__SPECS__', json.dumps([{'s': s, 'side': d, 't': t} for s, d, t in specs_for(sid)], ensure_ascii=False)).replace('__PAGE__', esc).replace('__TITLE__', f'Agriseco · {name}').replace('__ID__', sid))

lis = ''.join(f'<h2>{g}</h2><ul>' + ''.join(f'<li><a href="{i}.html">{names[i]}</a></li>' for i in ids) + '</ul>' for g, ids in groups)
(S / 'index.html').write_text(f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Agriseco · Các màn hình demo</title>
<style>body{{margin:0;padding:32px 20px;font:15px/1.5 system-ui,sans-serif;background:color-mix(in srgb,{BRAND[0]} 3%,#fff);color:#1f2328}}main{{max-width:560px;margin:0 auto}}h1{{font-size:24px}}h2{{margin:28px 0 8px;font-size:13px;text-transform:uppercase;letter-spacing:.04em;opacity:.6}}ul{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}a{{display:block;padding:12px 16px;border-radius:12px;background:#fff;color:inherit;text-decoration:none;box-shadow:0 1px 2px rgba(0,0,0,.06)}}a:hover{{background:color-mix(in srgb,{BRAND[0]} 12%,#fff)}}</style></head>
<body><main><h1>Các màn hình demo</h1><p>Mỗi màn hình là một file riêng, mở bằng trình duyệt.</p>{lis}</main>
<script>var h=location.hash.match(/d=\\w+/);if(h)document.querySelectorAll('a').forEach(function(a){{a.href+='#'+h[0]}})</script></body></html>''')
print(len(SCREENS), 'màn hình ->', S)
