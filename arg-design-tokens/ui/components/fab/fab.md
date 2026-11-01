## Dùng khi
Một thao tác phụ của cả màn hình, cần luôn thấy khi cuộn (ví dụ đổi cách xem bảng giá). Không dùng cho thao tác chính của trang.
## Class
| Class | Mô tả |
|---|---|
| `.arg-fab-wrap` | Vùng dính, không chiếm chỗ, nằm trên thanh tab dưới, nút căn phải |
| `.arg-fab` | Nút tròn 56px nền trắng đổ bóng, icon 28px |
| `__on` `__off` | Hai icon cho trạng thái chưa bật và đã bật (`aria-pressed="true"` hiện `__off`) |
## Hành vi (JS)
`data-arg-fab` cùng `data-arg-target` (selector) và `data-arg-class`: bấm thì bật tắt class trên các phần tử đó trong vùng `[data-arg-listbar-scope]` gần nhất.
## Phụ thuộc
Icon.
