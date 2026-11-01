"""Dữ liệu mẫu màn Thị trường (không phải số thật), thời điểm 10:15 ngày 29/10/2026.
Nhất quán với phần còn lại của demo:
- Số mã tăng, đứng, giảm và giá trị giao dịch của HNX, UPCoM bằng trang chi tiết chỉ số HNX, UPCoM.
- Tổng điểm kéo lên trừ kéo xuống bằng thay đổi của chỉ số (HNX 0,00; UPCoM +0,22).
- 8 mã có trang thông tin (stocks.py) lấy giá, %, khối lượng, khối ngoại từ đó; điểm tác động = vốn hoá × % / tổng vốn hoá sàn × điểm chỉ số.
- Phân bố theo khoảng % cộng lại đúng số mã tăng, đứng, giảm; mỗi mã nằm đúng khoảng của %."""
import random
from stocks import STOCKS, BY_CODE

EXCHANGES = (('hose', 'HOSE'), ('hnx', 'HNX'), ('upcom', 'UPCoM'))
LIM = {'hose': 7, 'hnx': 10, 'upcom': 15}   # biên độ giá (%)
BINS = ('≤-7', '-7÷-5', '-5÷-3', '-3÷-1', '-1÷0', '0', '0÷1', '1÷3', '3÷5', '5÷7', '≥7')

# Sàn: số mã tăng, đứng, giảm; giá trị khớp (tỷ) của nhóm mã tăng, đứng, giảm; KL (triệu CP); phân bố 5 khoảng giảm và 5 khoảng tăng;
# tổng điểm kéo lên / kéo xuống chỉ số; khối ngoại hôm nay (mua, bán, tỷ); tự doanh (mua, bán, tỷ); giá trị khớp cùng giờ 4 phiên trước (tỷ)
EX = {
    'hose': dict(breadth=(187, 63, 89), flow=(4216.3, 342.8, 1413.9), vol=412.6, down=(2, 5, 14, 31, 37), up=(52, 71, 38, 19, 7), impact=(7.05, -3.46),
                 foreign=(1845.62, 1912.34), prop=(612.40, 548.15), prev=(5210.4, 6340.8, 5892.6, 5487.1), amp=180),
    'hnx': dict(breadth=(96, 70, 94), flow=(612.4, 395.1, 516.2), vol=87.2, down=(3, 6, 15, 32, 38), up=(30, 34, 18, 10, 4), impact=(0.48, -0.48),
                foreign=(96.35, 88.12), prop=(31.20, 35.85), prev=(1402.6, 1610.3, 1588.0, 1466.9), amp=26),
    'upcom': dict(breadth=(210, 150, 130), flow=(538.9, 284.6, 279.3), vol=156.4, down=(4, 9, 22, 41, 54), up=(58, 70, 44, 26, 12), impact=(0.39, -0.17),
                  foreign=(74.80, 61.45), prop=(18.60, 15.25), prev=(980.2, 1150.6, 1204.5, 1061.0), amp=18),
}

