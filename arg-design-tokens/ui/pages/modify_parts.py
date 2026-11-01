"""Markup cho màn Sửa lệnh (component ordermodify, bidask, side, stepper, selectsheet, kv, actionbar, ordermodal).
Chỉ lệnh LO còn hiệu lực (Chờ khớp, Khớp một phần) sửa được; chiều lệnh và loại lệnh bị khoá, chỉ sửa giá và khối lượng.
Lite: dư mua, dư bán nằm ngang; Pro: sổ lệnh bên trái, trường nhập bên phải."""
import trade_parts as TP
from detail_parts import vn
from stocks import BY_CODE, BUYING_POWER

num = TP.num
I = TP.I


def modifiable(o):
    """Lệnh sửa được: loại LO và còn hiệu lực."""
    return o[4] == 'LO' and o[9] in ('pending', 'partial')


def modify_id(o):
    return 'modify-' + o[0].lower()


def bidask(st):
    """Dư mua (trái), dư bán (phải): tổng khối lượng, tỷ lệ và 3 mức giá tốt nhất mỗi bên."""
    sb, sa = sum(v for _, v in st.bids), sum(v for _, v in st.asks)
    pb = round(sb / (sa + sb) * 100)
    mx = max(v for _, v in st.bids + st.asks)
    side = lambda k, name, tot, pct, rows: (f'<div class="arg-bidask__side arg-bidask__side--{k}"><div class="arg-bidask__head"><b>{name}</b><span>Tổng <b>{num(tot)}</b> ({pct}%)</span></div>'
                                             + ''.join(f'<div class="arg-bidask__row" style="--w:{round(v / mx * 100)}">' + (f'<span class="arg-bidask__vol">{num(v)}</span><span class="{st.cls(p)}">{vn(p)}</span>' if k == 'bid' else f'<span class="{st.cls(p)}">{vn(p)}</span><span class="arg-bidask__vol">{num(v)}</span>') + '</div>' for p, v in rows) + '</div>')
    return '<div class="arg-bidask">' + side('bid', 'Dư mua', sb, pb, st.bids) + side('ask', 'Dư bán', sa, 100 - pb, st.asks) + '</div>'


def locked_side(side):
    b, s = ('true', 'false') if side == 'buy' else ('false', 'true')
    return (f'<div class="arg-side arg-locked" role="group" aria-label="Chiều lệnh (không đổi được)"><button class="arg-side__btn arg-side__btn--buy" type="button" aria-pressed="{b}" disabled>Mua</button>'
            f'<button class="arg-side__btn arg-side__btn--sell" type="button" aria-pressed="{s}" disabled>Bán</button></div>')


def locked_type():
    return ('<div class="arg-control arg-select arg-select--center arg-selectsheet arg-locked"><span class="arg-control__label">Loại</span><select class="arg-select-native" tabindex="-1" aria-label="Loại lệnh (không đổi được)" disabled>'
            '<option>LO</option></select>' + I('caret-down') + '</div>')


def kv(st, px, qty, side, lite=False):
    sell = side == 'sell'
    cap = (st.hold[0] if st.hold else qty) if sell else st.max_qty
    return ('<dl class="arg-kv"><div class="arg-kv__row"><dt>Sức mua<button class="arg-icon-btn" type="button" aria-label="Giải thích sức mua">' + I('info') + f'</button></dt><dd>{num(BUYING_POWER)}</dd></div>'
            + ('' if lite else '<div class="arg-kv__row"><dt>Tỷ lệ ký quỹ</dt><dd>50%</dd></div>')
            + ('' if lite else f'<div class="arg-kv__row"><dt>KL {"bán" if sell else "mua"} tối đa</dt><dd>{num(cap)}</dd></div>')
            + f'<div class="arg-kv__row arg-kv__row--total"><dt>Giá trị ước tính</dt><dd data-arg-order-total>{num(round(px * qty * 1000))}</dd></div></dl>')


