Ứng dụng Mô hình YOLOv8 và Phương pháp Xử lý Ảnh Kỹ thuật số trong Nhận diện Biển số Xe
📝 Giới thiệu tài liệu Đề tài

Đây là sản phẩm thực nghiệm thuộc học phần nhập môn Trí tuệ Nhân tạo tại Trường Công nghệ thông tin và Truyền thông – Đại học Công nghiệp Hà Nội (HaUI). Đề tài tập trung nghiên cứu về kiến trúc mạng nơ-ron tích chập tối ưu, cơ chế chú ý (attention mechanisms) và xây dựng bộ xử lý luồng (pipeline) tự động khép kín để hệ thống có thể phân tích, định vị và trích xuất thông tin biển số phương tiện giao thông một cách độc lập từ dữ liệu hình ảnh hoặc video tĩnh.

Hệ thống kết hợp sức mạnh kiến trúc thị giác máy tính tiên tiến của mô hình YOLOv8 (You Only Look Once phiên bản 8) để đồng thời thực hiện hai nhiệm vụ: khoanh vùng biển số xe (Bounding Box) và phân đoạn ký tự, kết hợp cùng thuật toán nhận dạng ký tự quang học (OCR) giúp chuyển đổi hình ảnh biển số thành chuỗi văn bản ký tự số với độ chính xác cao, kiểm soát sai sót toàn hệ thống thông qua cấu hình ngưỡng tin cậy (Confidence Threshold) tối ưu ở mức 0.5.
🚀 Tính năng Cốt lõi

  - Tiếp nhận dữ liệu đầu vào: Hỗ trợ xử lý luồng video trực tiếp từ camera hoặc hình ảnh tĩnh; tự động chuẩn hóa khung hình và lưu trữ.
  - Định vị biển số (YOLOv8): Tự động phát hiện và khoanh vùng (bounding box) các loại biển số xe (ô tô, xe máy) trong các điều kiện ánh sáng và góc chụp khác nhau.
  - Cắt vùng và Xử lý ảnh: Trích xuất vùng chứa biển số (Crop), thực hiện nhị phân hóa và căn chỉnh góc nghiêng để tối ưu hóa dữ liệu cho bước nhận diện.
  - Nhận diện ký tự (OCR): Phân tách và chuyển đổi hình ảnh các chữ số, ký tự trên biển số thành chuỗi văn bản (text) với độ chính xác cao.
  - Bộ lọc và Trực quan hóa: Loại bỏ các kết quả có độ tin cậy thấp (Confidence < 0.5) và hiển thị trực tiếp khung bao màu kèm chuỗi ký tự nhận diện lên màn hình.

👥 Thành viên Thực hiện (Nhóm 6)

Giảng viên hướng dẫn: TS. Trần Thanh Huân

Sinh viên triển khai:

Hồ Hữu Hoàng (Mã SV: 2024606561)
Vũ Thị Hương (Mã SV: 2024609007)
Nguyễn Phùng Hải Lý (Mã SV: 2024607888)
Lê Xuân Trường (Mã SV: 2024608925)
Trịnh Minh Tiến (Mã SV: 2024607881)
