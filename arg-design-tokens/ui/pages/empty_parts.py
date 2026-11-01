"""Màn Thêm (mục chưa làm trong demo): empty state gồm hình minh hoạ thư mục trống, tiêu đề, giải thích và nút về trang chủ (component emptystate).
Hình minh hoạ do chủ dự án cung cấp (ui/components/emptystate/empty-folder.svg), không thuộc bộ icon Solar."""
from pathlib import Path

I = lambda n, c='': f'<i data-arg-icon="{n}"{f" class=\"{c}\"" if c else ""}></i>'
ART = (Path(__file__).resolve().parent.parent / 'components/emptystate/empty-folder.svg').read_text().replace('<svg width="292" height="326"', '<svg class="arg-empty__art" role="img" aria-label="Thư mục trống" width="292" height="326"', 1)


def empty(title, text, action=''):
    return f'<div class="arg-empty">{ART}<h2 class="arg-empty__title">{title}</h2><p class="arg-empty__text">{text}</p>{action}</div>'


def screen(tabbar_html):
    btn = f'<button class="arg-btn arg-btn--primary arg-btn--xl" type="button" data-arg-go="home">Về trang chủ</button>'
    return f'''<div class="arg-screen arg-screen--plain" data-arg-screen="more" hidden>
<header class="arg-appbar arg-appbar--sticky"><h1 class="arg-appbar__title">Thêm</h1></header>
<main class="arg-page__main arg-page__main--dense">
  {empty('Mục này đang được hoàn thiện', 'Các tiện ích trong mục Thêm chưa có trong bản demo lần này. Chúng tôi sẽ bổ sung ở những phiên bản sau.', btn)}
</main>
{tabbar_html}
</div>'''
