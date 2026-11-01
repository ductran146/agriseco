"""Dữ liệu mẫu cho các tab Tin tức, Sự kiện, Tài chính, Doanh nghiệp, Kỹ thuật của trang thông tin mã (không phải số thật).
Mọi số suy ra từ giá khớp và số cổ phiếu trong stocks.py để khớp nhau:
EPS 4 quý = giá / P/E; lợi nhuận 4 quý = EPS × số CP; vốn chủ = giá / P/B × số CP; ROE = lợi nhuận 4 quý / vốn chủ;
tăng trưởng so với cùng kỳ = kỳ này / cùng kỳ năm trước − 1; tỷ lệ sở hữu × số CP = số CP nắm giữ."""
import math, random
from datetime import date, timedelta

# Hồ sơ (mẫu). pe, pb: định giá; g: tăng trưởng lợi nhuận năm; lev: tổng tài sản / vốn chủ; m: lợi nhuận / doanh thu
PROFILES = {
    'VCB': dict(full='Ngân hàng TMCP Ngoại thương Việt Nam', bank=True, pe=15.0, pb=2.45, g=.10, lev=12.5, m=.42, listed='30/06/2009', ipo=60.0,
                desc='Vietcombank là ngân hàng thương mại do Nhà nước nắm cổ phần chi phối, thành lập năm 1963. Ngân hàng cung cấp dịch vụ huy động vốn, cho vay, thanh toán quốc tế, kinh doanh ngoại tệ, thẻ và ngân hàng số cho khách hàng cá nhân và doanh nghiệp. Vietcombank có thế mạnh về tài trợ thương mại, thanh toán quốc tế và nền khách hàng doanh nghiệp lớn, đồng thời đẩy mạnh bán lẻ trên kênh số.',
                own=[('Nhà nước', 74.8), ('Nhà đầu tư nước ngoài', 22.1), ('Tổ chức trong nước', 1.6), ('Cá nhân trong nước', 1.5)],
                major=[('Ngân hàng Nhà nước Việt Nam', 74.8), ('Cổ đông chiến lược nước ngoài', 15.0), ('Quỹ đầu tư nước ngoài', 4.2), ('Công đoàn ngân hàng', .3)]),
    'CTG': dict(full='Ngân hàng TMCP Công thương Việt Nam', bank=True, pe=8.4, pb=1.25, g=.14, lev=15.0, m=.38, listed='16/07/2009', ipo=40.0,
                desc='VietinBank là ngân hàng thương mại do Nhà nước nắm cổ phần chi phối, thành lập năm 1988. Ngân hàng phục vụ khách hàng doanh nghiệp lớn, doanh nghiệp vừa và nhỏ và cá nhân với các dịch vụ cho vay, huy động, thanh toán, thẻ và ngân hàng điện tử. VietinBank có mạng lưới rộng khắp cả nước và đặt mục tiêu tăng trưởng bán lẻ, dịch vụ phi tín dụng.',
                own=[('Nhà nước', 64.5), ('Nhà đầu tư nước ngoài', 27.2), ('Tổ chức trong nước', 4.1), ('Cá nhân trong nước', 4.2)],
                major=[('Ngân hàng Nhà nước Việt Nam', 64.5), ('Cổ đông chiến lược nước ngoài', 19.7), ('Quỹ đầu tư nước ngoài', 3.4), ('Công đoàn ngân hàng', 1.2)]),
    'BID': dict(full='Ngân hàng TMCP Đầu tư và Phát triển Việt Nam', bank=True, pe=11.2, pb=1.75, g=.12, lev=17.0, m=.33, listed='24/01/2014', ipo=18.5,
                desc='BIDV là ngân hàng thương mại do Nhà nước nắm cổ phần chi phối, có lịch sử từ năm 1957. Ngân hàng hoạt động trong lĩnh vực ngân hàng, bảo hiểm, chứng khoán và đầu tư tài chính, với quy mô tổng tài sản thuộc nhóm lớn nhất hệ thống. BIDV có thế mạnh về tài trợ dự án, khách hàng doanh nghiệp và đang mở rộng mảng bán lẻ.',
                own=[('Nhà nước', 80.9), ('Nhà đầu tư nước ngoài', 16.6), ('Tổ chức trong nước', 1.2), ('Cá nhân trong nước', 1.3)],
                major=[('Ngân hàng Nhà nước Việt Nam', 80.9), ('Cổ đông chiến lược nước ngoài', 15.0), ('Quỹ đầu tư nước ngoài', 1.1), ('Công đoàn ngân hàng', .2)]),
    'AGR': dict(full='Công ty Cổ phần Chứng khoán Agribank', bank=False, pe=21.0, pb=1.35, g=.18, lev=1.9, m=.30, listed='10/12/2009', ipo=12.0,
                desc='Agriseco là công ty chứng khoán thành viên của Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank), thành lập năm 2000. Công ty cung cấp dịch vụ môi giới, lưu ký, tư vấn tài chính doanh nghiệp, bảo lãnh phát hành và tự doanh chứng khoán. Agriseco tận dụng mạng lưới khách hàng của Agribank để phát triển mảng môi giới và dịch vụ tài chính.',
                own=[('Cổ đông lớn trong nước', 75.0), ('Nhà đầu tư nước ngoài', 1.8), ('Tổ chức trong nước', 6.2), ('Cá nhân trong nước', 17.0)],
                major=[('Agribank', 75.0), ('Quỹ đầu tư trong nước', 3.1), ('Quỹ đầu tư nước ngoài', 1.2)]),
    'HPG': dict(full='Công ty Cổ phần Tập đoàn Hòa Phát', bank=False, pe=13.5, pb=1.45, g=.20, lev=1.95, m=.09, listed='15/11/2007', ipo=96.0,
                desc='Hòa Phát là tập đoàn sản xuất công nghiệp hàng đầu Việt Nam, khởi đầu từ năm 1992. Lĩnh vực cốt lõi là sản xuất thép (thép xây dựng, thép cuộn cán nóng, ống thép, tôn mạ), bên cạnh nông nghiệp, bất động sản khu công nghiệp và điện máy gia dụng. Tập đoàn sở hữu các khu liên hợp gang thép quy mô lớn và chuỗi sản xuất khép kín.',
                own=[('Cổ đông sáng lập', 34.2), ('Nhà đầu tư nước ngoài', 22.0), ('Tổ chức trong nước', 14.3), ('Cá nhân trong nước', 29.5)],
                major=[('Chủ tịch HĐQT và người liên quan', 26.4), ('Thành viên HĐQT khác', 7.8), ('Quỹ đầu tư nước ngoài', 6.3), ('Quỹ đầu tư trong nước', 3.0)]),
    'VIC': dict(full='Tập đoàn Vingroup - Công ty Cổ phần', bank=False, pe=38.0, pb=1.6, g=.08, lev=4.2, m=.06, listed='19/09/2007', ipo=60.0,
                desc='Vingroup là tập đoàn kinh tế tư nhân đa ngành, hoạt động trong các lĩnh vực công nghệ và công nghiệp, thương mại dịch vụ và thiện nguyện xã hội. Các mảng chính gồm bất động sản, du lịch và nghỉ dưỡng, ô tô điện, giáo dục và y tế. Tập đoàn có hệ sinh thái sản phẩm rộng với nhiều thương hiệu quen thuộc.',
                own=[('Cổ đông sáng lập', 59.5), ('Nhà đầu tư nước ngoài', 12.9), ('Tổ chức trong nước', 10.6), ('Cá nhân trong nước', 17.0)],
                major=[('Chủ tịch HĐQT và người liên quan', 51.4), ('Công ty liên quan cổ đông lớn', 8.1), ('Quỹ đầu tư nước ngoài', 2.6)]),
    'MSN': dict(full='Công ty Cổ phần Tập đoàn Masan', bank=False, pe=55.0, pb=2.7, g=.25, lev=3.1, m=.03, listed='05/11/2009', ipo=75.0,
                desc='Masan là tập đoàn hoạt động trong lĩnh vực hàng tiêu dùng và bán lẻ, với các mảng thực phẩm và đồ uống, chuỗi bán lẻ, thịt có thương hiệu và tài nguyên khoáng sản. Tập đoàn theo đuổi mô hình tiêu dùng bán lẻ tích hợp, kết nối sản phẩm với mạng lưới cửa hàng phủ rộng.',
                own=[('Cổ đông sáng lập', 52.6), ('Nhà đầu tư nước ngoài', 28.3), ('Tổ chức trong nước', 7.4), ('Cá nhân trong nước', 11.7)],
                major=[('Công ty mẹ của cổ đông sáng lập', 31.2), ('Công ty liên quan cổ đông sáng lập', 21.4), ('Cổ đông chiến lược nước ngoài', 7.1)]),
    'NVL': dict(full='Công ty Cổ phần Tập đoàn Đầu tư Địa ốc No Va', bank=False, pe=32.0, pb=0.62, g=.30, lev=5.6, m=.05, listed='28/12/2016', ipo=55.0,
                desc='Novaland là doanh nghiệp phát triển bất động sản, tập trung vào nhà ở đô thị, khu đô thị và bất động sản du lịch nghỉ dưỡng. Công ty có quỹ đất tại nhiều tỉnh thành, đang tái cấu trúc nợ và đẩy nhanh hoàn thiện pháp lý, bàn giao các dự án trọng điểm.',
                own=[('Cổ đông sáng lập', 45.0), ('Nhà đầu tư nước ngoài', 8.2), ('Tổ chức trong nước', 16.3), ('Cá nhân trong nước', 30.5)],
                major=[('Công ty liên quan cổ đông sáng lập', 21.6), ('Chủ tịch HĐQT và người liên quan', 18.2), ('Quỹ đầu tư nước ngoài', 3.4)]),
}

