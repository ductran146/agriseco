## Dùng khi
Tin tức và bản tin thị trường.
## Class
| Class | Mô tả |
|---|---|
| `.arg-news-list` | Danh sách trong thẻ, ngăn cách bằng đường kẻ |
| `.arg-news-item` `--thumb` | Một tin; `--thumb` thêm ô ảnh 88×64 chứa `<img class="arg-news-item__img">` (cắt vừa khung, `object-fit: cover`, ảnh webp 264×192) |
| `--plain` (trên `.arg-news-list`) | Danh sách phẳng, không khung thẻ, dùng trong khối trắng |
| `--rank` `__rank` | Tin xếp hạng: số thứ tự lớn bên trái (mục Đọc nhiều nhất) |
| `__body` `__title` `__meta` | Nội dung, tiêu đề (2 dòng), ngày và nguồn |

Ảnh mẫu: `pages/news/news-1.webp` đến `news-10.webp`, ảnh stock miễn phí (nguồn Lorem Picsum, ảnh Unsplash, giấy phép Unsplash), **chưa gắn với nội dung từng bài**; dùng ảnh thật của Agriseco thì thay đúng tên file. Màn demo lấy ở `screens/assets/news/`, viewer nhúng thẳng base64.
