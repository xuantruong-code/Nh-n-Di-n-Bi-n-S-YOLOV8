from ultralytics import YOLO
import cv2
import os


IMAGE_PATH = r"D:\NhanDienBienSo\abc.jpg"

def nhan_dien_co_ban(image_path):
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy ảnh tại {image_path}")
        return
    print("1. Đang tải mô hình YOLOv8...")
    # Sử dụng mô hình nhận diện biển số đã được huấn luyện sẵn
    model = YOLO("https://huggingface.co/Koushim/yolov8-license-plate-detection/resolve/main/best.pt")

    print("2. Đang quét ảnh để tìm biển số...")
    # conf=0.5 nghĩa là mô hình phải chắc chắn trên 50% đó là biển số thì mới nhận
    results = model.predict(source=image_path, conf=0.5)

    print("3. Đang xử lý và vẽ kết quả...")
    # Lệnh plot() của YOLOv8 sẽ tự động vẽ một khung chữ nhật bao quanh biển số tìm được
    img_ket_qua = results[0].plot()

    # 4. Lưu ảnh kết quả ra máy tính
    duong_dan_luu = "ket_qua_yolo.jpg"
    cv2.imwrite(duong_dan_luu, img_ket_qua)
    print(f"\nThành công! Đã lưu ảnh kết quả tại: {duong_dan_luu}")

    # (Tùy chọn) Hiển thị ảnh lên màn hình
    # Cửa sổ sẽ tự đóng khi bạn bấm phím bất kỳ
    cv2.imshow("YOLOv8 - Nhan dien bien so", img_ket_qua)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("=== CHƯƠNG TRÌNH YOLOv8 CƠ BẢN ===")
    nhan_dien_co_ban(IMAGE_PATH)