TODAY = date(2026, 10, 29)
WEEK = (date(2026, 10, 26), date(2026, 11, 1))           # tuần hiện tại (thứ Hai đến Chủ nhật)
RANGE = (date(2026, 10, 1), date(2026, 11, 30))          # khoảng lọc sự kiện mặc định
SOURCES = ('Agriseco', 'Vietstock', 'CafeF', 'VnEconomy', 'Tin nhanh')


def d(x): return x.strftime('%d/%m/%Y')
def vnf(x, n=2): return f'{x:,.{n}f}'.replace(',', '#').replace('.', ',').replace('#', '.')
def pct(x): return vnf(x) + '%'
def dong(x): return f'{round(x):,}'.replace(',', '.')


def verdict(rows):
    """Kết luận tín hiệu từ danh sách chỉ báo [(tên, giá trị, 'buy'|'sell'|'neutral')]."""
    b = sum(1 for *_, x in rows if x == 'buy'); sl = sum(1 for *_, x in rows if x == 'sell'); ne = len(rows) - b - sl
    score = (b - sl) / len(rows)                                  # -1..1
    word = 'Mua mạnh' if score > .5 else 'Mua' if score > .1 else 'Bán mạnh' if score < -.5 else 'Bán' if score < -.1 else 'Trung lập'
    return dict(buy=b, sell=sl, neutral=ne, v=round((score + 1) / 2, 3), word=word, cls='arg-buy' if score > .1 else 'arg-sell' if score < -.1 else '')


