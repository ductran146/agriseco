"""Dữ liệu mẫu các mã cổ phiếu cho trang demo (không phải số thật). Giá theo nghìn đồng, khối lượng theo cổ phiếu.
Quy tắc HOSE: bước giá 0,01 (dưới 10), 0,05 (10 đến dưới 50), 0,10 (từ 50); biên độ ±7%; lô 100.
Mỗi mã khai báo tham chiếu, giá khớp, khối lượng; phần còn lại (trần, sàn, mở, cao, thấp, sổ lệnh, khớp lệnh, khối ngoại, nến)
được suy ra theo seed để luôn nhất quán. VCB khai báo đủ để khớp màn Giao dịch đã duyệt."""
import math, random

WHEN = '10:15 29/10'          # thời điểm dữ liệu: phiên liên tục, 10:15 ngày 29/10/2026
BUYING_POWER = 125_000_000    # sức mua mẫu của tiểu khoản


def r2(x): return round(x + 1e-9, 2)
def tick(p): return 0.01 if p < 10 else 0.05 if p < 50 else 0.10
def down(x, s): return r2(math.floor(x / s + 1e-6) * s)
def up(x, s): return r2(math.ceil(x / s - 1e-6) * s)
def lot(x): return int(round(x / 100)) * 100


class Stock:
    def __init__(s, code, name, ref, last, vol, shares, seed, hold=None, ex='HOSE', **kw):
        r = random.Random(seed)
        s.code, s.name, s.ex, s.seed, s.hold = code, name, ex, seed, hold
        s.id, s.uid = 'stock-' + code.lower(), 'stock-' + code.lower() + '-more'
        s.trade_id = kw.get('trade_id', 'trade-' + code.lower())
        s.ref, s.last, s.vol, s.shares = ref, last, vol, shares
        s.step = st = tick(ref)
        s.ceil, s.floor = down(ref * 1.07, st), up(ref * 0.93, st)
        clamp = lambda p: min(s.ceil, max(s.floor, r2(p)))
        s.open = kw.get('open') or clamp(ref + st * r.choice((-2, -1, 0, 1, 2)))
        s.high = kw.get('high') or clamp(max(s.open, last) + st * r.randint(1, 3))
        s.low = kw.get('low') or clamp(min(s.open, last) - st * r.randint(1, 3))
        s.avg = kw.get('avg') or r2((s.high + s.low + 2 * last) / 4)
        s.chg = r2(last - ref); s.pct = s.chg / ref * 100
        s.kind = 'up' if s.chg > 0 else 'down' if s.chg < 0 else 'ref'
        s.turnover = vol * s.avg / 1e6                       # tỷ đồng
        s.cap = round(shares * last / 1e6)                   # tỷ đồng
        s.hi52 = kw.get('hi52') or up(s.high * r.uniform(1.04, 1.25), st)
        s.lo52 = kw.get('lo52') or down(s.low * r.uniform(0.75, 0.94), st)
        # Sổ lệnh 3 mức tốt nhất: dư mua từ giá khớp xuống, dư bán từ trên giá khớp một bước
        s.bids = kw.get('bids') or [(r2(last - i * st), r.randint(40, 600) * 100) for i in range(3) if last - i * st >= s.floor - 1e-9]
        s.asks = kw.get('asks') or [(r2(last + (i + 1) * st), r.randint(40, 600) * 100) for i in range(3) if last + (i + 1) * st <= s.ceil + 1e-9]
        # Khối ngoại hôm nay
        fb, fs, fp = kw.get('foreign') or (lot(vol * r.uniform(.04, .18)), lot(vol * r.uniform(.04, .18)), s.avg)
        s.f_buy, s.f_sell, s.f_price = fb, fs, fp
        s.f_gb, s.f_gs = r2(fb * fp / 1e6), r2(fs * fp / 1e6)
        s.f_gnet = r2(s.f_gb - s.f_gs)
        today = round(s.f_gnet, 1)
        amp = max(1.0, s.turnover * 0.06)
        if 'net_today' in kw: s.net_today = kw['net_today']
        else:
            hrs = [round(r.uniform(-amp, amp) / 3, 1) for _ in range(4)]
            s.net_today = list(zip(('9h', '10h', '11h', '13h'), hrs)) + [('14h', round(today - sum(hrs), 1))]
        days = ('16/10', '19/10', '20/10', '21/10', '22/10', '23/10', '26/10', '27/10', '28/10', '29/10')
        s.net_10 = kw.get('net_10') or [(d, round(r.uniform(-amp, amp), 1)) for d in days[:-1]] + [(days[-1], today)]
        # Khớp lệnh gần nhất: B = bán chủ động (khớp giá dư mua tốt nhất), M = mua chủ động (khớp giá dư bán tốt nhất)
        if 'ticks' in kw: s.ticks = kw['ticks']
        else:
            t, s.ticks = 10 * 3600 + 14 * 60 + 58, []
            for i in range(10):
                side = 'B' if i == 0 or r.random() < .5 or not s.asks else 'M'
                p = last if side == 'B' else s.asks[0][0]
                s.ticks.append((f'{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}', side, p, r.choice((1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 100)) * 100))
                t -= r.randint(3, 9)

    def cls(s, p):
        """Lớp màu theo giá so với tham chiếu, trần, sàn."""
        if abs(p - s.ceil) < 1e-9: return 'arg-ceil'
        if abs(p - s.floor) < 1e-9: return 'arg-floor'
        return 'arg-up' if p > s.ref + 1e-9 else 'arg-down' if p < s.ref - 1e-9 else 'arg-ref'

    @property
    def max_qty(s):
        """Khối lượng mua tối đa theo sức mua, làm tròn xuống lô 100."""
        return int(BUYING_POWER / (s.last * 1000) // 100 * 100)


VCB = Stock('VCB', 'Vietcombank', 92.10, 91.80, 2_608_400, 5_589_091_262, 31, hold=(1000, 88.50), trade_id='trade',
            open=92.00, high=92.40, low=91.50, avg=91.95, hi52=97.60, lo52=78.30,
            bids=[(91.80, 36_100), (91.70, 52_800), (91.60, 27_500)], asks=[(91.90, 41_200), (92.00, 18_700), (92.10, 25_400)],
            foreign=(412_300, 268_900, 91.83),
            net_today=[('9h', 2.4), ('10h', 5.1), ('11h', -1.3), ('13h', 4.6), ('14h', 2.4)],
            net_10=[('16/10', -4.2), ('19/10', 7.8), ('20/10', 18.6), ('21/10', 5.1), ('22/10', -3.9), ('23/10', -5.6), ('26/10', 17.4), ('27/10', 15.9), ('28/10', -8.7), ('29/10', 13.2)],
            ticks=[('10:14:58', 'B', 91.80, 1200), ('10:14:51', 'M', 91.90, 500), ('10:14:47', 'B', 91.80, 3000), ('10:14:40', 'B', 91.80, 800), ('10:14:32', 'M', 91.90, 2100),
                   ('10:14:25', 'M', 91.90, 400), ('10:14:19', 'B', 91.80, 1500), ('10:14:10', 'M', 91.90, 700), ('10:14:02', 'B', 91.80, 10000), ('10:13:55', 'M', 91.90, 300)])

STOCKS = [
    Stock('AGR', 'Chứng khoán Agribank', 19.50, 19.75, 4_812_300, 216_000_000, 41, hold=(5000, 18.20)),
    Stock('HPG', 'Hoà Phát', 26.90, 27.10, 21_304_500, 6_396_250_000, 42, hold=(2000, 25.40)),
    Stock('VIC', 'Vingroup', 41.20, 41.20, 3_118_200, 3_823_660_000, 43),
    Stock('MSN', 'Masan', 69.20, 68.40, 2_604_800, 1_438_220_000, 44),
    Stock('NVL', 'Novaland', 14.60, 14.95, 9_716_400, 1_950_000_000, 45),
    VCB,
    Stock('CTG', 'VietinBank', 35.40, 35.20, 8_215_600, 5_369_990_000, 46),
    Stock('BID', 'BIDV', 39.90, 40.10, 3_402_100, 6_830_000_000, 47),
]
BY_CODE = {x.code: x for x in STOCKS}
