"""Logo Agriseco là SVG nội tuyến có gradient đặt tên bằng id (paint0_linear_1080_30961...). Khi một trang chứa nhiều bản logo (thanh đầu, màn chào, chữ ký cuối trang)
thì id trùng nhau và trình duyệt lấy gradient ở bản đầu tiên trong tài liệu. Bản đó bị gỡ hoặc ẩn (màn chào tự gỡ sau ~1 giây) thì mọi logo còn lại mất màu,
chỉ còn chữ trắng. Hàm này đánh số lại id cho từng bản logo để không bản nào phụ thuộc bản khác."""
import re

_OLD = '_1080_30961'


def unique_logo_ids(html):
    n = [0]

    def one(m):
        n[0] += 1
        return m.group(0).replace(_OLD, f'{_OLD}_{n[0]}')
    return re.sub(r'<svg[^>]*class="arg-logo".*?</svg>', one, html, flags=re.S)