class Company:
    def __init__(s, st):
        s.st, s.p = st, PROFILES[st.code]
        s.r = random.Random(st.seed * 7 + 3)
        s._fin()

    # ---------- Tài chính ----------
    def _fin(s):
        st, p, r = s.st, s.p, s.r
        n = 24                                                    # Q4/2020 .. Q3/2026
        s.qlabels = [f'Q{(i + 3) % 4 + 1}/{2020 + (i + 3) // 4}' for i in range(n)]
        s.eps_ttm = st.last * 1000 / p['pe']                      # đồng
        s.ni_ttm = s.eps_ttm * st.shares / 1e9                    # tỷ đồng
        season = [1.0, .92, 1.0, 1.12]                            # Q1..Q4
        raw = [(1 + p['g']) ** (i / 4) * season[(i + 3) % 4] * r.uniform(.9, 1.1) for i in range(n)]
        k = s.ni_ttm / sum(raw[-4:])
        s.ni = [x * k for x in raw]
        s.equity_now = st.last * 1000 / p['pb'] * st.shares / 1e9
        s.equity = [s.equity_now / (1 + p['g'] * .8) ** ((n - 1 - i) / 4) for i in range(n)]
        s.assets = [e * p['lev'] * r.uniform(.97, 1.03) for e in s.equity]
        s.liab = [a - e for a, e in zip(s.assets, s.equity)]
        s.rev = [x / (p['m'] * r.uniform(.92, 1.08)) for x in s.ni]
        s.opp = [x / .8 * r.uniform(.97, 1.03) for x in s.ni]   # lợi nhuận trước thuế
        ttm = lambda a, i: sum(a[i - 3:i + 1])
        s.roe = [ttm(s.ni, i) / s.equity[i] * 100 if i >= 3 else None for i in range(n)]
        s.roa = [ttm(s.ni, i) / s.assets[i] * 100 if i >= 3 else None for i in range(n)]
        s.eps = [ttm(s.ni, i) * 1e9 / st.shares if i >= 3 else None for i in range(n)]
        sc = s.ni_ttm / 4
        s.cfo = [sc * r.uniform(-1.5, 2.5) for _ in range(n)]
        s.cfi = [-sc * r.uniform(.2, 1.5) for _ in range(n)]
        s.cff = [sc * r.uniform(-1.2, 1.0) for _ in range(n)]
        s.rev_ttm = ttm(s.rev, n - 1)
        s.ratios = s._ratios(st.shares * st.last / 1e6)

    def _ratios(s, cap):
        st, p, r = s.st, s.p, s.r
        n = len(s.ni) - 1
        val = [('P/E (lần)', vnf(st.last * 1000 / s.eps_ttm)), ('P/B (lần)', vnf(cap / s.equity_now)), ('P/S (lần)', vnf(cap / s.rev_ttm)),
               ('EPS 4 quý (đ)', dong(s.eps_ttm)), ('Giá trị sổ sách / CP (đ)', dong(s.equity_now * 1e9 / st.shares))]
        if p['bank']:
            prof = [('ROE', pct(s.roe[n])), ('ROA', pct(s.roa[n])), ('Biên lãi thuần (NIM)', pct(r.uniform(2.6, 3.6))), ('Chi phí vốn (COF)', pct(r.uniform(2.8, 4.2)))]
            stren = [('Vốn chủ sở hữu / Tổng tài sản', pct(s.equity[n] / s.assets[n] * 100)), ('Cho vay / Huy động (LDR)', pct(r.uniform(82, 98))),
                     ('Tỷ lệ an toàn vốn (CAR)', pct(r.uniform(9.5, 12.5)))]
            eff = [('Chi phí / Thu nhập (CIR)', pct(r.uniform(28, 38))), ('Tăng trưởng lợi nhuận cùng kỳ', pct((s.ni[n] / s.ni[n - 4] - 1) * 100))]
            qual = [('Tỷ lệ nợ xấu (NPL)', pct(r.uniform(.9, 1.8))), ('Tỷ lệ bao phủ nợ xấu (LLR)', pct(r.uniform(110, 230)))]
            return [('Định giá', val), ('Khả năng sinh lời', prof), ('Sức mạnh tài chính', stren), ('Hiệu quả quản lý', eff), ('Chất lượng tài sản', qual)]
        prof = [('ROE', pct(s.roe[n])), ('ROA', pct(s.roa[n])), ('Biên lợi nhuận gộp', pct(p['m'] * 100 * r.uniform(1.8, 2.6))), ('Biên lợi nhuận ròng', pct(s.ni_ttm / s.rev_ttm * 100))]
        stren = [('Nợ phải trả / Vốn chủ sở hữu (lần)', vnf(s.liab[n] / s.equity[n])), ('Vốn chủ sở hữu / Tổng tài sản', pct(s.equity[n] / s.assets[n] * 100)),
                 ('Khả năng thanh toán hiện hành (lần)', vnf(r.uniform(1.0, 1.9)))]
        eff = [('Vòng quay tổng tài sản (lần)', vnf(s.rev_ttm / s.assets[n])), ('Tăng trưởng doanh thu cùng kỳ', pct((s.rev[n] / s.rev[n - 4] - 1) * 100)),
               ('Tăng trưởng lợi nhuận cùng kỳ', pct((s.ni[n] / s.ni[n - 4] - 1) * 100))]
        return [('Định giá', val), ('Khả năng sinh lời', prof), ('Sức mạnh tài chính', stren), ('Hiệu quả quản lý', eff)]

    def periods(s, mode):
        """5 kỳ gần nhất: quý (Q3/2025..Q3/2026) hoặc năm (2021..2025). Mỗi kỳ: (nhãn, chỉ số các quý, chỉ số các quý cùng kỳ năm trước)."""
        n = len(s.ni)
        if mode == 'q':
            return [(s.qlabels[i], [i], [i - 4]) for i in range(n - 5, n)]
        out = []
        for y in range(2021, 2026):
            idx = [i for i, l in enumerate(s.qlabels) if l.endswith(str(y))]
            prev = [i for i, l in enumerate(s.qlabels) if l.endswith(str(y - 1))]
            out.append((str(y), idx, prev))
        return out

    def series(s, key, mode):
        """(giá trị theo kỳ, tăng trưởng % so với cùng kỳ). Lợi nhuận, doanh thu, dòng tiền: cộng các quý của kỳ;
        tài sản, nợ, vốn: số cuối kỳ; ROE, ROA, EPS: 4 quý gần nhất tính tại cuối kỳ."""
        flow = {'ni': s.ni, 'rev': s.rev, 'opp': s.opp, 'cfo': s.cfo, 'cfi': s.cfi, 'cff': s.cff}
        stock = {'assets': s.assets, 'liab': s.liab, 'equity': s.equity}
        ratio = {'roe': s.roe, 'roa': s.roa, 'eps': s.eps}
        vals, yoy = [], []
        for _, idx, prev in s.periods(mode):
            if key in flow:
                v = sum(flow[key][i] for i in idx)
                pv = sum(flow[key][i] for i in prev) if prev and prev[0] >= 0 and len(prev) == len(idx) else None
            elif key in stock:
                v = stock[key][idx[-1]]; pv = stock[key][prev[-1]] if prev and prev[-1] >= 0 else None
            else:
                v = ratio[key][idx[-1]]; pv = ratio[key][prev[-1]] if prev and prev[-1] >= 3 else None
            vals.append(v)
            yoy.append((v / pv - 1) * 100 if pv and pv > 0 else None)
        return vals, yoy

    # ---------- Doanh nghiệp ----------
    def ownership(s):
        return [(n, p, round(s.st.shares * p / 100)) for n, p in s.p['own']]

    def major(s):
        rows = [(n, p, round(s.st.shares * p / 100)) for n, p in s.p['major']]
        return rows + [('Cổ đông khác', round(100 - sum(p for _, p, _ in rows), 1), s.st.shares - sum(x for *_, x in rows))]

    def insiders(s):
        r = random.Random(s.st.seed * 11)
        people = [('Trần Thị Mai', 'Phó Tổng giám đốc'), ('Lê Quốc Hùng', 'Thành viên HĐQT'), ('Phạm Minh Đức', 'Giám đốc tài chính')]
        days = (date(2026, 10, 15), date(2026, 10, 8), date(2026, 9, 25))
        return [(nm, role, d(dt), side, r.randint(5, 300) * 100) for (nm, role), dt, side in zip(people, days, ('buy', 'sell', 'buy'))]

    def listing(s):
        st, p = s.st, s.p
        first = int(round(st.shares * random.Random(st.seed * 19).uniform(.25, .55), -5))
        return [('Ngày giao dịch đầu tiên', p['listed']), ('Giá chào sàn (nghìn đồng)', vnf(p['ipo'])), ('KL niêm yết lần đầu (CP)', dong(first)),
                ('KL niêm yết hiện tại (CP)', dong(st.shares)), ('KL đang lưu hành (CP)', dong(st.shares)), ('Vốn hoá (tỷ đồng)', dong(st.cap))]

    # ---------- Sự kiện ----------
    def events(s):
        st, r = s.st, random.Random(s.st.seed * 13)
        div = r.choice((500, 800, 1000, 1200, 1500))
        e1 = date(2026, 10, 27) + timedelta(days=r.randint(0, 3))
        e2 = date(2026, 11, 12) + timedelta(days=r.randint(0, 6))
        ev = [
            ('dividend', e1, f'{st.code}: Trả cổ tức đợt 1 năm 2025 bằng tiền',
             [('Ngày giao dịch không hưởng quyền', d(e1)), ('Ngày đăng ký cuối cùng', d(e1 + timedelta(days=1))), ('Ngày thanh toán', d(e1 + timedelta(days=28))),
              ('Tỷ lệ thực hiện', f'{vnf(div / 100, 0)}% ({dong(div)} đ/CP)')]),
            ('report', date(2026, 10, 30), f'{st.code}: Công bố kết quả kinh doanh quý III/2026',
             [('Ngày công bố', '30/10/2026'), ('Kỳ báo cáo', 'Quý III/2026'), ('Loại báo cáo', 'Báo cáo tài chính hợp nhất')]),
            ('dividend', e2, f'{st.code}: Phát hành cổ phiếu trả cổ tức năm 2025',
             [('Ngày giao dịch không hưởng quyền', d(e2)), ('Ngày đăng ký cuối cùng', d(e2 + timedelta(days=1))), ('Tỷ lệ thực hiện', f'100:{r.choice((8, 10, 12, 15, 18))}'),
              ('Nguồn phát hành', 'Lợi nhuận sau thuế chưa phân phối')]),
            ('meeting', date(2026, 11, 25), f'{st.code}: Đại hội đồng cổ đông bất thường năm 2026',
             [('Ngày đăng ký cuối cùng', '04/11/2026'), ('Ngày họp', '25/11/2026'), ('Nội dung chính', 'Bầu bổ sung thành viên HĐQT')]),
            ('dividend', date(2026, 10, 6), f'{st.code}: Trả cổ tức còn lại năm 2024 bằng tiền',
             [('Ngày giao dịch không hưởng quyền', '06/10/2026'), ('Ngày đăng ký cuối cùng', '07/10/2026'), ('Ngày thanh toán', '24/10/2026'), ('Tỷ lệ thực hiện', '5% (500 đ/CP)')]),
        ]
        return sorted(ev, key=lambda e: e[1])

    # ---------- Tin tức ----------
    def news(s):
        st, nm = s.st, s.st.name
        t = [f'{nm} công bố kết quả kinh doanh quý III/2026', f'Cổ phiếu {st.code}: diễn biến phiên sáng 29/10', f'Khối ngoại giao dịch {st.code} sôi động trong tuần',
             f'{st.code} chốt quyền nhận cổ tức bằng tiền', f'Chuyên viên phân tích cập nhật khuyến nghị {st.code}', f'{nm} triệu tập đại hội cổ đông bất thường',
             'Dòng tiền quay lại nhóm vốn hoá lớn', f'{st.code} trong danh mục các quỹ ETF nội', f'Triển vọng ngành của {st.code} trong quý IV/2026', 'Điểm tin chứng khoán phiên 28/10',
             'Thị trường phiên sáng đi ngang, dòng tiền phân hoá', 'Lịch trả cổ tức tuần này', f'Cập nhật định giá {st.code} sau báo cáo quý', 'Nhóm vốn hoá lớn dẫn dắt chỉ số',
             f'Lãnh đạo {st.code} đăng ký giao dịch cổ phiếu']
        return [(title, d(TODAY - timedelta(days=i // 2)), SOURCES[i % len(SOURCES)]) for i, title in enumerate(t)]

    # ---------- Kỹ thuật ----------
    def technical(s):
        """(dao động, trung bình động): mỗi chỉ báo (tên, giá trị, tín hiệu) theo quy tắc phổ biến; trung bình động: giá trên MA là Mua."""
        st, r = s.st, random.Random(s.st.seed * 17)
        price, trend = st.last, {'up': 1, 'down': -1, 'ref': 0}[st.kind]
        osc = []
        def add(name, v, buy, sell):
            osc.append((name, vnf(v), 'buy' if buy(v) else 'sell' if sell(v) else 'neutral'))
        add('RSI (14)', r.uniform(35, 65) + trend * r.uniform(0, 12), lambda v: v < 30, lambda v: v > 70)
        add('Stochastic %K (14, 3, 3)', r.uniform(10, 90), lambda v: v < 20, lambda v: v > 80)
        add('CCI (20)', r.uniform(-160, 160), lambda v: v < -100, lambda v: v > 100)
        add('ADX (14)', r.uniform(12, 35), lambda v: False, lambda v: False)
        add('Awesome Oscillator', price * (r.uniform(-.02, .02) + trend * .006), lambda v: v > 0, lambda v: v < 0)
        add('Momentum (10)', price * (r.uniform(-.03, .03) + trend * .01), lambda v: v > 0, lambda v: v < 0)
        add('MACD (12, 26)', price * (r.uniform(-.01, .01) + trend * .004), lambda v: v > 0, lambda v: v < 0)
        add('Stochastic RSI', r.uniform(5, 95), lambda v: v < 20, lambda v: v > 80)
        add('Williams %R (14)', r.uniform(-95, -5), lambda v: v < -80, lambda v: v > -20)
        add('Bull Bear Power', price * (r.uniform(-.015, .015) + trend * .005), lambda v: v > 0, lambda v: v < 0)
        add('Ultimate Oscillator', r.uniform(25, 75), lambda v: v < 30, lambda v: v > 70)
        ma = []
        for kind in ('EMA', 'SMA'):
            for n in (10, 20, 30, 50, 100, 200):
                v = round(price * (1 + (r.uniform(-.015, .015) - trend * .004 * math.log(n)) * (1 + n / 100)), 2)
                ma.append((f'{kind} ({n})', vnf(v), 'buy' if price > v else 'sell' if price < v else 'neutral'))
        return osc, ma
