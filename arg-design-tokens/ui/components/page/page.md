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
## Tablet (từ 720px)
Mục tiêu: các mục nằm cạnh nhau cân đối, không để khoảng trống thừa.
| Quy tắc | Mô tả |
|---|---|
| `.arg-page__cols--match` | Hai cột cùng chiều cao: khối thấp hơn giãn thẻ bên trong (lưới dịch vụ trang chủ chia đều theo chiều cao), tiêu đề hai cột cùng cao 44px nên thẳng hàng. Danh sách (`.arg-navlist`) vẫn dồn lên đầu |
| tabpanel có từ 2 khối trở lên (màn kiểu mục nền trắng) | Chảy thành hai cột cân bằng chiều cao (CSS columns); khối cần cả bề ngang thêm `.arg-page__block--full`; nhóm tab lồng (`.arg-page__tabbed`) tự chiếm cả hai cột, khối bên trong tự chia cột |
| `.arg-page__main--fit` (Giao dịch, Sửa lệnh) | Hai cột (CSS columns, các lớp bọc form, split, panel bỏ hộp bằng `display: contents`): cột trái là mã, giá, thông tin và sổ lệnh mua bán (Pro); cột phải là form đặt lệnh và nút Mua, Bán (`break-before: column`). Chế độ Lite không có sổ lệnh nên cột trái thêm `.arg-trade__info` (ô trần, tham chiếu, sàn, trung bình, GTGD, vốn hoá, đỉnh đáy 52 tuần, khối ngoại mua ròng; chỉ hiện ở tablet khi Lite) |
| Danh sách | Sổ lệnh và lịch sử lệnh (`.arg-orderrow-list`), xếp hạng top cổ phiếu (`.arg-quote--rank`, kèm hàng tiêu đề thứ hai `.arg-quote-heads`), chủ đề (`.arg-theme-list`), nắm giữ (`.arg-holding-list`) chia hai cột; bảng giá và yêu thích giãn cột xu hướng; `.arg-kv--lines` ở màn chi tiết chia hai cột |
| `.arg-page__flow` | Nhóm các khối xếp một cột (mobile) rồi hai cột cân bằng chiều cao (tablet), khối không bị ngắt: màn Thêm |
| `.arg-statrow` ở màn đặt lệnh | Tablet: mỗi chỉ số một dòng (nhãn trái, giá trị phải) trong cột trái |
| `.arg-page__tabbed--side` | Tablet: dải tab lớn thành cột danh mục dọc (component Side panel, 240px dùng chung với Sổ lệnh) bên trái (dính khi cuộn), mục đang chọn màu như Chip tabs đang chọn; nội dung của mục nằm bên phải, các khối và danh sách trong đó về một cột, bảng giá bớt cột phụ cho vừa. Khối cuối của cột phải kéo dài phủ hết chiều cao (nền trắng, không lộ nền xám khi nội dung ngắn). Dùng ở màn Thị trường; mobile vẫn là dải tab ngang |
| `.arg-page__main--split` (Thông tin mã) | Tablet: hai cột. Trái `.arg-split-info` (mã, giá, vị thế, 12 chỉ số xếp 2 cột) dính khi cuộn, cao từ thanh đầu đến đáy màn, nền trắng; thanh Mua, Bán chỉ nằm trong cột phải; phải là dải tab và nội dung tab xếp một cột |
