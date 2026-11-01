## Dùng khi
Dựng một trang hoàn chỉnh từ các component, hiển thị tốt trên mobile (dưới 720px) và tablet.
## Class
| Class | Mô tả |
|---|---|
| `.arg-page` | Nền trang, chiều cao tối thiểu bằng khung nhìn |
| `__main` | Cột nội dung, tối đa 1040px, lề trái phải `--arg-gutter` (20px) |
| `__block` | Một khối (tiêu đề + nội dung) |
| `__cols` | Chia 2 cột từ 720px |
| `.arg-screen--plain` | Màn nền trắng liền khối, header cũng trắng mờ |
| `.arg-page__main--dense` | Khoảng cách giữa các phần 16px thay vì 32px |
| `.arg-page__main--fit` | Gọn lại để cả màn vừa một khung hình, không cuộn: khoảng cách giữa các phần 12px, trong cột và form 8px, đáy main chừa 12px |
| `.arg-split` | Hai cột 1:2,1 (sổ lệnh hẹp và trường nhập rộng), cột con xếp dọc 12px |
| `.arg-order` | Form đặt lệnh xếp dọc 12px |
| `[data-mode]` | Trên màn hình: `.arg-trade--pro` và `.arg-trade--lite` chỉ hiện đúng chế độ |
| `.arg-lite` | Form đặt lệnh nhanh, các nhóm trường cách nhau 12px |
| `.arg-stack` | Khối xếp dọc, khoảng cách 16px (bảng, biểu đồ, ghi chú trong một mục) |
| `.arg-note` | Dòng ghi chú nhỏ dưới biểu đồ hoặc bảng |
| `.arg-page__tabbed[data-arg-tabs]` | Chuyển cả nhóm khối bằng tab: khối đầu chứa dải tab, mỗi `tabpanel` chứa nhiều `.arg-page__block`. Trong `.arg-screen--sections` khối tab liền với khối đầu của tabpanel, các khối khác cách 10px |
| `.arg-screen--sections` | Trang nền trắng chia mục: mỗi `.arg-page__block` là khối trắng tràn mép, cách nhau 10px bằng màu nền xám của trang. Dùng cho trang chi tiết |

Trong màn đặt lệnh (`.arg-page__main--fit`), hai cột của `.arg-split` (sổ lệnh trái, form phải) cao bằng nhau và khối đầu, khối cuối thẳng hàng: cột ngắn hơn giãn khoảng cách giữa các khối.
