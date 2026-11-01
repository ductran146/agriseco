"""Sparkline SVG dùng chung cho Trang chủ và màn Thị trường (một nơi sinh, cùng thuật toán)."""
import math, random


def spark(kind, seed, n=18, flat=False):
    """kind: up, down, ref, flat, ceil, floor. ceil và floor là up và down với độ dốc mạnh hơn.
    flat=True: mã đứng giá (ref) vẽ phẳng đúng đường tham chiếu, như bảng giá."""
    r = random.Random(seed); y = 16; pts = []
    drift = {'up': -0.5, 'down': 0.5, 'ceil': -1.2, 'floor': 1.2}.get(kind, 0)
    for _ in range(n):
        y += r.uniform(-4, 4) + drift; y = max(4, min(28, y)); pts.append(y)
    if kind == 'flat': pts = [16 + math.sin(i / 2.2) * 3 + r.uniform(-1, 1) for i in range(n)]
    if kind == 'ref' and flat: pts = [16.0] * n
    line = ' '.join(f'{i * 80 / (n - 1):.1f},{p:.1f}' for i, p in enumerate(pts))
    return f'<svg class="arg-spark arg-spark--{kind}" viewBox="0 0 80 32" preserveAspectRatio="none" aria-hidden="true"><polygon points="0,32 {line} 80,32"/><polyline points="{line}"/><line class="ref" x1="0" y1="16" x2="80" y2="16"/></svg>'
