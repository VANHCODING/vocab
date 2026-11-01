# LexiUp - Từ vựng B1-B2 và C1 chọn lọc

Ứng dụng luyện từ vựng tiếng Anh cho người Việt, chạy bằng một tệp `index.html`. Giữ phương pháp lặp lại ngắt quãng (Leitner/SRS), bổ sung hướng dẫn học, bộ nội dung đã biên tập và phản hồi âm thanh rõ ràng.

## Nội dung hiện tại

| Cấp độ | Mục từ/cụm trong thư viện | Trạng thái biên tập |
| --- | ---: | ---: |
| B1 | 951 | 951 mục đã qua rà soát song ngữ |
| B2 | 1.546 | 1.546 mục đã qua rà soát song ngữ |
| C1 chọn lọc | 185 | 185 mục đã qua rà soát song ngữ |
| Tổng | 2.682 | 2.682 mục trong thư viện hiện hành |

- Đã bổ sung 320 mục học mới (160 B1 và 160 B2): 160 cụm từ thông dụng và 160 từ đơn/từ ghép hay gặp. Mỗi mục bổ sung có hai ví dụ song ngữ độc lập và ghi chú cách dùng.
- Rà soát từng mục trong toàn bộ thư viện đang học qua các nguồn biên tập (`content-corrections.tsv`, `content-repairs.tsv`, `content-glosses.tsv` và `content-semantic-review.json` với 1.416 bản ghi mới). Không còn mục từ điển nào ở trạng thái chờ duyệt trong thư viện phát hành.
- So với bản gốc: sửa 1.803 nghĩa tiếng Việt, 311 định nghĩa tiếng Anh, 1.381 câu ví dụ chính, 1.482 bản dịch ví dụ và 1.185 cụm kết hợp (collocation).
- Đã **xóa hẳn 1.117 mục C1 ít gặp khỏi dữ liệu nhúng của web**, chỉ giữ lại 185 từ/khái niệm C1 có tính ứng dụng học thuật và công việc cao. Tệp `removed-c1.json` chỉ lưu tên/ID để phục vụ việc nhận diện lại tiến độ cũ khi nhập bản sao lưu, không làm nặng ứng dụng chạy thực tế.
- Bản sao lưu ban đầu trước khi sửa đổi được lưu tại `backups/index.before-education-2026-11-01.html` để có thể đối chiếu hoặc phục hồi khi cần.

Giới hạn phương pháp: Nhãn B1/B2/C1 trong ứng dụng là mức xếp lộ trình dạy học được biên tập, không phải chứng nhận CEFR độc lập cho từng từ riêng rẽ. 185 từ C1 là lựa chọn có chọn lọc theo mục tiêu sử dụng, không phải bảng tần suất từ ngữ liệu toàn cầu. Đây là ứng dụng học từ vựng và cụm từ theo ngữ cảnh, không thay thế cho giáo trình toàn diện cả bốn kỹ năng nghe - nói - đọc - viết.

## Sử dụng

Mở `index.html` trên trình duyệt. Chọn cấp độ muốn học ở trang chủ, ôn từ đến hạn trước, sau đó học một nhóm từ cùng chủ đề. Không bắt buộc làm bài tự kiểm tra từ vựng.

- Sáu dạng bài được chọn theo điều kiện nội dung; không ép bài nghe khi thiếu hỗ trợ hoặc bài điền từ không có chỗ trống hợp lệ.
- Phản hồi chờ người học bấm **Tiếp tục**, không tự chuyển mất câu.
- Tìm tiếng Anh hoặc tiếng Việt không dấu trên cả ba cấp; tải thêm khi có hơn 60 kết quả.
- Thêm từ của bạn, kèm ví dụ và bản dịch; từ trùng được kiểm tra trước khi lưu.
- Xuất/nhập JSON trong **Cài đặt & Sao lưu** để giữ tiến độ và chuyển thiết bị. localStorage gắn với từng trình duyệt/địa chỉ trang, không tự đồng bộ giữa máy.
- Lỗi lưu tiến độ hiện cảnh báo không tự biến mất. Khôi phục sao lưu chỉ thay trạng thái đang học sau khi ghi đủ các phần; lỗi ghi sẽ thử hoàn tác dữ liệu đã ghi. ID C1 cũ được giữ nhưng không tính vào thống kê từ đang học.

## Âm thanh và ngoại tuyến

Ưu tiên giọng tiếng Anh do trình duyệt cung cấp, có lựa chọn UK/US và tốc độ 0,8x/1x. Có thông báo lỗi, nghe thử và đổi bài nghe sang bài chữ nếu không nghe được. Tắt tự động đọc vẫn dùng được nút Nghe thủ công.

Thư viện và bài tập chữ không cần tải dữ liệu bên ngoài. Phát âm ngoại tuyến phụ thuộc giọng tiếng Anh đã cài và khả năng của trình duyệt. Giọng trình duyệt có thể dùng dịch vụ mạng; nguồn dự phòng trực tuyến gửi từ/câu cần đọc đến Youdao hoặc Google. Không đảm bảo phát được khi thiết bị tắt tiếng, trình duyệt chặn tự phát hoặc dịch vụ ngoài gián đoạn. Phông chữ mạng cũng có thể không tải khi ngoại tuyến; có phông dự phòng.

## Phát triển và kiểm tra

Không cần cài gói npm để chạy app hoặc các kiểm tra mới:

```powershell
node build-curriculum.js
node --test test_education.js
```

Nguồn nội dung: `content-corrections.tsv`, `content-repairs.tsv`, `content-glosses.tsv`, `content-semantic-review.json`, `content-expansion.tsv`, `content-additions.tsv`. Chính sách giữ C1: `curriculum-policy.json`. Dùng `build-curriculum.js` để áp dụng chỉnh sửa; các generator và dữ liệu trung gian cũ đã được dọn khỏi dự án.

`content-audit.json` chứa thống kê và danh sách ngữ nghĩa còn chờ duyệt; `content-review-ledger.json` ghi trạng thái từng mục gốc và mục bổ sung. Phân tích chi tiết: `EDUCATION_AUDIT.md`. Builder giữ ID theo mục từ, kiểm tra trùng, ghi HTML qua tệp tạm và chạy lại không thay kết quả.

48 kiểm thử dùng Node VM và DOM/âm thanh giả lập; chưa thay thế việc kiểm tra hình ảnh và nghe trên thiết bị thật. Đợt kiểm tra lại bổ sung hồi quy cho phiên kế tiếp đúng cấp độ, bàn phím Enter/Space, phím giữ lặp, ngày học sau khôi phục sao lưu, chuỗi học sau đặt lại, callback sau khi thoát và trình duyệt không hỗ trợ canvas. Không coi kết quả kiểm thử là bảo đảm web không còn bất kỳ lỗi nào.

Có bản HTML trước thay đổi tại `backups/index.before-education-2026-11-01.html`. Không chép đè tệp đang dùng nếu chưa sao lưu tiến độ.

## Đưa lên hosting

Chỉ cần phục vụ tệp `index.html` từ hosting tĩnh của bạn. Không cần tải lên dữ liệu nguồn, script, báo cáo hoặc thư mục `backups/`. Đợt cập nhật này chỉ sửa tệp cục bộ, không tự đăng công khai hay thay đổi hosting.
