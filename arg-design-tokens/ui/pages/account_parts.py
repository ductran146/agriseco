"""Thẻ tài sản ở trang chủ (component Account). Số lấy từ danh mục mẫu trong stocks.py để khớp trang thông tin mã:
tổng tài sản = tiền mặt (bằng sức mua của tiểu khoản thường X1) + giá trị cổ phiếu theo giá khớp."""
from detail_parts import I, vn
from stocks import STOCKS, BUYING_POWER

num = lambda n: f'{n:,}'.replace(',', '.')
sgn = lambda n: ('+' if n > 0 else '') + num(n)


def figures():
    held = [s for s in STOCKS if s.hold]
    stock = round(sum(s.last * s.hold[0] * 1000 for s in held))
    cost = round(sum(s.hold[1] * s.hold[0] * 1000 for s in held))
    today = round(sum(s.chg * s.hold[0] * 1000 for s in held))
    cash = BUYING_POWER
    total = cash + stock
    return dict(total=total, cash=cash, stock=stock, today=today, today_pct=today / (total - today) * 100,
                pl=stock - cost, pl_pct=(stock - cost) / cost * 100, stock_pct=round(stock / total * 100))


def chips(items):
    b = ''.join(f'<button class="arg-chip-tab" role="tab" type="button" aria-selected="{"true" if i == 0 else "false"}">{t}</button>' for i, t in enumerate(items))
    return f'<div class="arg-chip-tabs" data-arg-tabs><div class="arg-chip-tabs__list" role="tablist" aria-label="Tiểu khoản">{b}</div></div>'


def account(no='C040899', initials='AN'):
    f = figures()
    trend = 'trend-up' if f['today'] >= 0 else 'trend-down'
    pl_cls = 'arg-up' if f['pl'] > 0 else 'arg-down' if f['pl'] < 0 else 'arg-ref'
    sp = f['stock_pct']
    return f'''<section class="arg-account" aria-label="Tài sản">
  <div class="arg-account__head">
    <div class="arg-account__top"><span class="arg-account__label">Tổng tài sản (đ)<button class="arg-account__eye" type="button" data-arg-account-eye aria-label="Ẩn số dư">{I('eye-slash')}</button></span><span class="arg-account__avatar" aria-hidden="true">{initials}</span></div>
    <b class="arg-account__amount" data-arg-secret>{num(f['total'])}</b>
    <span class="arg-account__delta">{I(trend)}Hôm nay <b data-arg-secret>{sgn(f['today'])}</b> ({vn(f['today_pct'], 2, True)}%)</span>
    <div class="arg-account__alloc"><div class="arg-account__bar" style="--v:{sp}" role="img" aria-label="Cổ phiếu {sp}%, tiền mặt {100 - sp}%"></div>
      <dl class="arg-account__split"><div><dt><i class="arg-account__dot"></i>Cổ phiếu · {sp}%</dt><dd data-arg-secret>{num(f['stock'])}</dd></div><div><dt><i class="arg-account__dot arg-account__dot--cash"></i>Tiền mặt · {100 - sp}%</dt><dd data-arg-secret>{num(f['cash'])}</dd></div></dl></div>
  </div>
  <div class="arg-account__body"><span class="arg-account__no">Tài khoản <b>{no}</b></span>
    {chips(['X1', 'M1', 'D1', 'Ảo'])}
    <div class="arg-account__foot"><div class="arg-account__pl"><span>Lãi/lỗ danh mục</span><b class="{pl_cls}"><span data-arg-secret>{sgn(f['pl'])}</span> ({vn(f['pl_pct'], 2, True)}%)</b></div><button class="arg-btn arg-btn--primary" type="button">Nộp tiền</button></div>
  </div>
</section>'''
