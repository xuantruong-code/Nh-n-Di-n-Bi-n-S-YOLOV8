from ultralytics import YOLO
import easyocr
import cv2
import os
import re

# 1. ĐƯỜNG DẪN ẢNH CỦA BẠN (Đổi tên ảnh ở đây, ví dụ: abc.jpg)
IMAGE_PATH = r"D:\NhanDienBienSo\abc.jpg"


def nhan_dien_va_doc_chu(image_path):
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy ảnh tại {image_path}")
        return

    # Khởi tạo mô hình
    print("1. Đang tải mô hình YOLOv8...")
    model = YOLO("https://huggingface.co/Koushim/yolov8-license-plate-detection/resolve/main/best.pt")

    print("2. Đang tải EasyOCR (có thể mất 15-30s cho lần đầu)...")
    reader = easyocr.Reader(['en'], gpu=False)

    # Đọc ảnh gốc bằng OpenCV
    img = cv2.imread(image_path)

    print("3. Đang quét tìm biển số...")
    results = model.predict(source=img, conf=0.3)
    boxes = results[0].boxes

    if len(boxes) == 0:
        print("-> Không tìm thấy biển số nào trong ảnh này.")
        return

    print(f"-> Tìm thấy {len(boxes)} biển số. Đang bắt đầu đọc chữ...")

    # Xử lý từng biển số tìm được
    for i, box in enumerate(boxes):
        # Lấy tọa độ [x1, y1, x2, y2]
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Cắt ảnh đúng vùng biển số
        vung_bien_so = img[y1:y2, x1:x2]

        # Chuyển sang ảnh xám để OCR đọc nét hơn
        gray = cv2.cvtColor(vung_bien_so, cv2.COLOR_BGR2GRAY)

        # Đưa cho EasyOCR đọc
        ket_qua_ocr = reader.readtext(gray)

        bien_so_text = ""
        if len(ket_qua_ocr) == 0:
            bien_so_text = "KHONG_DOC_DUOC"
        else:
            # Thuật toán: Sắp xếp theo tọa độ Y (giải quyết biển 2 dòng)
            ket_qua_ocr.sort(key=lambda x: x[0][0][1])
            for (toa_do, text, prob) in ket_qua_ocr:
                # Dùng Regex để chỉ giữ lại Chữ cái và Số (Xóa khoảng trắng, dấu chấm, gạch ngang)
                clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
                bien_so_text += clean_text

        print(f"   => Biển số #{i + 1}: {bien_so_text}")

        # --- VẼ LÊN ẢNH ---
        # 1. Vẽ khung chữ nhật bao quanh biển (Màu Đỏ)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        # 2. Cấu hình Font chữ
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2

        # 3. Tính toán kích thước chữ để vẽ background
        (text_width, text_height), baseline = cv2.getTextSize(bien_so_text, font, font_scale, thickness)

        # 4. Chống tràn màn hình: Tính tọa độ in chữ
        if y1 - text_height - 10 < 0:  # Nếu sát mép trên quá thì in xuống dưới mép dưới
            bg_y1, bg_y2 = y2, y2 + text_height + 15
            text_y = y2 + text_height + 5
        else:  # Bình thường thì in nổi lên trên mép trên
            bg_y1, bg_y2 = y1 - text_height - 15, y1
            text_y = y1 - 5

        # 5. Vẽ hình chữ nhật làm nền cho chữ (Màu Đỏ đặc)
        cv2.rectangle(img, (x1, bg_y1), (x1 + text_width + 10, bg_y2), (0, 0, 255), -1)

        # 6. In chữ lên nền (Màu Trắng)
        cv2.putText(img, bien_so_text, (x1 + 5, text_y), font, font_scale, (255, 255, 255), thickness)

    # Lưu kết quả
    duong_dan_luu = "ket_qua_Full_OCR.jpg"
    cv2.imwrite(duong_dan_luu, img)
    print(f"\n✅ Hoàn tất! Đã xuất ảnh có chứa dòng chữ nhận diện tại: {duong_dan_luu}")



if __name__ == "__main__":
    print("=" * 50)
    print("HỆ THỐNG YOLOv8 + EASYOCR HOÀN CHỈNH")
    print("=" * 50)
    nhan_dien_va_doc_chu(IMAGE_PATH)