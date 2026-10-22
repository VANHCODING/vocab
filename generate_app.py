# -*- coding: utf-8 -*-
"""
LexiUp Application Generator
Generates index.html and vocab-dataset.json
"""
import json
import os

# Import the 90 items from build_lexiup
from build_lexiup import VOCAB_ITEMS

# Additional bonus words for the extension pack (30 extra items: 10 B1, 10 B2, 10 C1)
EXTENDED_ITEMS = [
    # B1 Bonus
    {
        "id": "b1-ex01",
        "word": "negotiate",
        "ipa": "/nɪˈɡəʊʃieɪt/",
        "pos": "verb",
        "meaningVi": "thương lượng, đàm phán",
        "definitionEn": "Try to reach an agreement or compromise by discussion.",
        "example": "He managed to negotiate a lower price for the second-hand motorbike.",
        "exampleVi": "Anh ấy đã thương lượng được mức giá thấp hơn cho chiếc xe máy cũ.",
        "level": "B1",
        "topic": "Công việc & Nghề nghiệp"
    },
    {
        "id": "b1-ex02",
        "word": "convenience",
        "ipa": "/kənˈviːniəns/",
        "pos": "noun",
        "meaningVi": "sự tiện lợi, thuận tiện",
        "definitionEn": "The state of being able to proceed with something without difficulty.",
        "example": "The online payment app offers great convenience for busy young workers.",
        "exampleVi": "Ứng dụng thanh toán trực tuyến mang lại sự tiện lợi lớn cho người lao động bận rộn.",
        "level": "B1",
        "topic": "Ẩm thực & Mua sắm"
    },
    {
        "id": "b1-ex03",
        "word": "enthusiastic",
        "ipa": "/ɪnˌθjuːziˈæstɪk/",
        "pos": "adjective",
        "meaningVi": "nhiệt tình, hào hứng",
        "definitionEn": "Having or showing intense and eager enjoyment, interest, or approval.",
        "example": "The young volunteers were extremely enthusiastic about teaching rural children English.",
        "exampleVi": "Các tình nguyện viên trẻ vô cùng nhiệt tình với việc dạy tiếng Anh cho trẻ em nông thôn.",
        "level": "B1",
        "topic": "Đời sống & Cảm xúc"
    },
    {
        "id": "b1-ex04",
        "word": "reservation",
        "ipa": "/ˌrezəˈveɪʃn/",
        "pos": "noun",
        "meaningVi": "sự đặt chỗ trước",
        "definitionEn": "An arrangement whereby something, especially a seat or room, is reserved.",
        "example": "We made a dinner reservation at the riverside seafood restaurant yesterday.",
        "exampleVi": "Hôm qua chúng tôi đã đặt bàn ăn tối tại nhà hàng hải sản ven sông.",
        "level": "B1",
        "topic": "Du lịch & Đi lại"
    },
    {
        "id": "b1-ex05",
        "word": "satisfaction",
        "ipa": "/ˌsætɪsˈfækʃn/",
        "pos": "noun",
        "meaningVi": "sự hài lòng, thỏa mãn",
        "definitionEn": "Fulfillment of one's wishes, expectations, or needs.",
        "example": "Customer satisfaction is the number one priority for this retail brand.",
        "exampleVi": "Sự hài lòng của khách hàng là ưu tiên số một của thương hiệu bán lẻ này.",
        "level": "B1",
        "topic": "Ẩm thực & Mua sắm"
    },
    {
        "id": "b1-ex06",
        "word": "reliable",
        "ipa": "/rɪˈlaɪəbl/",
        "pos": "adjective",
        "meaningVi": "đáng tin cậy",
        "definitionEn": "Consistently good in quality or performance, and able to be trusted.",
        "example": "She is a reliable assistant who always finishes every assigned task promptly.",
        "exampleVi": "Cô ấy là một trợ lý đáng tin cậy luôn hoàn thành nhanh chóng mọi công việc được giao.",
        "level": "B1",
        "topic": "Công việc & Nghề nghiệp"
    },
    {
        "id": "b1-ex07",
        "word": "patience",
        "ipa": "/ˈpeɪʃns/",
        "pos": "noun",
        "meaningVi": "sự kiên nhẫn, nhẫn nại",
        "definitionEn": "The capacity to accept or tolerate delay or suffering without anger.",
        "example": "Learning a foreign language requires endless patience and daily conversational practice.",
        "exampleVi": "Học một ngoại ngữ đòi hỏi sự kiên nhẫn không ngừng và luyện giao tiếp hàng ngày.",
        "level": "B1",
        "topic": "Đời sống & Cảm xúc"
    },
    {
        "id": "b1-ex08",
        "word": "scenery",
        "ipa": "/ˈsiːnəri/",
        "pos": "noun",
        "meaningVi": "phong cảnh thiên nhiên",
        "definitionEn": "The natural features of a landscape considered in terms of appearance.",
        "example": "The mountainous scenery along the northern pass took our breath away.",
        "exampleVi": "Phong cảnh miền núi dọc theo con đèo phía bắc đã làm chúng tôi choáng ngợp.",
        "level": "B1",
        "topic": "Du lịch & Đi lại"
    },
    {
        "id": "b1-ex09",
        "word": "punctual",
        "ipa": "/ˈpʌŋktʃuəl/",
        "pos": "adjective",
        "meaningVi": "đúng giờ",
        "definitionEn": "Happening or doing something at the agreed or proper time.",
        "example": "Being punctual for business meetings shows professionalism and deep respect for partners.",
        "exampleVi": "Đúng giờ trong các cuộc họp kinh doanh thể hiện sự chuyên nghiệp và tôn trọng đối tác.",
        "level": "B1",
        "topic": "Công việc & Nghề nghiệp"
    },
    {
        "id": "b1-ex10",
        "word": "delicious",
        "ipa": "/dɪˈlɪʃəs/",
        "pos": "adjective",
        "meaningVi": "thơm ngon, ngon miệng",
        "definitionEn": "Highly pleasant to the taste.",
        "example": "Street vendors in Da Nang serve delicious grilled pork noodles every evening.",
        "exampleVi": "Các hàng quán vỉa hè ở Đà Nẵng phục vụ món bún thịt nướng thơm ngon mỗi tối.",
        "level": "B1",
        "topic": "Ẩm thực & Mua sắm"
    },

    # B2 Bonus
    {
        "id": "b2-ex01",
        "word": "deteriorate",
        "ipa": "/dɪˈtɪəriəreɪt/",
        "pos": "verb",
        "meaningVi": "xuống cấp, xấu đi",
        "definitionEn": "Become progressively worse over time.",
        "example": "Air quality in major industrial cities continues to deteriorate during winter months.",
        "exampleVi": "Chất lượng không khí tại các thành phố công nghiệp lớn tiếp tục xấu đi trong những tháng mùa đông.",
        "level": "B2",
        "topic": "Môi trường & Bền vững"
    },
    {
        "id": "b2-ex02",
        "word": "cryptocurrency",
        "ipa": "/ˈkrɪptəʊkʌrənsi/",
        "pos": "noun",
        "meaningVi": "tiền mã hóa, tiền số",
        "definitionEn": "A digital currency in which transactions are verified by cryptography.",
        "example": "Young investors should understand the volatile risks associated with decentralized cryptocurrency trading.",
        "exampleVi": "Các nhà đầu tư trẻ nên hiểu rõ những rủi ro biến động gắn liền với giao dịch tiền mã hóa phi tập trung.",
        "level": "B2",
        "topic": "Công nghệ & Đổi mới"
    },
    {
        "id": "b2-ex03",
        "word": "entrepreneurship",
        "ipa": "/ˌɒntrəprəˈnɜːʃɪp/",
        "pos": "noun",
        "meaningVi": "tinh thần khởi nghiệp",
        "definitionEn": "The activity of setting up a business or businesses, taking financial risks.",
        "example": "University incubators actively foster entrepreneurship by offering seed funding and mentorship.",
        "exampleVi": "Các vườn ươm đại học tích cực nuôi dưỡng tinh thần khởi nghiệp bằng cách cấp vốn hạt giống và cố vấn.",
        "level": "B2",
        "topic": "Kinh tế & Kinh doanh"
    },
    {
        "id": "b2-ex04",
        "word": "inequality",
        "ipa": "/ˌɪnɪˈkwɒləti/",
        "pos": "noun",
        "meaningVi": "sự bất bình đẳng",
        "definitionEn": "Difference in size, degree, or circumstances; lack of equality.",
        "example": "Progressive tax policies aim to reduce widening wealth inequality across developing societies.",
        "exampleVi": "Các chính sách thuế lũy tiến nhằm giảm thiểu sự bất bình đẳng giàu nghèo đang gia tăng trong các xã hội đang phát triển.",
        "level": "B2",
        "topic": "Xã hội & Giáo dục"
    },
    {
        "id": "b2-ex05",
        "word": "deplete",
        "ipa": "/dɪˈpliːt/",
        "pos": "verb",
        "meaningVi": "làm cạn kiệt",
        "definitionEn": "Use up the supply or resources of something.",
        "example": "Excessive groundwater extraction threatens to deplete freshwater reserves for future urban generations.",
        "exampleVi": "Việc khai thác nước ngầm quá mức có nguy cơ làm cạn kiệt các nguồn dự trữ nước ngọt cho các thế hệ tương lai.",
        "level": "B2",
        "topic": "Môi trường & Bền vững"
    },
    {
        "id": "b2-ex06",
        "word": "disruptive",
        "ipa": "/dɪsˈrʌptɪv/",
        "pos": "adjective",
        "meaningVi": "mang tính đột phá, đột phá thị trường",
        "definitionEn": "Innovatively replacing an established industry, technology, or business model.",
        "example": "Ride-sharing mobile apps introduced disruptive innovation that revolutionized traditional city taxi transportation.",
        "exampleVi": "Các ứng dụng gọi xe trên di động đã mang đến sự đổi mới đột phá làm cách mạng hóa phương thức vận tải taxi truyền thống.",
        "level": "B2",
        "topic": "Công nghệ & Đổi mới"
    },
    {
        "id": "b2-ex07",
        "word": "acquisition",
        "ipa": "/ˌækwɪˈzɪʃn/",
        "pos": "noun",
        "meaningVi": "sự mua lại, thâu tóm doanh nghiệp",
        "definitionEn": "An asset or object bought or obtained, or the takeover of a company.",
        "example": "The corporate acquisition allowed the domestic firm to expand into European markets.",
        "exampleVi": "Thương vụ mua lại doanh nghiệp đã cho phép công ty trong nước mở rộng sang các thị trường châu Âu.",
        "level": "B2",
        "topic": "Kinh tế & Kinh doanh"
    },
    {
        "id": "b2-ex08",
        "word": "emancipation",
        "ipa": "/ɪˌmænsɪˈpeɪʃn/",
        "pos": "noun",
        "meaningVi": "sự giải phóng, trao quyền",
        "definitionEn": "The fact or process of being set free from legal, social, or political restrictions.",
        "example": "Universal public education remains the bedrock of socioeconomic emancipation for marginalized groups.",
        "exampleVi": "Giáo dục công lập phổ cập vẫn là nền tảng cho sự giải phóng kinh tế xã hội của các nhóm yếu thế.",
        "level": "B2",
        "topic": "Xã hội & Giáo dục"
    },
    {
        "id": "b2-ex09",
        "word": "feasibility",
        "ipa": "/ˌfiːzəˈbɪləti/",
        "pos": "noun",
        "meaningVi": "tính khả thi",
        "definitionEn": "The state or degree of being easily or conveniently done.",
        "example": "Engineers conducted an exhaustive feasibility study before commencing subway tunnel construction.",
        "exampleVi": "Các kỹ sư đã tiến hành một nghiên cứu tính khả thi kỹ lưỡng trước khi bắt đầu xây dựng đường hầm tàu điện ngầm.",
        "level": "B2",
        "topic": "Kinh tế & Kinh doanh"
    },
    {
        "id": "b2-ex10",
        "word": "accessible",
        "ipa": "/əkˈsesəbl/",
        "pos": "adjective",
        "meaningVi": "dễ tiếp cận, tiếp cận được",
        "definitionEn": "Able to be reached or entered, or easily understood.",
        "example": "Online distance learning makes world-class academic courses accessible to remote students globally.",
        "exampleVi": "Học trực tuyến từ xa giúp sinh viên ở vùng sâu vùng xa trên toàn cầu có thể tiếp cận các khóa học học thuật đẳng cấp thế giới.",
        "level": "B2",
        "topic": "Xã hội & Giáo dục"
    },

    # C1 Bonus
    {
        "id": "c1-ex01",
        "word": "ephemeral",
        "ipa": "/ɪˈfemərəl/",
        "pos": "adjective",
        "meaningVi": "phù du, chóng tàn",
        "definitionEn": "Lasting for a very short time; fleeting.",
        "example": "Social media viral fame is notoriously ephemeral compared to enduring creative masterpieces.",
        "exampleVi": "Sự nổi tiếng lan truyền trên mạng xã hội vốn dĩ rất phù du khi so sánh với những kiệt tác sáng tạo trường tồn.",
        "level": "C1",
        "topic": "Học thuật & Tranh biện"
    },
    {
        "id": "c1-ex02",
        "word": "anachronism",
        "ipa": "/əˈnækrənɪzəm/",
        "pos": "noun",
        "meaningVi": "sự lỗi thời, sai thời đại",
        "definitionEn": "A thing belonging to a period other than that in which it exists.",
        "example": "Relying on manual paper logs in an automated hospital is an indefensible anachronism.",
        "exampleVi": "Việc phụ thuộc vào sổ ghi chép giấy thủ công trong một bệnh viện tự động hóa là một sự lỗi thời không thể biện minh.",
        "level": "C1",
        "topic": "Chính sách & Thể chế"
    },
    {
        "id": "c1-ex03",
        "word": "juxtaposition",
        "ipa": "/ˌdʒʌkstəpəˈzɪʃn/",
        "pos": "noun",
        "meaningVi": "sự đặt cạnh nhau để tương phản",
        "definitionEn": "The fact of two things being seen or placed close together with contrasting effect.",
        "example": "The dramatic juxtaposition of futuristic skyscrapers against ancient pagodas fascinates visiting tourists.",
        "exampleVi": "Sự đặt cạnh nhau ấn tượng giữa các tòa nhà chọc trời tương lai với các ngôi chùa cổ kính làm say đắm du khách đến thăm.",
        "level": "C1",
        "topic": "Học thuật & Tranh biện"
    },
    {
        "id": "c1-ex04",
        "word": "reticence",
        "ipa": "/ˈretɪsns/",
        "pos": "noun",
        "meaningVi": "sự kín đáo, dè dặt",
        "definitionEn": "The quality of being reserved or not revealing one's thoughts readily.",
        "example": "Her diplomatic reticence was often misinterpreted by aggressive trade negotiators as indecisiveness.",
        "exampleVi": "Sự dè dặt mang tính ngoại giao của cô thường bị các nhà đàm phán thương mại hung hăng hiểu sai thành sự thiếu quyết đoán.",
        "level": "C1",
        "topic": "Tâm lý & Nhận thức"
    },
    {
        "id": "c1-ex05",
        "word": "touch upon",
        "ipa": "/tʌtʃ əˈpɒn/",
        "pos": "phrasal verb",
        "meaningVi": "đề cập ngắn gọn đến",
        "definitionEn": "Mention a topic briefly or in passing.",
        "example": "The keynote lecture only touched upon macroeconomic factors before delving into micro-finance.",
        "exampleVi": "Bài diễn thuyết chính chỉ đề cập ngắn gọn đến các yếu tố kinh tế vĩ mô trước khi đi sâu vào tài chính vi mô.",
        "level": "C1",
        "topic": "Thành ngữ & Cụm nâng cao"
    },
    {
        "id": "c1-ex06",
        "word": "catalyst",
        "ipa": "/ˈkætəlɪst/",
        "pos": "noun",
        "meaningVi": "chất xúc tác, nhân tố thúc đẩy",
        "definitionEn": "A person or thing that precipitates an event or change.",
        "example": "The global pandemic acted as an unexpected catalyst for widespread remote work adoption.",
        "exampleVi": "Đại dịch toàn cầu đã đóng vai trò như một chất xúc tác bất ngờ cho việc áp dụng làm việc từ xa rộng rãi.",
        "level": "C1",
        "topic": "Chính sách & Thể chế"
    },
    {
        "id": "c1-ex07",
        "word": "ubiquity",
        "ipa": "/juːˈbɪkwəti/",
        "pos": "noun",
        "meaningVi": "sự phổ biến khắp nơi",
        "definitionEn": "The state or capacity of being everywhere at once.",
        "example": "The ubiquity of portable computing devices fundamentally altered human attention spans and study habits.",
        "exampleVi": "Sự phổ biến khắp nơi của các thiết bị máy tính cầm tay đã làm thay đổi căn bản khả năng chú ý và thói quen học tập của con người.",
        "level": "C1",
        "topic": "Học thuật & Tranh biện"
    },
    {
        "id": "c1-ex08",
        "word": "in tandem with",
        "ipa": "/ɪn ˈtændəm wɪð/",
        "pos": "phrase",
        "meaningVi": "song hành cùng với",
        "definitionEn": "Alongside each other; in conjunction.",
        "example": "Fiscal policy must work in tandem with monetary adjustments to tame runaway inflation.",
        "exampleVi": "Chính sách tài khóa phải hoạt động song hành cùng với các điều chỉnh tiền tệ để kìm hãm lạm phát phi mã.",
        "level": "C1",
        "topic": "Thành ngữ & Cụm nâng cao"
    },
    {
        "id": "c1-ex09",
        "word": "vicarious",
        "ipa": "/vɪˈkeəriəs/",
        "pos": "adjective",
        "meaningVi": "gián tiếp, trải nghiệm qua người khác",
        "definitionEn": "Experienced in the imagination through the feelings or actions of another.",
        "example": "Reading international adventure novels provided him with a thrilling vicarious sense of exploration.",
        "exampleVi": "Đọc các tiểu thuyết phiêu lưu quốc tế đã mang lại cho anh một cảm giác thám hiểm gián tiếp đầy ly kỳ.",
        "level": "C1",
        "topic": "Tâm lý & Nhận thức"
    },
    {
        "id": "c1-ex10",
        "word": "stand in the way of",
        "ipa": "/stænd ɪn ðə weɪ əv/",
        "pos": "phrase",
        "meaningVi": "cản trở, ngáng đường",
        "definitionEn": "Prevent or hinder something from happening or progressing.",
        "example": "Bureaucratic inertia should never stand in the way of lifesaving technological healthcare innovation.",
        "exampleVi": "Sự trì trệ quan liêu không bao giờ được phép cản trở sự đổi mới công nghệ y tế cứu sống con người.",
        "level": "C1",
        "topic": "Thành ngữ & Cụm nâng cao"
    }
]

# Write standalone vocab-dataset.json
dataset_path = r"C:\Users\vanh\.gemini\antigravity\scratch\lexiup\vocab-dataset.json"
with open(dataset_path, "w", encoding="utf-8") as f:
    json.dump(VOCAB_ITEMS, f, ensure_ascii=False, indent=2)

print(f"Written vocab-dataset.json ({len(VOCAB_ITEMS)} items)")

# Prepare HTML components
vocab_json_string = json.dumps(VOCAB_ITEMS, ensure_ascii=False, indent=2)
extended_json_string = json.dumps(EXTENDED_ITEMS, ensure_ascii=False, indent=2)

print("Ready to assemble index.html")
