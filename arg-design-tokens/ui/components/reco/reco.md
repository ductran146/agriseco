## Dùng khi
Hiển thị khuyến nghị bán, giữ, mua của chuyên viên phân tích cho từng mã, kèm lãi/lỗ và giá mục tiêu.
## Class
| Class | Mô tả |
|---|---|
| `.arg-reco-row` | Dải thẻ cuộn ngang, lề tràn mép theo `--arg-gutter` |
| `.arg-reco` | Thẻ nền trắng, bo `--arg-radius`, đổ bóng `soft-shadow` |
| `__head` | Tiêu đề thẻ kèm mũi tên, cao 40px |
| `__cols` | Hàng tiêu đề cột, nền xám nhạt |
| `__sort` | Nút sắp xếp theo Lãi/lỗ (`aria-sort`: `none`, `ascending`, `descending`) |
| `__body` > `__item` | Một dòng, có `data-pl` là số Lãi/lỗ để sắp xếp; `__sym` là nhãn và mã, `__pl` là Lãi/lỗ |
| `.arg-rating` | Nhãn B, G, M ở đầu dòng (xem Rating) |
| `__item--link` | Dòng bấm được: `__sym` là thẻ `a` (ví dụ `data-arg-go` mở trang thông tin mã), vùng bấm phủ cả dòng, nền đổi khi rê chuột |

Màu Lãi/lỗ trong dòng theo nhãn của dòng đó (tăng, giảm, tham chiếu), lấy từ token giao dịch.
## JS
`reco.js`: bấm `__sort` đổi chiều và sắp xếp lại dòng. Bắn `arg:sort`.
