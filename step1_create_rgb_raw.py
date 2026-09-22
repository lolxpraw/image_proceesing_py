"""
Step 1: Tạo ra ảnh màu RGB chuẩn RAW (24 bit/pixel = 3 byte/pixel: R, G, B)
File đầu ra: rgb.raw
Được kiểm tra bằng Adobe Photoshop:
  - Width: 512, Height: 512
  - Channels: 3
  - Depth: 8 Bits
  - Interleaved: Yes
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

def create_sample_rgb_image(width=512, height=512):
    """
    Tạo một ảnh màu mẫu 512x512 có các dải màu phong phú:
    - Nửa trên: Các khối màu cơ bản (Đỏ, Xanh lá, Xanh dương, Vàng, Cyan, Magenta, Trắng, Đen)
    - Nửa dưới: Gradient màu mượt mà để kiểm tra dải sắc độ khi chuyển sang ảnh xám
    """
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # 8 màu cơ bản ở nửa trên (chiều cao height // 2)
    colors = [
        [255,   0,   0],  # Đỏ (Red)
        [  0, 255,   0],  # Xanh lá (Green)
        [  0,   0, 255],  # Xanh dương (Blue)
        [255, 255,   0],  # Vàng (Yellow)
        [  0, 255, 255],  # Cyan
        [255,   0, 255],  # Magenta
        [255, 255, 255],  # Trắng (White)
        [  0,   0,   0],  # Đen (Black)
    ]
    
    half_h = height // 2
    block_w = width // len(colors)
    
    for idx, color in enumerate(colors):
        x_start = idx * block_w
        x_end = (idx + 1) * block_w if idx < len(colors) - 1 else width
        img_array[0:half_h, x_start:x_end] = color
        
    # Nửa dưới: Gradient màu đa dạng
    for y in range(half_h, height):
        for x in range(width):
            r = int((x / width) * 255)
            g = int(((y - half_h) / half_h) * 255)
            b = int(((x + (height - y)) / (width + half_h)) * 255)
            img_array[y, x] = [r, g, b]
            
    return img_array

def save_rgb_raw(img_array, output_raw_path="rgb.raw", preview_png_path="rgb_preview.png"):
    """
    Lưu mảng numpy (Height, Width, 3) thành file nhị phân rgb.raw (24 bit/pixel)
    Dữ liệu được ghi tuần tự từng pixel: [R, G, B, R, G, B, ...]
    """
    height, width, channels = img_array.shape
    assert channels == 3, "Ảnh phải có đúng 3 kênh màu (RGB)!"
    
    # Ghi dữ liệu thô (raw bytes)
    raw_bytes = img_array.tobytes()
    with open(output_raw_path, "wb") as f:
        f.write(raw_bytes)
        
    # Lưu thông tin kích thước vào file để Step 2 & 3 tự động nhận diện
    with open("image_dim.txt", "w") as f_dim:
        f_dim.write(f"{width} {height}")

    # Lưu file PNG preview để xem trước trên máy tính
    img = Image.fromarray(img_array, mode='RGB')
    img.save(preview_png_path)
    return width, height

if __name__ == "__main__":
    img_array = create_sample_rgb_image(512, 512)
    save_rgb_raw(img_array, "rgb.raw", "rgb_preview.png")
    print("Đã xong")

