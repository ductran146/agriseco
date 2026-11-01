"""Markup cho tab Lịch sử lệnh trong màn Sổ lệnh (component orderhist; dùng lại orderrow, chip-tab, tabs, statrow, datepicker).
Dữ liệu mẫu: lệnh cổ phiếu cơ sở trên HOSE của tiểu khoản 039C101991 - 01 trong các phiên trước 29/10/2026 (không phải số thật).
Quy tắc: lô 100, bước giá 0,01 (dưới 10), 0,05 (10 đến dưới 50), 0,10 (từ 50); giá đặt nằm trong biên độ ±7%; lệnh bán chỉ với mã đang nắm giữ (VCB, HPG, AGR)."""
from datetime import date
from detail_parts import vn
from orderbook_parts import STATUS, order_id, num, I
from asset_parts import date_pair

TODAY = date(2026, 10, 29)
WD = ('Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ nhật')

# (mã lệnh, giờ, mã CK, chiều, loại, giá (None = không có giá: MP, ATO, ATC), khối lượng, đã khớp, giá khớp TB, trạng thái, ngày đặt, ghi chú)
HISTORY = [
    ('LD-281001', '14:20:31', 'VCB', 'buy', 'LO', 92.00, 500, 500, 91.95, 'matched', '2026-10-28', ''),
    ('LD-281002', '11:05:17', 'HPG', 'sell', 'LO', 26.80, 1000, 1000, 26.85, 'matched', '2026-10-28', ''),
    ('LD-281003', '09:15:00', 'CTG', 'buy', 'ATO', None, 1000, 1000, 35.25, 'matched', '2026-10-28', ''),
    ('LD-271001', '10:48:22', 'AGR', 'buy', 'LO', 19.60, 3000, 1800, 19.60, 'partial', '2026-10-27', 'Phần chưa khớp hết hiệu lực cuối phiên'),
    ('LD-271002', '09:35:41', 'MSN', 'buy', 'LO', 68.00, 300, 0, 0, 'cancelled', '2026-10-27', 'Bạn đã huỷ lệnh'),
    ('LD-261001', '14:45:00', 'BID', 'buy', 'ATC', None, 800, 800, 39.90, 'matched', '2026-10-26', ''),
    ('LD-261002', '11:02:17', 'VIC', 'buy', 'LO', 44.50, 1000, 0, 0, 'rejected', '2026-10-26', 'Giá đặt cao hơn giá trần 44,00'),
    ('LD-231001', '10:22:09', 'VCB', 'sell', 'LO', 93.00, 500, 500, 93.00, 'matched', '2026-10-23', ''),
    ('LD-221001', '14:05:33', 'NVL', 'buy', 'LO', 14.80, 5000, 5000, 14.80, 'matched', '2026-10-22', ''),
    ('LD-201001', '13:30:12', 'HPG', 'buy', 'LO', 25.40, 2000, 2000, 25.40, 'matched', '2026-10-20', ''),
    ('LD-161001', '09:50:44', 'AGR', 'buy', 'LO', 18.20, 5000, 5000, 18.20, 'matched', '2026-10-16', ''),
    ('LD-121001', '10:12:30', 'VCB', 'buy', 'LO', 88.50, 1000, 1000, 88.50, 'matched', '2026-10-12', ''),
    ('LD-250901', '09:30:08', 'VCB', 'buy', 'LO', 87.00, 500, 500, 87.00, 'matched', '2026-09-25', ''),
]
CHIPS = [('all', 'Tất cả'), ('matched', 'Đã khớp'), ('partial', 'Khớp một phần'), ('cancelled', 'Đã huỷ'), ('rejected', 'Từ chối')]
PERIODS = [('7', '7 ngày'), ('30', '30 ngày'), ('90', '3 tháng'), ('custom', 'Tuỳ chọn')]
DEFAULT = '30'


def d_of(o): return date.fromisoformat(o[10])
def dmy(d): return f'{d.day:02d}/{d.month:02d}/{d.year}'
def day_title(d): return f'{WD[d.weekday()]}, {dmy(d)}'
def value(o): return round(o[7] * o[8] * 1000)
def px_text(typ, px): return vn(px) if px else ('Thị trường' if typ == 'MP' else typ)


def row(o):
    oid, time, code, side, typ, px, qty, matched, avg, status, day, note = o
    label, badge = STATUS[status]
    sd = 'mua' if side == 'buy' else 'bán'
    fill = ('Vượt giá trần' if 'trần' in note else 'Bị từ chối') if status == 'rejected' else f'Khớp <b>{num(matched)}</b>/{num(qty)}'
    return (f'<li class="arg-orderrow" data-side="{side}" data-status="{status}" data-code="{code}" data-date="{day}" data-matched="{matched}" data-value="{value(o)}">'
            f'<a class="arg-orderrow__main" href="#" data-arg-go="{order_id(o)}" aria-label="Xem chi tiết lệnh {sd} {code} ngày {dmy(d_of(o))}"><span class="arg-orderrow__side">{"M" if side == "buy" else "B"}</span>'
            f'<span class="arg-orderrow__id"><b>{code}</b><span>{time[:5]} · {typ}</span></span><span class="arg-badge{" arg-badge--" + badge if badge else ""}">{label}</span>'
            f'<span class="arg-orderrow__px">{px_text(typ, px)}<span> × {num(qty)}</span></span><span class="arg-orderrow__fill">{fill}</span><span class="arg-orderrow__go">{I("caret-right")}</span></a></li>')


