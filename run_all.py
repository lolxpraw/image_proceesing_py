"""
Chương trình chạy toàn bộ bài tập BT2:
- Step 1: Python tạo rgb.raw (24 bit/pixel)
- Step 2: C program chuyển rgb.raw -> gray.raw (8 bit/pixel)
- Step 3: C program chuyển gray.raw -> binary.raw (binary scale)
"""

import os
import sys
import subprocess

# Cấu hình encoding utf-8 cho console Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from step1_create_rgb_raw import create_sample_rgb_image, save_rgb_raw, convert_image_to_rgb_raw

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
    print("=" * 65)
    print(" BÀI TẬP 2 (BT2): KẾT HỢP PYTHON (STEP 1) & C (STEP 2, STEP 3)")
    print("=" * 65)

    width = 512
    height = 512

    # 1. STEP 1: Python tạo rgb.raw
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        input_image = sys.argv[1]
        print(f"\n[1] STEP 1 (Python): Đang nạp ảnh '{input_image}' -> rgb.raw...")
        width, height = convert_image_to_rgb_raw(input_image, "rgb.raw", "rgb_preview.png")
    else:
        print(f"\n[1] STEP 1 (Python): Đang tạo ảnh màu mẫu 512x512 -> rgb.raw...")
        img_array = create_sample_rgb_image(512, 512)
        width, height = save_rgb_raw(img_array, "rgb.raw", "rgb_preview.png")

    # Biên dịch file C nếu cần
    if not compile_c_programs():
        return

    # 2. STEP 2: Chạy chương trình C chuyển rgb.raw -> gray.raw
    print(f"\n[2] STEP 2 (C Program): Đang chạy step2_rgb_to_gray.exe...")
    cmd_step2 = [".\\step2_rgb_to_gray.exe", str(width), str(height)]
    ret2 = subprocess.run(cmd_step2)
    if ret2.returncode != 0:
        print("[Lỗi] Chạy step2_rgb_to_gray.exe thất bại!")
        return

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
    print("=" * 65)
    print("Các file RAW trong thư mục 'D:\\image processing':")
    for fname in ["rgb.raw", "gray.raw", "binary.raw"]:
        if os.path.exists(fname):
            sz = os.path.getsize(fname)
            print(f"  + {fname:<15} : {sz:,} bytes")
    print("=" * 65)

if __name__ == "__main__":
    main()
