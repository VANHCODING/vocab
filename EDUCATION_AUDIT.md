# LexiUp: rà soát nội dung và lỗi ứng dụng

Ngày cập nhật: 01/11/2026. Chỉ sửa mã nguồn cục bộ, không triển khai lên hosting.

## Kết quả và giới hạn

Đã quét cấu trúc đủ 3.479 mục gốc trong dữ liệu gốc và thực hiện rà soát từng mục đối với toàn bộ 2.682 mục trong thư viện hiện hành.

| Lộ trình | Thư viện phát hành | Trạng thái biên tập song ngữ |
| --- | ---: | ---: |
| B1 | 951 | 951 (hoàn tất rà soát ngữ nghĩa) |
| B2 | 1.546 | 1.546 (hoàn tất rà soát ngữ nghĩa) |
| C1 chọn lọc | 185 | 185 (hoàn tất rà soát ngữ nghĩa) |
| Tổng | 2.682 | 2.682 (toàn bộ thư viện đủ điều kiện học) |

- Bổ sung 320 mục: 160 cụm từ và 160 từ/từ ghép thông dụng (chia đều 160 B1 và 160 B2). Mỗi mục có 2 ví dụ song ngữ và ghi chú cách dùng.
- Xóa hẳn 1.117 từ C1 ít gặp khỏi dữ liệu chạy của web.
- So với bản gốc: sửa 1.803 nghĩa tiếng Việt, 311 định nghĩa tiếng Anh, 1.381 câu ví dụ chính, 1.482 bản dịch ví dụ và 1.185 cụm kết hợp (collocation).
- Nguồn dữ liệu gồm: `content-corrections.tsv` (140 mục), `content-repairs.tsv` (829 mục), `content-glosses.tsv` (512 mục), `content-semantic-review.json` (1.416 mục), `content-expansion.tsv` (160 cụm) và `content-additions.tsv` (160 từ).

Giới hạn cần nêu rõ:
1. Việc rà soát và biên tập nội dung được thực hiện bởi quy trình biên tập nội bộ, không thay thế chứng nhận ngôn ngữ độc lập của các tổ chức khảo thí quốc tế.
2. Nhãn cấp độ B1, B2 và bộ 185 từ C1 là định hướng giảng dạy theo mức độ hữu dụng và quen thuộc, không phải xếp hạng tuyệt đối từ một ngữ liệu thống kê duy nhất.
3. Chưa thực hiện kiểm thử hình ảnh trực quan trên mọi trình duyệt/điện thoại thật và chưa nghe thử âm thanh phát âm thực tế trên từng dòng máy.

Ví dụ những lỗi thực tế đã sửa:

| Mục | Lỗi cũ | Cách sửa |
| --- | --- | --- |
| reveal | Nghĩa Việt thành tái chế | Tiết lộ, làm lộ ra; ví dụ khảo sát tiết lộ nhu cầu luyện nói |
| resist | Nghĩa Việt thành phục hồi | Chống lại, cưỡng lại; ví dụ cưỡng lại sự cám dỗ |
| attempt | Nghĩa Việt thành thuộc kiểm toán | Nỗ lực, lần thử; ví dụ lần đầu thử nướng bánh |
| enemy | Nghĩa Việt thành thì giờ, ma vương | Kẻ thù; câu có ngữ cảnh truyện rõ ràng |
| key | Động từ nhưng định nghĩa và nghĩa là chìa khóa | Nhập thông tin bằng bàn phím; sửa cả định nghĩa |
| centre / experiment | Từ loại động từ, định nghĩa lại là danh từ | Thống nhất định nghĩa, nghĩa Việt và hành động trong ví dụ |
| tear | Lẫn nghĩa vết rách và giọt nước mắt | Chọn nghĩa giọt nước mắt, sửa định nghĩa và IPA tương ứng |
| subject | IPA nhấn âm danh từ trong mục tính từ | IPA tính từ và cấu trúc subject to |
| seriously | Câu mẫu khuyên thường xuyên bị bệnh nặng | Câu tự nhiên với take instructions seriously |
| violate | Câu mẫu khuyên thường xuyên vi phạm luật | Câu giải thích hành vi có thể xâm phạm quyền riêng tư |