def days():
    out = []
    for o in HISTORY:
        d = d_of(o)
        if not out or out[-1][0] != d: out.append((d, []))
        out[-1][1].append(o)
    return out


def pane():
    """Nội dung tab Lịch sử lệnh: một hàng công cụ (khoảng thời gian, Bộ lọc), thẻ tổng kết hai chỉ số, danh sách nhóm theo ngày.
    Trạng thái và chiều lệnh nằm trong bảng Bộ lọc (Offcanvas từ dưới) để màn không chồng nhiều hàng chip và tab."""
    opts = ''.join(f'<option value="{k}"{" selected" if k == DEFAULT else ""}>{t}</option>' for k, t in PERIODS)
    period = f'<div class="arg-control arg-select"><select class="arg-select-native" data-oh-period-select aria-label="Khoảng thời gian">{opts}</select>{I("caret-down")}</div>'
    filt = (f'<button class="arg-btn arg-btn--outline2 arg-orderhist__filter" type="button" data-arg-open="oh-filter" aria-haspopup="dialog">{I("funnel")}Bộ lọc'
            f'<span class="arg-count" data-oh-fcount hidden>0</span></button>')
    radio = lambda name, k, t, on: f'<label class="arg-check arg-orderhist__opt"><input type="radio" name="oh-{name}" value="{k}" data-oh-{name}{" checked" if on else ""}><span class="box"></span>{t}</label>'
    chips = ''.join(radio('status', k, t, k == 'all') for k, t in CHIPS)
    sides = ''.join(radio('side', k, t, k == 'all') for k, t in (('all', 'Tất cả'), ('buy', 'Mua'), ('sell', 'Bán')))
    summary = ('<dl class="arg-statrow arg-orderhist__sum" aria-live="polite"><div class="arg-statrow__item"><dt>Mua khớp</dt><dd data-oh-buy>0</dd></div>'
               '<div class="arg-statrow__item"><dt>Bán khớp</dt><dd data-oh-sell>0</dd></div></dl>')
    groups = ''.join(f'<section class="arg-orderhist__day" data-oh-day aria-label="{day_title(d)}"><h3 class="arg-orderhist__date">{day_title(d)}<span data-oh-day-n></span></h3>'
                     f'<ul class="arg-orderrow-list">{"".join(row(o) for o in os)}</ul></section>' for d, os in days())
    sheet = (f'<div class="arg-offcanvas-wrap" id="oh-filter" hidden data-arg-offcanvas><aside class="arg-offcanvas arg-offcanvas--bottom arg-offcanvas--auto" role="dialog" aria-modal="true" aria-labelledby="oh-filter-t">'
             f'<div class="arg-modal__header"><h4 class="arg-modal__title" id="oh-filter-t">Bộ lọc lệnh</h4><button class="arg-icon-btn" type="button" data-arg-close aria-label="Đóng">{I("x", "i--20")}</button></div>'
             f'<div class="arg-modal__body arg-orderhist__opts"><div class="arg-orderhist__grp"><span class="arg-label" aria-hidden="true">Trạng thái</span><div class="arg-orderhist__radios" role="radiogroup" aria-label="Trạng thái lệnh">{chips}</div></div>'
             f'<div class="arg-orderhist__grp"><span class="arg-label" aria-hidden="true">Chiều lệnh</span><div class="arg-orderhist__radios" role="radiogroup" aria-label="Chiều lệnh">{sides}</div></div></div>'
             f'<div class="arg-modal__footer arg-orderhist__foot"><button class="arg-btn arg-btn--tertiary arg-btn--xl" type="button" data-oh-reset>Đặt lại</button><button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-arg-close data-oh-apply>Xem lệnh</button></div></aside></div>')
    return f'''<div class="arg-orderhist" data-arg-orderhist data-today="{TODAY.isoformat()}" data-period="{DEFAULT}">
  <div class="arg-orderhist__panel">
  <div class="arg-orderbook__filters arg-sidepanel">
  <div class="arg-orderhist__bar">{period}{filt}</div>
  <div class="arg-orderhist__range" data-oh-range hidden>{date_pair("oh")}</div>
  {summary}
  </div>
  <div class="arg-orderbook__results">
  <div class="arg-orderhist__list">{groups}</div>
  <p class="arg-orderbook__empty" data-oh-empty hidden>Không có lệnh trong khoảng thời gian và bộ lọc này.</p>
  </div>
  </div>
  {sheet}
</div>'''
