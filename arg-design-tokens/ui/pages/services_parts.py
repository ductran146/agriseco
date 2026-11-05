"""Dịch vụ nhanh: danh mục dịch vụ mẫu, lưới ở Trang chủ và màn Tuỳ chỉnh (component service, svcedit, reorder).
Lựa chọn của người dùng lưu trong sessionStorage ('arg-services' = danh sách id theo thứ tự); Trang chủ đọc lại khi mở."""
import html, json

I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'
MAX = 6
# (id, tên, icon duotone) theo nhóm; icon dùng chung với thanh tab và lưới ở Trang chủ
GROUPS = [
    ('Giao dịch chứng khoán', [('orders', 'Sổ lệnh', 'clipboard-list-duotone'), ('history', 'Lịch sử lệnh', 'document-text-duotone'), ('confirm', 'Xác nhận lệnh', 'shield-check-duotone'),
                               ('conditional', 'Lệnh điều kiện', 'notes-duotone'), ('stock-transfer', 'Chuyển khoản chứng khoán', 'arrows-left-right-duotone'), ('rights', 'Quyền mua', 'cart-plus-duotone'),
                               ('deposit-stock', 'Lưu ký', 'safe-square-duotone'), ('withdraw-stock', 'Rút lưu ký', 'safe-2-duotone')]),
    ('Giao dịch tiền', [('cash-in', 'Nộp tiền', 'card-receive-duotone'), ('cash-out', 'Rút tiền', 'card-send-duotone'), ('transfer', 'Chuyển khoản', 'transfer-horizontal-duotone'),
                        ('advance', 'Ứng trước tiền bán', 'piggy-bank-duotone'), ('margin', 'Hoàn trả margin', 'download-simple-duotone'), ('statement', 'Sao kê tiền', 'bill-list-duotone')]),
]
CATALOG = {i: {'id': i, 'label': n, 'icon': ic} for _, items in GROUPS for i, n, ic in items}
DEFAULT = ['orders', 'cash-in', 'transfer', 'statement', 'deposit-stock', 'withdraw-stock']   # khớp lưới Trang chủ ban đầu
CAT_ATTR = html.escape(json.dumps(CATALOG, ensure_ascii=False, separators=(',', ':')), quote=True)


def tile(d):
    return f'<a class="arg-service" href="#" data-id="{d["id"]}"><span class="arg-service__icon">{I(d["icon"])}</span><span class="arg-service__label">{d["label"]}</span></a>'


def home_grid():
    """Lưới Dịch vụ nhanh ở Trang chủ; service.js dựng lại theo lựa chọn đã lưu."""
    return f'<div class="arg-service-grid arg-service-grid--card" data-arg-catalog="{CAT_ATTR}">' + ''.join(tile(CATALOG[i]) for i in DEFAULT) + '</div>'


def edit_tile(d):
    return (f'<li class="arg-svcedit__tile" data-id="{d["id"]}"><button class="arg-svcedit__remove" type="button" data-svc-remove aria-label="Bỏ {d["label"]} khỏi dịch vụ nhanh">{I("minus")}</button>'
            f'<span class="arg-service__icon">{I(d["icon"])}</span><span class="arg-service__label">{d["label"]}</span></li>')


def edit_row(d, fav):
    add = '' if fav else f'<button class="arg-svcedit__add" type="button" data-svc-add aria-label="Thêm {d["label"]} vào dịch vụ nhanh">{I("plus-circle")}</button>'
    return f'<li class="arg-svcedit__row" data-id="{d["id"]}"><span class="arg-svcedit__icon">{I(d["icon"])}</span><span class="arg-svcedit__name">{d["label"]}</span>{add}</li>'


def title(text):
    return f'<div class="arg-title arg-title--md"><div class="arg-title__left"><div class="arg-title__main"><div class="arg-title__text" role="heading" aria-level="2">{text}</div></div></div></div>'


def screen():
    groups = ''.join(f'<div class="arg-page__block">{title(name)}<ul class="arg-svcedit__list" data-svc-group>' + ''.join(edit_row(CATALOG[i], i in DEFAULT) for i, _, _ in items) + '</ul></div>' for name, items in GROUPS)
    return f'''<div class="arg-screen arg-screen--plain" data-arg-screen="services" data-arg-svcedit data-arg-catalog="{CAT_ATTR}" data-max="{MAX}" hidden>
<header class="arg-appbar arg-appbar--sticky"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I('caret-left')}</button><h1 class="arg-appbar__title">Tuỳ chỉnh dịch vụ nhanh</h1></header>
<main class="arg-page__main">
  <div class="arg-page__block">{title('Dịch vụ nhanh')}<p class="arg-svcedit__hint">Giữ và kéo thẻ để đổi vị trí. Đã chọn <b data-svc-count>{len(DEFAULT)}</b>/{MAX} dịch vụ.</p>
    <ul class="arg-svcedit__grid" data-arg-reorder="grid" aria-label="Dịch vụ nhanh">{''.join(edit_tile(CATALOG[i]) for i in DEFAULT)}</ul><p class="arg-svcedit__empty" data-svc-empty hidden>Chưa có dịch vụ nào. Thêm từ danh sách bên dưới.</p></div>
  {groups}
</main>
<div class="arg-actionbar arg-actionbar--fixed"><button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-svc-save disabled>Lưu</button></div>
</div>'''