Các câu We observed / They decided to / It is an honor và chuỗi It is important to ... regularly đã được thay trong dữ liệu đang dùng. Không còn câu mẫu có lựa chọn bằng dấu gạch chéo hoặc ngoặc vuông thừa trong các mục đã biên tập. Kiểm tra tự động không tìm thấy câu tiếng Anh trùng nguyên văn trong tập ví dụ hiện tại; điều đó **không** chứng minh mọi câu đã đa dạng hoặc hay về mặt sư phạm.

## C1 được loại thật khỏi dữ liệu chạy web

1.117 mục C1 ngoài danh sách giữ đã được xóa khỏi `RAW_VOCAB` trong `index.html`, không chỉ bị ẩn bằng bộ lọc. Tệp chứa nguyên nội dung C1 `vocabulary-c1-archive.json` đã được xóa.

`removed-c1.json` chỉ ghi tên, ID và lý do loại, không giữ nghĩa/định nghĩa/ví dụ. `curriculum-policy.json` cố định danh sách 185 mục được giữ để chạy lại builder không tự đưa C1 đã loại trở lại.

ID các từ còn học không đổi khi mảng bị rút gọn. ID tiến độ cũ vẫn có thể đọc từ sao lưu; các từ đã loại không được thêm lại vào thư viện và không làm tăng thống kê hộp nhớ. Bản HTML lịch sử trong `backups/` và các nguồn dữ liệu cũ không được app nạp vẫn được giữ để phục hồi, không nên tải lên hosting.

## Lỗi kỹ thuật sửa trong đợt này

1. **Xung đột ID:** check in và check-in, check out và check-out từng có thể bị chuẩn hóa về cùng ID, ghi đè từ loại và dữ liệu. Đã tách ID bổ sung, giữ ID cụm cũ, kiểm tra duy nhất trước khi ghi HTML và kiểm thử nạp lại tiến độ.
2. **Mất tiến độ của ID bổ sung:** bộ chuẩn hóa tiến độ nhận thêm tiền tố supp, không loại ID từ mới khi tải hoặc khôi phục.
3. **Lỗi lưu không thông báo:** lỗi localStorage hiện cảnh báo cố định, hướng dẫn tải sao lưu trước khi đóng trang. Khi lưu thành công lại, cảnh báo được xóa.
4. **Khôi phục dở dang:** chỉ thay trạng thái trong bộ nhớ sau khi ghi đủ người dùng, tiến độ, lịch sử và từ tự thêm; khi ghi lỗi sẽ thử hoàn tác các khóa đã ghi. Không tuyên bố localStorage có giao dịch nguyên tử khi trình duyệt bị đóng đột ngột.
5. **Thống kê C1 đã xóa:** số hộp nhớ chỉ tính mục có trong thư viện hiện hành, đồng nhất với tổng đã học/đã thuộc.
6. **Hiệu năng đáp án nhiễu:** thay việc chuẩn hóa và sắp xếp toàn bộ thư viện mỗi câu bằng nhóm ưu tiên và dừng khi đủ đáp án hợp lệ. Kiểm tra toàn bộ mục đã biên tập trước đó chạm timeout 10 giây; sau sửa hoàn tất dưới khoảng một giây trên môi trường kiểm thử này. Không coi đó là benchmark trình duyệt.
7. **Điền từ và tô sáng:** nhận thêm phụ âm gấp đôi, dạng bất quy tắc và biến thể cụm như are committed to / took care of. Không dùng khớp tiền tố rộng; mọi ví dụ chính đã biên tập hiện có đoạn mục tiêu khớp được.
8. **Tính tái lập:** builder kiểm tra dữ liệu, nghĩa còn thiếu, ID trùng, từ trùng; ghi HTML qua tệp tạm; chạy lại không làm thay đổi kết quả hoặc hồi sinh C1 đã loại.

Các sửa của đợt trước vẫn giữ: thoát phiên có xác nhận; phản hồi không tự chuyển câu; sửa SRS khi trả lời sai rồi làm lại; tách ôn tự do khỏi tăng hộp nhớ; tìm không dấu xuyên cấp; tải thêm kết quả; kiểm tra sao lưu/từ tự thêm; thoát HTML; focus modal; hỗ trợ giảm chuyển động.

## Âm thanh và giao diện