def form(st, o, lite):
    oid, time, code, side, typ, px, qty, matched, avg, status = o
    head = (f'<form class="arg-order{" arg-lite" if lite else ""}" data-arg-order data-side="{side}" data-symbol="{code}" data-om-price="{vn(px)}" data-om-qty="{num(qty)}" onsubmit="return false">')
    price = TP.stepper('Giá', TP._step(st), 2, vn(px), 'price')
    q = TP.stepper('Khối lượng', '100', 0, num(qty), 'qty', short='KL')
    if lite:
        cap = (st.hold[0] if st.hold else qty) if side == 'sell' else st.max_qty
        hint = f'<p class="arg-ordermodify__hint">KL {"bán" if side == "sell" else "mua"} tối đa: {num(cap)}</p>'
        return head + bidask(st) + locked_type() + price + q + hint + kv(st, px, qty, side, True) + '</form>'
    return (head + f'<div class="arg-split"><div>{TP.view_switch(st)}</div><div>{locked_side(side)}{locked_type()}{price}{q}{kv(st, px, qty, side)}</div></div></form>')


MODAL = '''<div class="arg-overlay" id="om-confirm" hidden data-arg-modal data-om-modal>
  <div class="arg-modal arg-modal--sm arg-ordermodal" role="alertdialog" aria-modal="true" aria-labelledby="om-confirm-t">
    <div class="arg-modal__header"><h4 class="arg-modal__title" id="om-confirm-t" data-ord="title">Sửa lệnh</h4></div>
    <div class="arg-modal__body"><dl class="arg-kv arg-kv--lines">
      <div class="arg-kv__row"><dt>Giá</dt><dd data-ord="price"></dd></div>
      <div class="arg-kv__row"><dt>Khối lượng</dt><dd data-ord="qty"></dd></div>
      <div class="arg-kv__row"><dt>Loại lệnh</dt><dd data-ord="type">LO</dd></div>
      <div class="arg-kv__row"><dt>Giá trị ước tính</dt><dd data-ord="value"></dd></div>
    </dl></div>
    <div class="arg-modal__footer arg-ordermodal__actions"><button class="arg-btn arg-btn--tertiary arg-btn--xl" type="button" data-arg-close>Huỷ</button><button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-om-ok>Xác nhận sửa</button></div>
  </div>
</div>
<div class="arg-overlay arg-overlay--blur" id="om-done" hidden data-arg-modal data-om-done>
  <div class="arg-modal arg-modal--sm arg-ordermodal arg-ordermodal--done" role="dialog" aria-modal="true" aria-labelledby="om-done-t">
    <div class="arg-modal__body">
      <span class="arg-modal__icon arg-modal__icon--success arg-modal__icon--lg"><i data-arg-icon="seal-check"></i></span>
      <h4 class="arg-modal__title" id="om-done-t">Sửa lệnh thành công</h4>
      <span data-ord="done"></span>
    </div>
    <div class="arg-modal__footer arg-ordermodal__actions arg-ordermodal__actions--stack"><button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-arg-go="orderbook" data-arg-close>Xem sổ lệnh</button></div>
  </div>
</div>'''


def screen(o):
    st = BY_CODE[o[2]]
    return f'''<div class="arg-screen arg-screen--plain" data-arg-screen="{modify_id(o)}" data-arg-modify data-mode="pro" hidden>
<header class="arg-appbar arg-appbar--sticky"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I('caret-left')}</button><h1 class="arg-appbar__title">Sửa lệnh</h1></header>
<main class="arg-page__main arg-page__main--dense arg-page__main--fit">
  {TP.symbol(st.code, st.ex)}
  {TP.quote_head(st)}
  {TP.stats(st)}
  <div class="arg-trade--pro">{form(st, o, False)}</div>
  <div class="arg-trade--lite">{form(st, o, True)}</div>
</main>
<div class="arg-actionbar arg-actionbar--fixed"><button class="arg-btn arg-btn--tertiary arg-btn--xl" type="button" data-arg-back>Huỷ</button><button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-om-submit disabled>Sửa lệnh</button></div>
{MODAL}
</div>'''
