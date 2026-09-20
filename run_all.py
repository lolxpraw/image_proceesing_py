"""
Chương trình chạy toàn bộ quy trình bài tập BT2:
Step 1: Tạo rgb.raw (24 bit/pixel)
Step 2: Chuyển rgb.raw -> gray.raw (8 bit/pixel) bằng Python (thay thế C)
Step 3: Chuyển gray.raw -> binary.raw (binary scale)
"""

import os
import sys

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi bảng mã (UnicodeEncodeError)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from step1_create_rgb_raw import create_sample_rgb_image, save_rgb_raw, convert_image_to_rgb_raw
from step2_rgb_to_gray import rgb_raw_to_gray_raw
from step3_gray_to_binary import gray_raw_to_binary_raw

def main():
    print("=" * 60)
    print(" BÀI TẬP 2 (BT2): XỬ LÝ ẢNH RAW BẰNG PYTHON (THAY THẾ C)")
    print("=" * 60)

    width = 512
    height = 512
    threshold = 128

    # Kiểm tra nếu người dùng truyền ảnh đầu vào tùy chọn
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        input_image = sys.argv[1]
        print(f"\n[1] STEP 1: Đang nạp ảnh đầu vào '{input_image}'...")
        width, height = convert_image_to_rgb_raw(input_image, "rgb.raw", "rgb_preview.png")
    else:
        print(f"\n[1] STEP 1: Đang tạo ảnh màu mẫu 512x512 (rgb.raw)...")
        img_array = create_sample_rgb_image(width, height)
        width, height = save_rgb_raw(img_array, "rgb.raw", "rgb_preview.png")

    print(f"\n[2] STEP 2: Chuyển rgb.raw -> gray.raw (8 bit/pixel bằng Python)...")
    rgb_raw_to_gray_raw("rgb.raw", "gray.raw", "gray_preview.png", width=width, height=height)

    print(f"\n[3] STEP 3: Chuyển gray.raw -> binary.raw (Ngưỡng T = {threshold})...")
    gray_raw_to_binary_raw("gray.raw", "binary.raw", "binary_preview.png", width=width, height=height, threshold=threshold)

    print("\n" + "=" * 60)
    print(" HOÀN THÀNH TẤT CẢ CÁC BƯỚC THÀNH CÔNG!")
    print("=" * 60)
    print("Các file RAW được tạo ra trong thư mục 'D:\\image processing':")
    for fname in ["rgb.raw", "gray.raw", "binary.raw", "rgb_preview.png", "gray_preview.png", "binary_preview.png"]:
        if os.path.exists(fname):
            sz = os.path.getsize(fname)
            print(f"  + {fname:<20} : {sz:,} bytes")
    print("=" * 60)

if __name__ == "__main__":
    main()

