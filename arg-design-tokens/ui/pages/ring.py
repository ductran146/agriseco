"""Cung donut kiểu khối bo góc: vòng dày 6 (đơn vị viewBox 42, bán kính giữa 15,915), mỗi cung là một hình quạt rỗng, bốn góc bo RC,
hai cung cách nhau khe GAP. Bo góc bằng cách thu hình quạt vào RC rồi tô thêm viền cùng màu dày 2×RC, nối góc tròn (stroke-linejoin round)."""
import math

CX = CY = 21
RM, TH = 15.915, 6.0
RC, GAP = 0.9, 0.5  # khe 0,5 đơn vị = 2px khi vòng rộng 168px


def seg(color, start, p, name='', main=''):
    """color: giá trị --c; start, p: vị trí đầu và độ dài cung theo phần trăm vòng (bắt đầu từ 12 giờ, chiều kim đồng hồ do CSS xoay -90°).
    name, main: chữ hiện giữa vòng khi rê chuột hoặc nhấn giữ cung (data-name, data-main)."""
    extra = f' data-name="{name}" data-main="{main}"' if name else ''
    if p >= 99.9:
        return f'<circle class="seg" style="--c:{color}" cx="{CX}" cy="{CY}" r="{RM}"{extra}/>'
    ro, ri = RM + TH / 2 - RC, RM - TH / 2 + RC
    h = GAP / 2 + RC  # mép cung là đường song song với đường bán kính, cách nó h: khe giữa hai cung luôn đều
    a0 = start / 100 * 2 * math.pi
    a1 = (start + p) / 100 * 2 * math.pi
    def pt(r, a, side):
        hh = h * side
        d = math.sqrt(r * r - hh * hh); ang = a + math.atan2(hh, d)
        return CX + d * math.cos(a) - hh * math.sin(a), CY + d * math.sin(a) + hh * math.cos(a), ang
    xo0, yo0, b0 = pt(ro, a0, 1); xo1, yo1, b1 = pt(ro, a1, -1); xi0, yi0, _ = pt(ri, a0, 1); xi1, yi1, _ = pt(ri, a1, -1)
    big = 1 if (b1 - b0) > math.pi else 0
    d = (f'M{xo0:.2f} {yo0:.2f} A{ro:.2f} {ro:.2f} 0 {big} 1 {xo1:.2f} {yo1:.2f} L{xi1:.2f} {yi1:.2f} '
         f'A{ri:.2f} {ri:.2f} 0 {big} 0 {xi0:.2f} {yi0:.2f}Z')
    return f'<path class="seg" style="--c:{color}" d="{d}"{extra}/>'
