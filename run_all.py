"""
Chương trình chạy toàn bộ quy trình bài tập BT2:
Step 1: Tạo rgb.raw (24 bit/pixel)
Step 2: Chuyển rgb.raw -> gray.raw (8 bit/pixel) bằng Python (thay thế C)
Step 3: Chuyển gray.raw -> binary.raw (binary scale)
Chương trình chạy toàn bộ bài tập BT2:
- Step 1: Python tạo rgb.raw (24 bit/pixel)
- Step 2: C program chuyển rgb.raw -> gray.raw (8 bit/pixel)
- Step 3: C program chuyển gray.raw -> binary.raw (binary scale)
"""

import os
import sys
import subprocess

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi bảng mã (UnicodeEncodeError)
# Cấu hình encoding utf-8 cho console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from step1_create_rgb_raw import create_sample_rgb_image, save_rgb_raw, convert_image_to_rgb_raw
from step2_rgb_to_gray import rgb_raw_to_gray_raw
from step3_gray_to_binary import gray_raw_to_binary_raw

def compile_c_programs():
    """Tự động biên dịch mã nguồn C nếu chưa có file .exe hoặc file .c mới hơn .exe"""
    c_files = [
        ("step2_rgb_to_gray.c", "step2_rgb_to_gray.exe"),
        ("step3_gray_to_binary.c", "step3_gray_to_binary.exe")
    ]
    for src, exe in c_files:
        need_compile = False
        if not os.path.exists(exe):
            need_compile = True
        elif os.path.getmtime(src) > os.path.getmtime(exe):
            need_compile = True

        if need_compile:
            print(f"[Biên dịch] Đang biên dịch {src} bằng gcc...")
            ret = subprocess.run(["gcc", "-O2", src, "-o", exe])
            if ret.returncode != 0:
                print(f"[Lỗi] Biên dịch thất bại cho {src}!")
                return False
    return True

def main():
    print("=" * 60)
    print(" BÀI TẬP 2 (BT2): XỬ LÝ ẢNH RAW BẰNG PYTHON (THAY THẾ C)")
    print("=" * 60)
    print("=" * 65)
    print(" BÀI TẬP 2 (BT2): KẾT HỢP PYTHON (STEP 1) & C (STEP 2, STEP 3)")
    print("=" * 65)

    width = 512
    height = 512
    threshold = 128

    # Kiểm tra nếu người dùng truyền ảnh đầu vào tùy chọn
    # 1. STEP 1: Python tạo rgb.raw
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        input_image = sys.argv[1]
        print(f"\n[1] STEP 1: Đang nạp ảnh đầu vào '{input_image}'...")
        print(f"\n[1] STEP 1 (Python): Đang nạp ảnh '{input_image}' -> rgb.raw...")
        width, height = convert_image_to_rgb_raw(input_image, "rgb.raw", "rgb_preview.png")
    else:
        print(f"\n[1] STEP 1: Đang tạo ảnh màu mẫu 512x512 (rgb.raw)...")
        img_array = create_sample_rgb_image(width, height)
        print(f"\n[1] STEP 1 (Python): Đang tạo ảnh màu mẫu 512x512 -> rgb.raw...")
        img_array = create_sample_rgb_image(512, 512)
        width, height = save_rgb_raw(img_array, "rgb.raw", "rgb_preview.png")

    print(f"\n[2] STEP 2: Chuyển rgb.raw -> gray.raw (8 bit/pixel bằng Python)...")
    rgb_raw_to_gray_raw("rgb.raw", "gray.raw", "gray_preview.png", width=width, height=height)
    # Biên dịch file C nếu cần
    if not compile_c_programs():
        return

    print(f"\n[3] STEP 3: Chuyển gray.raw -> binary.raw (Ngưỡng T = {threshold})...")
    gray_raw_to_binary_raw("gray.raw", "binary.raw", "binary_preview.png", width=width, height=height, threshold=threshold)
    # 2. STEP 2: Chạy chương trình C chuyển rgb.raw -> gray.raw
    print(f"\n[2] STEP 2 (C Program): Đang chạy step2_rgb_to_gray.exe...")
    cmd_step2 = [".\\step2_rgb_to_gray.exe", str(width), str(height)]
    ret2 = subprocess.run(cmd_step2)
    if ret2.returncode != 0:
        print("[Lỗi] Chạy step2_rgb_to_gray.exe thất bại!")
        return

    print("\n" + "=" * 60)
    # 3. STEP 3: Chạy chương trình C chuyển gray.raw -> binary.raw
    threshold = 128
    print(f"\n[3] STEP 3 (C Program): Đang chạy step3_gray_to_binary.exe (Threshold = {threshold})...")
    cmd_step3 = [".\\step3_gray_to_binary.exe", str(threshold), str(width), str(height)]
    ret3 = subprocess.run(cmd_step3)
    if ret3.returncode != 0:
        print("[Lỗi] Chạy step3_gray_to_binary.exe thất bại!")
        return

    print("\n" + "=" * 65)
    print(" HOÀN THÀNH TẤT CẢ CÁC BƯỚC THÀNH CÔNG!")
    print("=" * 60)
    print("Các file RAW được tạo ra trong thư mục 'D:\\image processing':")
    for fname in ["rgb.raw", "gray.raw", "binary.raw", "rgb_preview.png", "gray_preview.png", "binary_preview.png"]:
    print("=" * 65)
    print("Các file RAW trong thư mục 'D:\\image processing':")
    for fname in ["rgb.raw", "gray.raw", "binary.raw"]:
        if os.path.exists(fname):
            sz = os.path.getsize(fname)
            print(f"  + {fname:<20} : {sz:,} bytes")
    print("=" * 60)
            print(f"  + {fname:<15} : {sz:,} bytes")
    print("=" * 65)

if __name__ == "__main__":
    main()

