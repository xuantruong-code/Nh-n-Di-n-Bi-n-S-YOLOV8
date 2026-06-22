from ultralytics import YOLO
import easyocr
import cv2
import os
import re

# 1. ĐƯỜNG DẪN VIDEO CỦA BẠN
VIDEO_PATH = r"D:\NhanDienBienSo\video1.mp4"
# Đường dẫn video xuất ra
OUTPUT_PATH = r"D:\NhanDienBienSo\ket_qua_video.mp4"


def nhan_dien_video(video_path, output_path):
    if not os.path.exists(video_path):
        print(f"Lỗi: Không tìm thấy video tại {video_path}")
        return

    print("1. Đang tải mô hình YOLOv8 và EasyOCR...")
    model = YOLO("https://huggingface.co/Koushim/yolov8-license-plate-detection/resolve/main/best.pt")
    reader = easyocr.Reader(['en'], gpu=False)

    print("2. Đang mở video...")
    cap = cv2.VideoCapture(video_path)

    # Lấy thông số của video gốc để tạo video đầu ra y hệt
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    tong_so_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Công cụ ghi video của OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    print(f"Bắt đầu xử lý {tong_so_frame} khung hình. Vui lòng đợi, quá trình này sẽ hơi lâu...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Hết video thì dừng

        frame_count += 1

        # Quét YOLO trên khung hình hiện tại
        results = model.predict(source=frame, conf=0.3, verbose=False)
        boxes = results[0].boxes

        # Nếu có biển số thì xử lý
        if len(boxes) > 0:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Cắt vùng biển số để đọc chữ
                vung_bien_so = frame[y1:y2, x1:x2]
                gray = cv2.cvtColor(vung_bien_so, cv2.COLOR_BGR2GRAY)

                # EasyOCR đọc chữ
                ket_qua_ocr = reader.readtext(gray)

                bien_so_text = ""
                if len(ket_qua_ocr) > 0:
                    ket_qua_ocr.sort(key=lambda x: x[0][0][1])
                    for (toa_do, text, prob) in ket_qua_ocr:
                        clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
                        bien_so_text += clean_text

                # Vẽ khung và nền đỏ
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

                font = cv2.FONT_HERSHEY_SIMPLEX
                (text_width, text_height), _ = cv2.getTextSize(bien_so_text, font, 1, 2)

                if y1 - text_height - 10 < 0:
                    bg_y1, bg_y2 = y2, y2 + text_height + 15
                    text_y = y2 + text_height + 5
                else:
                    bg_y1, bg_y2 = y1 - text_height - 15, y1
                    text_y = y1 - 5

                cv2.rectangle(frame, (x1, bg_y1), (x1 + text_width + 10, bg_y2), (0, 0, 255), -1)
                cv2.putText(frame, bien_so_text, (x1 + 5, text_y), font, 1, (255, 255, 255), 2)

        # Ghi khung hình đã vẽ vào video mới
        out.write(frame)

        # In tiến độ cho đỡ sốt ruột
        if frame_count % 10 == 0:
            print(f"  Đã xử lý: {frame_count}/{tong_so_frame} khung hình...")

    # Giải phóng bộ nhớ
    cap.release()
    out.release()
    print(f"\n✅ Xong! Video kết quả đã được lưu tại: {output_path}")


if __name__ == "__main__":
    nhan_dien_video(VIDEO_PATH, OUTPUT_PATH)