"""Markup cho màn Tìm kiếm (component search, quote, input, button).
Dữ liệu mẫu: mã lấy từ bảng giá HOSE mẫu (market.universe), tên đầy đủ nếu có trong market.FULL; ngôi sao đã chọn sẵn VCB, HPG; tìm gần đây là danh sách mẫu."""
import unicodedata
from market import universe, FULL

I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'
RECENT = ('CTG', 'MSN', 'BID', 'NVL', 'VCB')
FAV = ('VCB', 'HPG')


def fold(t):
    return unicodedata.normalize('NFD', t.lower().replace('đ', 'd')).encode('ascii', 'ignore').decode()


def result_li(r):
    name = FULL.get(r.code, r.name)
    idt = (f'<a class="arg-quote__id" href="#" data-arg-go="{r.go}" aria-label="Xem thông tin {r.code}"><b>{r.code}</b><span>{name}</span></a>' if r.go
           else f'<div class="arg-quote__id"><b>{r.code}</b><span>{name}</span></div>')
    on = r.code in FAV
    star = (f'<button class="arg-fav" type="button" data-arg-fav-toggle aria-pressed="{"true" if on else "false"}" aria-label="{"Bỏ" if on else "Thêm"} {r.code} {"khỏi" if on else "vào"} danh mục theo dõi" '
            f'data-label-on="Bỏ {r.code} khỏi danh mục theo dõi" data-label-off="Thêm {r.code} vào danh mục theo dõi">'
            f'<span class="arg-fav__on">{I("star-fill")}</span><span class="arg-fav__off">{I("star")}</span></button>')
    return f'<li class="arg-search__row" data-code="{r.code}" data-q="{fold(r.code + " " + name)}">{idt}{star}</li>'


def recent_li(code):
    return (f'<li class="arg-search__row"><button class="arg-search__pick" type="button" data-arg-search-pick="{code}">{I("magnifying-glass")}<b>{code}</b></button>'
            f'<button class="arg-icon-btn" type="button" data-arg-search-remove aria-label="Xoá {code} khỏi tìm gần đây">{I("x", "i--20")}</button></li>')


def body(value=''):
    """Phần thân dùng chung cho màn hình và ví dụ trong viewer: thanh đầu, tìm gần đây, kết quả."""
    rows = sorted(universe('hose'), key=lambda r: r.code)
    return f'''<header class="arg-appbar arg-appbar--sticky arg-search__bar"><button class="arg-appbar__tool" type="button" data-arg-back aria-label="Quay lại">{I('caret-left')}</button>
<div class="arg-control">{I('magnifying-glass')}<input class="arg-input" type="search" enterkeyhint="search" placeholder="Tìm mã, tên công ty" aria-label="Tìm mã, tên công ty" autocomplete="off" value="{value}" data-arg-search-input><button class="arg-icon-btn arg-search__clear" type="button" data-arg-search-clear aria-label="Xoá chữ đã nhập" hidden>{I('x', 'i--16')}</button></div></header>
<main class="arg-page__main">
  <section class="arg-search__recent" data-arg-search-recent aria-labelledby="sr-t">
    <div class="arg-search__head"><h2 class="arg-search__title" id="sr-t">Tìm kiếm gần đây</h2><button class="arg-icon-btn" type="button" data-arg-search-clear-all aria-label="Xoá lịch sử tìm kiếm">{I('trash', 'i--24')}</button></div>
    <ul class="arg-search__list">{''.join(recent_li(c) for c in RECENT)}</ul>
    <p class="arg-search__none" data-arg-search-empty hidden>Chưa có tìm kiếm nào gần đây.</p>
  </section>
  <ul class="arg-search__list arg-search__results" data-arg-search-results aria-label="Kết quả tìm kiếm" hidden>{''.join(result_li(r) for r in rows)}</ul>
  <p class="arg-search__none" data-arg-search-none hidden>Không tìm thấy mã phù hợp.</p>
</main>'''


def screen():
    return f'<div class="arg-screen arg-screen--plain" data-arg-screen="search" data-arg-search hidden>\n{body()}\n</div>'
