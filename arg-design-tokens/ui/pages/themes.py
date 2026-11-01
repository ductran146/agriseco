"""Dữ liệu mẫu cho tab Chủ đề và trang chi tiết chủ đề (19 nhóm ngành, ảnh trong images/themes).
Mã đã có trong sàn HOSE mẫu (market.universe) dùng đúng giá và % của bảng giá; mã bổ sung chỉ là số mẫu sinh cố định theo mã.
Vốn hoá, P/E, P/B, cơ cấu sở hữu bình quân của chủ đề cũng là số mẫu (không phải số thật)."""
import random
from market import universe, Row

# (slug, tên hiển thị, tên file ảnh trong images/themes, màu nền ảnh, mã thành viên)
THEMES = [
    ('automobiles', 'Ô tô và phụ tùng', '01-Automobiles & Parts', '#d1e1ee', ('VIC', 'HAX', 'SVC')),
    ('bank', 'Ngân hàng', '02-Bank', '#f3ece6', ('VCB', 'CTG', 'BID', 'VPB', 'HDB', 'SSB', 'LPB', 'STB')),
    ('basic-resources', 'Tài nguyên cơ bản', '03-Basic Resources', '#ced5db', ('HPG', 'GVR', 'HSG', 'NKG')),
    ('chemicals', 'Hoá chất', '04-Chemicals', '#b2d9e8', ('DGC', 'DPM', 'DCM', 'BFC')),
    ('construction', 'Xây dựng và vật liệu', '05-Construction & Materials', '#f0cd96', ('GEX', 'VCG', 'CTD', 'HT1')),
    ('financial-services', 'Dịch vụ tài chính', '06-Financial Services', '#59b8e2', ('SSI', 'VIX', 'AGR', 'VND', 'HCM')),
    ('food-beverage', 'Thực phẩm và đồ uống', '07-Food & Beverage', '#f4e8da', ('VNM', 'MSN', 'SAB', 'KDC', 'DBC')),
    ('health-care', 'Chăm sóc sức khoẻ', '08-Health Care', '#d8ebe7', ('DHG', 'IMP', 'TNH')),
    ('industrial', 'Hàng và dịch vụ công nghiệp', '09-Industrial Goods & Services', '#dce1e7', ('GMD', 'HAH', 'VSC')),
    ('insurance', 'Bảo hiểm', '10-Insurance', '#c9d8c1', ('BVH', 'MIG', 'BMI')),
    ('media', 'Truyền thông', '11-Media', '#eed8da', ('ADG', 'YEG', 'VTV')),
    ('oil-gas', 'Dầu khí', '12-Oil & Gas', '#ccc2b8', ('GAS', 'PVD', 'PLX', 'BSR')),
    ('personal-household', 'Hàng cá nhân và gia dụng', '13-Personal & Household Goods', '#abdaf6', ('PNJ', 'TCM', 'GIL')),
    ('real-estate', 'Bất động sản', '14-Real Estate', '#eef6df', ('VHM', 'VRE', 'DXG', 'HQC', 'NVL')),
    ('retail', 'Bán lẻ', '15-Retail', '#f4eee0', ('MWG', 'DGW', 'FRT', 'PET')),
    ('technology', 'Công nghệ', '16-Technology', '#7bd0ef', ('FPT', 'CMG', 'ELC')),
    ('telecom', 'Viễn thông', '17-Telecommunications', '#7cc1de', ('VGI', 'CTR', 'FOX')),
    ('travel-leisure', 'Du lịch và giải trí', '18-Travel & Leisure', '#83c9c9', ('VJC', 'HVN', 'SCS')),
    ('utilities', 'Tiện ích', '19-Utilities', '#f7f7ed', ('POW', 'REE', 'PC1', 'NT2')),
]

# Tên rút gọn của mã bổ sung (không có trong bảng giá mẫu)
EXTRA = {'HAX': 'Ô tô Hàng Xanh', 'SVC': 'Savico', 'HSG': 'Tôn Hoa Sen', 'NKG': 'Thép Nam Kim', 'DPM': 'Phân bón Dầu khí', 'DCM': 'Đạm Cà Mau', 'BFC': 'Phân bón Bình Điền',
         'VCG': 'Vinaconex', 'CTD': 'Coteccons', 'HT1': 'Xi măng Hà Tiên 1', 'VND': 'Chứng khoán VNDirect', 'HCM': 'Chứng khoán HSC', 'SAB': 'Sabeco', 'KDC': 'KIDO',
         'DBC': 'Dabaco', 'DHG': 'Dược Hậu Giang', 'IMP': 'Dược Imexpharm', 'TNH': 'Bệnh viện Thái Nguyên', 'GMD': 'Gemadept', 'HAH': 'Vận tải Hải An', 'VSC': 'Container Việt Nam',
         'BVH': 'Tập đoàn Bảo Việt', 'MIG': 'Bảo hiểm Quân đội', 'BMI': 'Bảo hiểm Bảo Minh', 'ADG': 'Clever Group', 'YEG': 'Yeah1', 'VTV': 'VTV Cab', 'PVD': 'Khoan Dầu khí',
         'PLX': 'Petrolimex', 'BSR': 'Lọc hoá dầu Bình Sơn', 'PNJ': 'Vàng bạc Phú Nhuận', 'TCM': 'Dệt may Thành Công', 'GIL': 'Gilimex', 'DGW': 'Digiworld', 'FRT': 'FPT Retail',
         'PET': 'Petrolimex Dịch vụ', 'CMG': 'CMC', 'ELC': 'Elcom', 'VGI': 'Viettel Global', 'CTR': 'Viettel Construction', 'FOX': 'FPT Telecom', 'VJC': 'Vietjet', 'HVN': 'Vietnam Airlines',
         'SCS': 'Dịch vụ hàng hoá Sài Gòn', 'POW': 'PV Power', 'REE': 'Cơ điện lạnh REE', 'PC1': 'Xây lắp điện 1', 'NT2': 'Điện lực Dầu khí Nhơn Trạch 2'}


def _rows():
    by = {r.code: r for r in universe('hose')}
    def get(c):
        if c in by: return by[c]
        r = random.Random('theme-' + c)
        price = round(r.uniform(8, 110), 2); pct = round(r.uniform(-3.2, 3.2), 2)
        return Row(c, EXTRA[c], price, pct, round(r.uniform(.4, 18), 1), 0, 0, 0)
    return get


def build():
    """Danh sách chủ đề kèm dữ liệu tổng hợp, mỗi chủ đề là dict."""
    get = _rows(); out = []
    for slug, name, img, tint, codes in THEMES:
        rows = [get(c) for c in codes]
        r = random.Random('theme-' + slug)
        avg = round(sum(x.pct for x in rows) / len(rows), 2)
        foreign, retail = r.randint(6, 30), r.randint(28, 52)
        out.append(dict(slug=slug, id='theme-' + slug, name=name, img=img, tint=tint, rows=rows, avg=avg,
                        kind='up' if avg > 0 else 'down' if avg < 0 else 'ref', up=sum(x.pct > 0 for x in rows),
                        cap=r.randint(18, 420) * 1000 + r.randint(0, 9) * 100, vol=round(sum(x.vol for x in rows), 1),
                        pe=round(r.uniform(8, 24), 1), pb=round(r.uniform(.9, 3.6), 1),
                        own=[('Nước ngoài', foreign), ('Tổ chức', 100 - foreign - retail), ('Cá nhân', retail)]))
    return out


THEME_DATA = build()
