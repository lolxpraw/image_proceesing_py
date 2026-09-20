"""
Step 2: Chuyển đổi từ RGB.raw -> gray.raw (8 bit/pixel)
THAY THẾ CHƯƠNG TRÌNH C BẰNG PYTHON

File đầu vào: rgb.raw (24 bit/pixel, width x height x 3 bytes)
File đầu ra:  gray.raw (8 bit/pixel, width x height bytes)

Công thức chuyển đổi mức xám (Grayscale Luminance BT.601):
    Gray = round(0.299 * R + 0.587 * G + 0.114 * B)

Tương đương logic chương trình C:
    unsigned char rgb[3];
    fread(rgb, sizeof(unsigned char), 3, f_in);
    unsigned char gray = (unsigned char)(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]);
    fwrite(&gray, sizeof(unsigned char), 1, f_out);
"""

import os
import sys

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi bảng mã (UnicodeEncodeError)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from PIL import Image
import numpy as np

def rgb_raw_to_gray_raw(input_raw_path="rgb.raw", 
                        output_raw_path="gray.raw", 
                        preview_png_path="gray_preview.png",
                        width=512, 
                        height=512):
    """
    Đọc dữ liệu thô từ file rgb.raw và chuyển đổi sang gray.raw
    Thao tác trực tiếp với các byte nhị phân thô (tương tự con trỏ / mảng byte trong C)
    """
    if not os.path.exists(input_raw_path):
        print(f"[Lỗi] Không tìm thấy file '{input_raw_path}'! Hãy chạy Step 1 trước.")
        return False
        
    expected_size = width * height * 3
    actual_size = os.path.getsize(input_raw_path)
    if actual_size != expected_size:
        print(f"[Cảnh báo] Kích thước file ({actual_size:,} bytes) khác dự kiến ({expected_size:,} bytes).")
        calculated_pixels = actual_size // 3
        side = int(calculated_pixels ** 0.5)
        if side * side * 3 == actual_size:
            width = height = side
            print(f"           -> Đã tự động điều chỉnh kích thước: {width} x {height}")

    print(f"[Step 2] Đang đọc '{input_raw_path}'...")
    
    # Đọc dữ liệu nhị phân thô mô phỏng tương tự fread trong C
    with open(input_raw_path, "rb") as f_in:
        raw_rgb_data = f_in.read()

    total_pixels = width * height
    # Cấp phát bộ nhớ cho mảng byte kết quả (tương tự malloc trong C: unsigned char *gray_buf)
    gray_buffer = bytearray(total_pixels)
    
    # Duyệt qua từng pixel (mỗi pixel chiếm 3 byte liên tiếp: R, G, B)
    for i in range(total_pixels):
        offset = i * 3
        r = raw_rgb_data[offset]
        g = raw_rgb_data[offset + 1]
        b = raw_rgb_data[offset + 2]
        
        # Áp dụng công thức chuyển đổi mức xám chuẩn
        gray_val = int(0.299 * r + 0.587 * g + 0.114 * b + 0.5)  # +0.5 để làm tròn
        
        if gray_val > 255:
            gray_val = 255
        elif gray_val < 0:
            gray_val = 0
            
        gray_buffer[i] = gray_val

    # Ghi mảng byte ra file gray.raw (tương tự fwrite trong C)
    with open(output_raw_path, "wb") as f_out:
        f_out.write(gray_buffer)

    out_size = os.path.getsize(output_raw_path)
    print(f"[Step 2] Đã tạo thành công file RAW ảnh xám: '{output_raw_path}'")
    print(f"         - Kích thước ảnh: {width} x {height}")
    print(f"         - Độ sâu màu: 8 bit/pixel (1 byte/pixel)")
    print(f"         - Dung lượng file: {out_size:,} bytes ({width} x {height} x 1 = {width * height:,} bytes)")
    
    # Lưu file PNG preview để xem trước kết quả
    gray_arr = np.frombuffer(gray_buffer, dtype=np.uint8).reshape((height, width))
    img = Image.fromarray(gray_arr, mode='L')
    img.save(preview_png_path)
    print(f"         - Đã lưu ảnh xem trước: '{preview_png_path}'")
    return True

if __name__ == "__main__":
    w = 512
    h = 512
    if len(sys.argv) >= 3:
        w = int(sys.argv[1])
        h = int(sys.argv[2])
    elif os.path.exists("image_dim.txt"):
        try:
            with open("image_dim.txt", "r") as f_dim:
                parts = f_dim.read().strip().split()
                w, h = int(parts[0]), int(parts[1])
        except Exception:
            pass
        
    rgb_raw_to_gray_raw("rgb.raw", "gray.raw", "gray_preview.png", width=w, height=h)