# Mã mẫu khác (không có trang thông tin): mã, tên, giá, %, KL (triệu), điểm tác động, khối ngoại ròng (tỷ), tự doanh ròng (tỷ)
OTHERS = {
    'hose': [('VHM', 'Vinhomes', 46.20, 2.10, 8.6, 1.60, 38.6, 12.4), ('VPB', 'VPBank', 19.85, 1.53, 25.4, 1.07, 9.8, 6.1), ('SSI', 'Chứng khoán SSI', 27.45, 1.67, 18.2, .91, 16.4, -3.2),
             ('GEX', 'Tập đoàn GELEX', 21.65, 2.85, 14.1, .73, 4.1, 2.0), ('VIX', 'Chứng khoán VIX', 13.30, 3.91, 32.5, .55, -6.2, 0), ('HDB', 'HDBank', 24.30, 1.46, 7.3, .52, -28.7, 1.5),
             ('SSB', 'SeABank', 18.95, 1.34, 5.8, .49, 2.2, 0), ('FPT', 'FPT', 118.40, -.34, 3.9, -.16, 45.2, -4.5), ('MWG', 'Thế Giới Di Động', 61.30, -1.20, 6.2, -.35, 22.1, 3.3),
             ('VNM', 'Vinamilk', 63.10, -.94, 4.1, -.24, -52.3, -7.8), ('GAS', 'PV GAS', 66.90, -.74, 1.4, -.22, -3.5, 0), ('GVR', 'Cao su Việt Nam', 30.40, -1.46, 3.3, -.42, -8.4, -1.1),
             ('LPB', 'LPBank', 32.60, -.61, 2.7, -.18, 1.3, 0), ('STB', 'Sacombank', 36.85, -.40, 9.4, -.10, -19.6, 2.6), ('VRE', 'Vincom Retail', 23.15, -.64, 5.0, -.08, -14.2, 0),
             ('DGC', 'Hoá chất Đức Giang', 98.60, -1.10, 1.7, -.09, -12.8, -2.1),
             ('DXG', 'Đất Xanh Group', 16.05, 7.00, 21.4, .12, 1.2, 0), ('HQC', 'Địa ốc Hoàng Quân', 2.79, -7.00, 12.3, -.01, -.3, 0)],
    'hnx': [('SHS', 'Chứng khoán SHS', 16.80, 1.82, 15.4, .12, 3.2, 1.1), ('PVS', 'Dịch vụ Kỹ thuật Dầu khí', 33.70, 1.20, 6.1, .09, 5.6, -.8), ('CEO', 'Tập đoàn C.E.O', 13.90, 2.21, 9.8, .05, -1.4, .3),
            ('IDC', 'IDICO', 52.30, .58, 1.9, .04, 2.1, 0), ('MBS', 'Chứng khoán MB', 27.10, .74, 4.3, .03, -.9, .6), ('DTD', 'Đầu tư Phát triển Thành Đạt', 28.60, .35, .6, .02, .2, 0),
            ('PVI', 'PVI Holdings', 51.00, -1.35, .3, -.10, -.4, 0), ('VCS', 'Vicostone', 55.20, -1.08, .2, -.07, -1.2, -.2), ('NTP', 'Nhựa Tiền Phong', 61.80, -.96, .4, -.05, .5, 0),
            ('HUT', 'Tasco', 17.40, -.57, 3.2, -.04, -2.3, -.5), ('L14', 'Licogi 14', 37.20, -.80, .3, -.02, -.1, 0)],
    'upcom': [('ACV', 'Cảng Hàng không Việt Nam', 112.50, 1.26, 1.2, .11, 4.8, .6), ('BSR', 'Lọc hoá dầu Bình Sơn', 21.40, 1.42, 12.6, .07, 3.9, 1.4), ('VEA', 'VEAM', 41.30, .98, .8, .05, 1.1, 0),
              ('MCH', 'Masan Consumer', 128.00, .79, .5, .04, 2.6, .3), ('QNS', 'Đường Quảng Ngãi', 48.90, .62, .9, .02, -.7, 0), ('OIL', 'PV OIL', 12.80, .79, 5.4, .02, -1.6, -.4),
              ('MML', 'Masan MEATLife', 32.50, -1.22, .1, -.03, -.2, 0), ('VTP', 'Viettel Post', 118.20, -.92, .4, -.02, -2.4, -.3), ('SIP', 'Saigon VRG', 76.40, -.65, .3, -.02, .4, 0),
              ('ABB', 'ABBank', 7.90, -1.25, 3.8, -.01, -.6, .2)],
}
PROP = {'VCB': 2.4, 'HPG': 5.8, 'CTG': -1.9, 'BID': 1.2, 'MSN': -.8, 'VIC': -3.6, 'NVL': 0, 'AGR': .4}   # tự doanh ròng (tỷ) của 8 mã
HOSE_CAP, VNINDEX = 7_000_000, 1300.0          # tổng vốn hoá HOSE (tỷ) và điểm VN-Index dùng để quy đổi điểm tác động

# Tên đầy đủ để gợi ý blue-chip
FULL = {'VCB': 'Ngân hàng TMCP Ngoại thương Việt Nam', 'CTG': 'Ngân hàng TMCP Công thương Việt Nam', 'BID': 'Ngân hàng TMCP Đầu tư và Phát triển Việt Nam', 'HPG': 'Tập đoàn Hòa Phát'}

