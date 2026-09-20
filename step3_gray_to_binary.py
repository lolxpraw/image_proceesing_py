"""
Step 3: Chuyển ảnh xám sang ảnh nhị phân (Binary scale)
File đầu vào: gray.raw (8 bit/pixel, width x height bytes)
File đầu ra:  binary.raw (8 bit/pixel: các điểm ảnh có giá trị 0 hoặc 255)

Nguyên lý phân ngưỡng (Thresholding):
    Nếu Gray >= Threshold: Pixel = 255 (Trắng)
    Ngược lại:              Pixel = 0   (Đen)

Mặc định Threshold = 128 (có thể thay đổi tùy ý).
Định dạng file binary.raw này khi mở bằng Photoshop:
    - Channels: 1
    - Depth: 8 Bits
    - Header: 0 bytes
"""

import os
import sys

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi bảng mã (UnicodeEncodeError)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from PIL import Image
import numpy as np

def gray_raw_to_binary_raw(input_raw_path="gray.raw",
                           output_raw_path="binary.raw",
                           preview_png_path="binary_preview.png",
                           width=512,
                           height=512,
                           threshold=128):
    """
    Đọc dữ liệu thô từ file gray.raw và chuyển sang binary scale
    """
    if not os.path.exists(input_raw_path):
        print(f"[Lỗi] Không tìm thấy file '{input_raw_path}'! Hãy chạy Step 2 trước.")
        return False

    expected_size = width * height
    actual_size = os.path.getsize(input_raw_path)
    if actual_size != expected_size:
        print(f"[Cảnh báo] Kích thước file ({actual_size:,} bytes) khác dự kiến ({expected_size:,} bytes).")
        side = int(actual_size ** 0.5)
        if side * side == actual_size:
            width = height = side
            print(f"           -> Đã tự động điều chỉnh kích thước: {width} x {height}")

    print(f"[Step 3] Đang đọc '{input_raw_path}' với ngưỡng threshold = {threshold}...")

    # Đọc dữ liệu ảnh xám thô
    with open(input_raw_path, "rb") as f_in:
        gray_data = f_in.read()

    total_pixels = width * height
    binary_buffer = bytearray(total_pixels)

    # Duyệt qua từng pixel để so sánh với ngưỡng threshold
    for i in range(total_pixels):
        pixel_val = gray_data[i]
        binary_buffer[i] = 255 if pixel_val >= threshold else 0

    # Ghi kết quả ra file binary.raw
    with open(output_raw_path, "wb") as f_out:
        f_out.write(binary_buffer)

    out_size = os.path.getsize(output_raw_path)
    print(f"[Step 3] Đã tạo thành công file RAW ảnh nhị phân: '{output_raw_path}'")
    print(f"         - Kích thước ảnh: {width} x {height}")
    print(f"         - Phân ngưỡng: Threshold = {threshold}")
    print(f"         - Giá trị pixel: Chỉ gồm 0 (đen) và 255 (trắng)")
    print(f"         - Dung lượng file: {out_size:,} bytes")

    # Lưu file PNG preview
    bin_arr = np.frombuffer(binary_buffer, dtype=np.uint8).reshape((height, width))
    img = Image.fromarray(bin_arr, mode='L')
    img.save(preview_png_path)
    print(f"         - Đã lưu ảnh xem trước: '{preview_png_path}'")
    return True

if __name__ == "__main__":
    thresh = 128
    w = 512
    h = 512
    if len(sys.argv) >= 2:
        thresh = int(sys.argv[1])
    if len(sys.argv) >= 4:
        w = int(sys.argv[2])
        h = int(sys.argv[3])
    elif os.path.exists("image_dim.txt"):
        try:
            with open("image_dim.txt", "r") as f_dim:
                parts = f_dim.read().strip().split()
                w, h = int(parts[0]), int(parts[1])
        except Exception:
            pass
        
    gray_raw_to_binary_raw("gray.raw", "binary.raw", "binary_preview.png", width=w, height=h, threshold=thresh)

