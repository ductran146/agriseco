# ARG Design Tokens (Agriseco)

Bộ token dựng lại từ export TradeX/Paave trong `../design-tokens/`, đổi tên sang **ARG** và chuyển Primary sang đỏ thương hiệu Agriseco.

## Cấu trúc

| File | Collection / mode | Nội dung |
|---|---|---|
| `ARG-Color.Mode 1.tokens.json` | ARG-Color | Primitive `p--*`: Brand, Grayscale, Gray.Raven, Primary (Agri_Red, Royal_Blue, Seagull), Alpha, Emotional, Market_Trading, Chart-color, Revenue |
| `Theme.ARG_Lightmode.tokens.json` | Theme / ARG_Lightmode | Semantic P1–P7 cho chế độ sáng |
| `Theme.ARG_Darkmode.tokens.json` | Theme / ARG_Darkmode | Semantic P1–P7 cho chế độ tối |
| `Spacing.Mode 1.tokens.json` | Spacing | Spacing 4px grid, breakpoints, radius, height-size |
| `Typography.Pretendard.tokens.json` | Typography | Font family, weight, size, line-height |
| `text.styles` / `effect.styles` / `color.styles` | Styles | Text style, shadow, gradient |
| `arg-tokens.css` | — | Toàn bộ token dạng CSS variable `--arg-*` |
| `manifest.json` | — | Manifest import Figma |

Các tầng semantic:

- **P1_Basic**: đen, trắng
- **P2_UI_Color**: text, nền, divider, state layer, bảng, label, skeleton
- **P3_Trading_Color**: tăng, giảm, tham chiếu, trần, sàn
- **P4_Action**: nút, tab, thông báo
- **P5–P7**: chart, effect, gradient

## Màu thương hiệu

| Token | Giá trị | Ghi chú |
|---|---|---|
| `p--Brand.Agri_Red` | `#A5000A` | Đỏ logo, bằng `p--Primary.Agri_Red.600-M` |
| `p--Brand.Orange` | `#FF8000` | Lấy từ logo |
| `p--Brand.Amber` | `#F5AF00` | Lấy từ logo |
| `p--Brand.Yellow` | `#FFD200` | Lấy từ logo |

Thang `p--Primary.Agri_Red`: 50 `#fff0f1` · 100 `#ffdbdd` · 200 `#ffb8bc` · 300 `#ff858c` · 400 `#ff4752` · 500 `#f5000f` · **600-M `#a5000a`** · 700 `#8a0008` · 800 `#700007` · 900 `#570005` · 950 `#380003`.

`p--Alpha.Primary.*` được tính lại trên nền `#A5000A`, giữ nguyên các bậc alpha. Royal_Blue và Seagull vẫn được giữ trong primitive để dùng cho info hoặc chart.

### Tương phản (WCAG 2.1)

| Cặp màu | Tỉ lệ | Cách dùng |
|---|---|---|
| Chữ trắng trên `600-M` | 8.06:1 | Nút chính ở cả hai chế độ |
| `600-M` trên nền trắng | 8.06:1 | Link và chữ nút phụ ở chế độ sáng |
| `400` trên Surface tối `#17181C` | 5.30:1 | Link, chữ nút phụ và nút outline ở chế độ tối |
| `600-M` trên Surface tối | 2.20:1 | Không đạt, nên **không** dùng làm màu chữ ở chế độ tối |

> **Lưu ý về màu Giảm:** đỏ thương hiệu (`#A5000A`) và đỏ Giảm (`#F73E3F`) cùng tông. Trên bảng giá, không dùng Primary làm màu chữ cho số liệu, và nên giữ nút Mua/Bán theo màu Trading (P3) thay vì Primary.

## Thay đổi so với bản gốc

**Đổi tên TradeX/Paave sang ARG**
- Mode `TradeX_Lightmode` / `TradeX_Darkmode` → `ARG_Lightmode` / `ARG_Darkmode`
- Collection `Paave-Color` → `ARG-Color`
- Manifest `Design Tokens` → `ARG Design Tokens`

**Primary**: mọi tham chiếu `p--Primary.Royal_Blue.600-M` → `p--Primary.Agri_Red.600-M`. Ở chế độ tối, ba token chữ trỏ sang `Agri_Red.400` để đủ tương phản:
- `Secondary_Button.Text_Button-Secondary`
- `Outline_Button.Text_Button-Outline`
- `Text_Button_Link.Text_Button`

**Sửa tên sai** (đổi ở cả tên token lẫn mọi chỗ tham chiếu):

| Cũ | Mới |
|---|---|
| `Background.Sureface` | `Background.Surface` |
| `Divider.Saperator`, `eff_Saperator`, `eff-Saperator` | `Separator`, `eff_Separator`, `eff-Separator` |
| `Font_Weight.Rugular` | `Font_Weight.Regular` |
| `height-largre` | `height-large` |
| `Text_Button-Main-Green` (thực chất không phải màu xanh lá) | `Text_Button-Outline` |
| `Line_Height.Body` | `Line_Height.Body_1` |
| `p--\bRevenue` (có ký tự điều khiển ẩn) | `p--Revenue` |

**Sửa tham chiếu gãy**
- `text.styles`: `{Font.Font_Size.Display 1}` → `{Font.Font_Size.Display_1}`, tương tự cho mọi size và line-height.
- `color.styles`: `{P3_Trading Color.*}` → `{P3_Trading_Color.*}` và `{P7_Gradient.Empty Color}` → `{P7_Gradient.Empty_Color}`.

## Dùng trong CSS

```html
<link rel="stylesheet" href="arg-tokens.css">
<html data-theme="dark">  <!-- bỏ attribute hoặc dùng "light" cho chế độ sáng -->
```

```css
.btn-primary {
  background: var(--arg-action-primary-button-button-main);
  color: var(--arg-action-primary-button-text-button-main);
  border-radius: var(--arg-border-radius-radius-md);
  height: var(--arg-border-height-size-height-normal);
  box-shadow: var(--arg-shadow-base);
}
```

Text style dùng class `.arg-text-<style>-<weight>`, ví dụ `.arg-text-body-4-regular` hoặc `.arg-text-title-1-bold`.

## Build lại

Sửa nguồn trong `../design-tokens/` hoặc sửa `build_arg.py`, rồi chạy:

```bash
python3 arg-design-tokens/build_arg.py design-tokens arg-design-tokens
```

Script kiểm mọi tham chiếu `{...}` ở cả hai mode. Nếu còn tham chiếu không resolve được, script dừng với mã lỗi 1.

## Còn để ngỏ

- `Font_Size.Label_2` và `Label_3` cùng là 11px, chỉ khác line-height (16 / 14). Có thể `Label_2` đúng ra là 12px.
- `P5_Chart.*` đều là `#ffffff`, có vẻ là placeholder.
- Tên nhóm trong P3 chưa nhất quán: `Down-Light.Increase` dùng cho màu giảm, `Ceiling-Purple.Flat` dùng cho màu trần. Bản này giữ nguyên để giới hạn phạm vi thay đổi.