# Chủ đề (nhóm ngành) trên HOSE
THEMES = [('Ngân hàng', ('VCB', 'CTG', 'BID', 'VPB', 'HDB', 'SSB', 'LPB', 'STB')), ('Bất động sản', ('VIC', 'VHM', 'NVL', 'VRE')),
          ('Chứng khoán', ('SSI', 'VIX', 'AGR')), ('Thép, vật liệu', ('HPG', 'GEX', 'DGC', 'GVR')), ('Tiêu dùng, bán lẻ', ('MSN', 'VNM', 'MWG')),
          ('Công nghệ, năng lượng', ('FPT', 'GAS'))]

DAYS = (('T', '29/10'), ('T-1', '28/10'), ('T-2', '27/10'), ('T-3', '26/10'), ('T-4', '23/10'), ('T-5', '22/10'))
SESS = ('23/10', '26/10', '27/10', '28/10', '29/10')


def times():
    """Mốc 5 phút: 09:00 đến 11:30 và 13:00 đến 14:45 (bỏ nghỉ trưa)."""
    out = [9 * 60 + 5 * i for i in range(31)] + [13 * 60 + 5 * i for i in range(22)]
    return [f'{m // 60:02d}:{m % 60:02d}' for m in out]


class Row:
    """Một mã trong bảng của sàn: giá, %, KL (triệu), điểm tác động, khối ngoại ròng, tự doanh ròng; go là id trang thông tin nếu có."""
    def __init__(s, code, name, price, pct, vol, impact, fnet, prop, go=None, lim=7):
        s.code, s.name, s.price, s.pct, s.vol, s.impact, s.fnet, s.prop, s.go = code, name, price, pct, vol, impact, fnet, prop, go
        s.lim = lim
        s.kind = 'ceil' if pct >= lim else 'floor' if pct <= -lim else 'up' if pct > 0 else 'down' if pct < 0 else 'ref'   # lim: biên độ của sàn (HOSE 7, HNX 10, UPCoM 15)
        s.chg = round(price - price / (1 + pct / 100), 2)


def universe(ex):
    rows = [Row(*o, lim=LIM[ex]) for o in OTHERS[ex]]
    if ex == 'hose':
        for st in STOCKS:
            imp = round(st.shares * st.last / 1e6 * st.pct / 100 / HOSE_CAP * VNINDEX, 2)
            rows.append(Row(st.code, st.name, st.last, round(st.pct, 2), st.vol / 1e6, imp, st.f_gnet, PROP[st.code], st.id, lim=LIM[ex]))
    return rows


def bin_of(pct):
    """Chỉ số khoảng % (theo BINS) của một mã."""
    if pct <= -7: return 0
    if pct <= -5: return 1
    if pct <= -3: return 2
    if pct <= -1: return 3
    if pct < 0: return 4
    if pct == 0: return 5
    return 6 if pct < 1 else 7 if pct < 3 else 8 if pct < 5 else 9 if pct < 7 else 10


def netflow(ex, day_index):
    """Dòng tiền chủ động lũy kế (tỷ) theo mốc 5 phút. Phiên hôm nay (T) chỉ đến 10:15."""
    r = random.Random(f'flow-{ex}-{day_index}')
    amp, t = EX[ex]['amp'], times()
    v, out = 0.0, []
    drift = r.uniform(-.25, .25) * amp / 10
    for i in range(len(t)):
        v += r.gauss(drift, amp / 9)
        v = max(-amp * 1.1, min(amp * 1.1, v))
        out.append(round(v, 1))
        if day_index == 0 and t[i] == '10:15': break
    return out


def net10(ex, today, key):
    r = random.Random(f'net10-{ex}-{key}')
    amp = {'hose': 260, 'hnx': 30, 'upcom': 22}[ex] * (.4 if key == 'prop' else 1)
    days = ('16/10', '19/10', '20/10', '21/10', '22/10', '23/10', '26/10', '27/10', '28/10', '29/10')
    return [(d, round(r.uniform(-amp, amp), 1)) for d in days[:-1]] + [(days[-1], round(today, 1))]
