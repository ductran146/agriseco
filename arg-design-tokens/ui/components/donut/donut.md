## Dùng khi
Tỉ trọng của vài thành phần trong một tổng, ví dụ cơ cấu sở hữu hoặc cổ đông lớn. Tối đa khoảng 6 phần; phần nhỏ gộp vào "Khác".
## Class
| Class | Mô tả |
|---|---|
| `.arg-donut` | Khung: biểu đồ 168px trên, chú giải dưới; từ 600px xếp ngang |
| `__chart` | SVG `viewBox="0 0 42 42"`, vòng `r=15.915` `pathLength="100"`: `.bg` là nền, `.seg` là một phần (`--c` màu, `stroke-dasharray` = phần trăm) |
| `--side` | Biểu đồ 128px bên trái, chú giải bên phải (không xếp dọc), dùng khi cần gọn trên màn hẹp |
| `__center` | Chữ giữa vòng (số lớn và nhãn) |
| `__legend` `__key` `__name` `__pct` `__sub` | Chú giải: chấm màu `--c`, tên, phần trăm, dòng phụ (số cổ phiếu hoặc giá trị) |

Màu dùng `--arg-viz-1` đến `--arg-viz-6`.

## Hành vi (JS)
Rê chuột (máy tính) hoặc nhấn giữ khoảng 250ms rồi kéo (điện thoại) lên một cung: cung phóng to 7%, các cung khác mờ còn 40%, giữa vòng hiện thông số của cung (`data-main` dòng đậm, `data-name` dòng nhỏ). Rời chuột hoặc thả tay thì trả về như cũ; vuốt nhanh vẫn cuộn trang. Bắn `arg:donut` ({ name, main }).

## Cung
Mỗi cung là `path.seg` (hình quạt rỗng, góc bo 3,6px), khe giữa hai cung đều 2px (mép song song) khi vòng rộng 168px. Dựng bằng `pages/ring.py`.
