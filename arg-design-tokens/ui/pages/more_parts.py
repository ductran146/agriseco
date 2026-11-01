"""Màn Thêm: thẻ người dùng, các nhóm chức năng (dịch vụ tiền và lưu ký, thông tin thị trường, tài khoản và bảo mật, hỗ trợ), đăng xuất, chữ ký thương hiệu.
Họ tên và phiên bản là dữ liệu mẫu. Mục có đích dẫn tới màn đã có trong demo; mục chưa có màn dùng href="#" (giữ chỗ)."""
import re
from pathlib import Path
import info_parts as IP

I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'
_LOGO = (Path(__file__).resolve().parent / 'logo-agriseco.svg').read_text().replace('width="78" height="80" ', 'class="arg-logo" aria-hidden="true" ', 1)
LOGO = re.sub(r'\s+', ' ', _LOGO).strip()


def item(icon, label, meta='', go='', cls=''):
    attr = f' data-arg-go="{go}"' if go else ''
    m = f'<span class="arg-navlist__meta">{meta}</span>' if meta else ''
    return (f'<li><a class="arg-navlist__item{cls}" href="#"{attr}><span class="arg-navlist__icon">{I(icon)}</span><span class="arg-navlist__label">{label}</span>{m}'
            f'<span class="arg-navlist__go" aria-hidden="true">{I("caret-right")}</span></a></li>')


def group(title, items, i=0):
    return f'<div class="arg-page__block" data-sn-group="{i}"{" data-sn-active" if i == 0 else ""}>{IP.title(title)}<ul class="arg-navlist">{"".join(items)}</ul></div>'


NAMES = ('Tiền và lưu ký', 'Giao dịch và thị trường', 'Tài khoản và bảo mật', 'Hỗ trợ')


def screen(tabbar_html):
    profile = ('<div class="arg-profile"><i class="arg-brandmark arg-brandmark--soft arg-brandmark--corner" aria-hidden="true" style="--size:104px"></i>'
               '<span class="arg-profile__avatar" aria-hidden="true">A</span><div class="arg-profile__body"><p class="arg-profile__name">Nguyễn Văn An</p>'
               '<p class="arg-profile__sub">Tài khoản <b>C040899</b></p></div></div>')
    g = [
        group('Tiền và lưu ký', [item('card-receive-duotone', 'Nộp tiền'), item('card-send-duotone', 'Rút tiền'), item('transfer-horizontal-duotone', 'Chuyển khoản'),
                                 item('bill-list-duotone', 'Sao kê tiền', go='asset'), item('safe-square-duotone', 'Lưu ký'), item('safe-2-duotone', 'Rút lưu ký')], i=0),
        group('Giao dịch và thị trường', [item('clipboard-list-duotone', 'Sổ lệnh', go='orderbook'), item('magnifer-duotone', 'Tìm mã chứng khoán', go='search'),
                                          item('notes-duotone', 'Tin tức'), item('calendar-duotone', 'Lịch sự kiện')], i=1),
        group('Tài khoản và bảo mật', [item('user-circle-duotone', 'Thông tin tài khoản'), item('lock-keyhole-duotone', 'Đổi mật khẩu'), item('shield-check-duotone', 'Bảo mật và sinh trắc học'),
                                       item('bell-duotone', 'Cài đặt thông báo')], i=2),
        group('Hỗ trợ', [item('chat-round-dots-duotone', 'Liên hệ hỗ trợ'), item('question-circle-duotone', 'Câu hỏi thường gặp'), item('document-text-duotone', 'Điều khoản và chính sách'),
                         item('info-circle-duotone', 'Về Agriseco', 'Phiên bản 1.0')], i=3),
    ]
    nav = ''.join(f'<button class="arg-sidepanel__item" type="button" data-sn-btn="{i}" aria-pressed="{"true" if i == 0 else "false"}">{t}<i data-arg-icon="caret-right"></i></button>' for i, t in enumerate(NAMES))
    out = ('<div class="arg-page__block"><ul class="arg-navlist">' + item('logout-2-duotone', 'Đăng xuất', cls=' arg-navlist__item--danger') + '</ul>'
           f'<div class="arg-brandsign">{LOGO}<p class="arg-brandsign__name">Agriseco</p><p class="arg-brandsign__sub">Chứng khoán Agribank</p></div></div>')
    return f'''<div class="arg-screen arg-screen--sections" data-arg-screen="more" hidden>
<header class="arg-appbar arg-appbar--sticky"><h1 class="arg-appbar__title">Thêm</h1></header>
<main class="arg-page__main">
  <div class="arg-page__block arg-more__profile">{profile}</div>
  <div class="arg-sidenav" data-arg-sidenav>
    <nav class="arg-sidepanel arg-sidenav__nav" aria-label="Nhóm chức năng"><div class="arg-sidenav__user"><span class="arg-sidenav__avatar" aria-hidden="true">A</span><div class="arg-sidenav__who"><b>Nguyễn Văn An</b><span>Tài khoản <b>C040899</b></span></div></div><div class="arg-sidenav__list">{nav}</div>
      <div class="arg-sidenav__foot"><div class="arg-brandsign arg-brandsign--row">{LOGO}<div class="arg-brandsign__text"><p class="arg-brandsign__name">Agriseco</p><p class="arg-brandsign__sub">Chứng khoán Agribank</p></div></div><a class="arg-sidepanel__item arg-sidenav__logout" href="#">{I('logout-2-duotone')}Đăng xuất</a></div></nav>
    <div class="arg-sidenav__body">{''.join(g)}</div>
  </div>
  <div class="arg-sidenav__out">{out}</div>
</main>
{tabbar_html}
</div>'''