Giữ giao diện teal, phân cấp hiện tại và hướng dẫn chọn cấp độ/nội dung đã biên tập. Thêm giải thích rõ mức xếp lộ trình và cảnh báo lưu thất bại. Kiểm tra mã không phát hiện ID tĩnh bị trùng hoặc hook ID tĩnh bị thiếu trong phần được kiểm tra.

Âm thanh giữ cơ chế giọng trình duyệt trước, dự phòng mạng sau, timeout và hủy yêu cầu cũ, UK/US, tốc độ, nghe thử và đổi bài nghe sang bài chữ. Kiểm thử giả lập bao phủ lỗi mạng, không có giọng đọc, callback cũ và tắt tự động đọc.

**Chưa kiểm tra bằng trình duyệt thật, chưa xác nhận bố cục trực quan trên điện thoại và chưa nghe âm thanh trên thiết bị thật.** Vì vậy không thể kết luận mọi lỗi UI/UX hoặc mọi cách phát âm đã được loại bỏ. Trọng âm từ đồng dạng và chất lượng giọng đọc còn phụ thuộc máy/giọng đang dùng.

## Kiểm chứng và phần còn lại

Chạy:

```powershell
node build-curriculum.js
node --test test_education.js
```

48 kiểm thử hiện đạt: dữ liệu/ID/xóa C1, ví dụ và đoạn mục tiêu, tìm kiếm, khởi tạo, thêm từ, chống nội dung chèn HTML, SRS, ngày địa phương, sao lưu, lỗi dung lượng, thống kê và luồng âm thanh giả lập. Builder chạy lại cho cùng kết quả. Các kiểm thử không thay thế kiểm định ngôn ngữ, CEFR hoặc trải nghiệm thực tế.

`content-audit.json` phân biệt lỗi cấu trúc với `semanticPending`; giá trị không có lỗi mẫu câu không có nghĩa là không còn mục cần duyệt. `content-review-ledger.json` ghi trạng thái đủ 3.479 mục gốc và 320 mục bổ sung: đã biên tập, chỉ sửa nghĩa, chờ duyệt toàn bộ hoặc đã loại.

Thư viện hiện hành không còn mục chờ biên tập trong sổ theo dõi. Những việc chưa xác nhận độc lập: mức CEFR của từng nghĩa, tần suất ngữ liệu, bố cục trên trình duyệt/mobile thật và chất lượng phát âm thực tế của từng giọng UK/US. Các mục C1 đã loại được kiểm tra cấu trúc và loại khỏi giáo trình, không phải tất cả đều được viết lại ngữ nghĩa.

## Kiểm tra lại ngày 01/11/2026

- Tái hiện sáu lỗi bằng kiểm thử trước khi sửa: nút phiên kế tiếp rơi về từ B1 khi đã hết từ mới B2; phím tắt can thiệp Enter/Space của nút; giữ Enter chấm bài và Enter sau phản hồi không chuyển tiếp đúng; sao lưu cũ còn hiển thị số từ của ngày trước; đặt lại tiến độ khiến streak cùng ngày không tăng; callback câu trả lời sau khi thoát vẫn ghi tiến độ.
- Phiên kế tiếp nay giữ đúng cấp độ và báo hết từ thay vì tự đổi giáo trình. Bàn phím tôn trọng nút, phím hệ thống và bộ gõ; chống nhấn giữ liên tiếp, đưa focus đến nút Tiếp tục khi chấm xong.
- Khôi phục sao lưu chuẩn hóa ngày học trước khi ghi dữ liệu. Đặt lại tiến độ xóa mốc ngày học để phiên mới có thể bắt đầu chuỗi đúng. Callback chấm bài kiểm tra phiên còn hoạt động trước khi ghi dữ liệu.
- Thêm kiểm thử xác nhận hoàn tất phiên vẫn lưu kết quả khi canvas không khả dụng. Bổ sung nghĩa cảnh tượng cho định nghĩa sight để khớp câu ví dụ đang có.
- Kiểm thử trước đây chủ yếu là giả lập: kết luận trước đó rằng web hoạt động 100% và không có bất kỳ lỗi runtime nào là quá mức so với bằng chứng. Đợt này không xác nhận trực quan hay nghe trên trình duyệt thật.
