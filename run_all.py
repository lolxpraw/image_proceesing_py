"""
Chương trình chạy toàn bộ bài tập BT2:
- Step 1: Python tạo rgb.raw (24 bit/pixel)
- Step 2: C program chuyển rgb.raw -> gray.raw (8 bit/pixel)
- Step 3: C program thuật toán Directional edge-based feature representation
          -> Sinh ra binary.raw và 4 bản đồ hướng cạnh: edge_H, edge_P, edge_V, edge_M
- Xuất ảnh tổng hợp directional_summary.png mô phỏng đúng Fig. 1 trong tài liệu nghiên cứu.
"""

import os
import sys
import subprocess
import numpy as np
from PIL import Image

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
            ret = subprocess.run(["gcc", "-O2", src, "-o", exe])
            if ret.returncode != 0:
                print(f"[Lỗi] Biên dịch thất bại cho {src}!")
                return False
    return True

def export_edge_previews(width, height):
    """Xuất các ảnh xem trước PNG cho các bản đồ hướng cạnh và ảnh tổng hợp Fig. 1"""
    maps = {}
    filenames = [
        ("gray.raw", "gray_preview.png"),
        ("binary.raw", "binary_preview.png"),
        ("edge_H.raw", "edge_H.png"),
        ("edge_P.raw", "edge_P.png"),
        ("edge_V.raw", "edge_V.png"),
        ("edge_M.raw", "edge_M.png")
    ]
    for raw_f, png_f in filenames:
        if os.path.exists(raw_f):
            with open(raw_f, "rb") as f:
                data = f.read(width * height)
                arr = np.frombuffer(data, dtype=np.uint8).reshape((height, width))
                img = Image.fromarray(arr, mode='L')
                img.save(png_f)
                maps[raw_f] = img

    # Tạo ảnh ghép so sánh đúng theo Fig. 1:
    # [Input image] -> [Horizontal FH] [+45 degree FP] [Vertical FV] [-45 degree FM]
    if "gray.raw" in maps and "edge_H.raw" in maps and "edge_P.raw" in maps and "edge_V.raw" in maps and "edge_M.raw" in maps:
        thumb_size = 160
        gap = 16
        total_w = thumb_size * 5 + gap * 6
        total_h = thumb_size + 60
        summary_img = Image.new('RGB', (total_w, total_h), color=(255, 255, 255))

        images_to_show = [
            (maps["gray.raw"], "Input Image"),
            (maps["edge_H.raw"], "Horizontal (FH)"),
            (maps["edge_P.raw"], "+45 deg (FP)"),
            (maps["edge_V.raw"], "Vertical (FV)"),
            (maps["edge_M.raw"], "-45 deg (FM)")
        ]

        for i, (im, label) in enumerate(images_to_show):
            resized = im.resize((thumb_size, thumb_size))
            x_pos = gap + i * (thumb_size + gap)
            summary_img.paste(resized.convert('RGB'), (x_pos, 20))

        summary_img.save("directional_summary.png")

def main():
    width = 512
    height = 512

    # 1. STEP 1: Đọc ảnh ngoài (nếu có) hoặc tạo ảnh màu mẫu 512x512
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        width, height = convert_image_to_rgb_raw(sys.argv[1], "rgb.raw", "rgb_preview.png")
    else:
        img_array = create_sample_rgb_image(512, 512)
        width, height = save_rgb_raw(img_array, "rgb.raw", "rgb_preview.png")

    # Biên dịch file C nếu cần
    if not compile_c_programs():
        return

    # 2. STEP 2: Chạy chương trình C chuyển rgb.raw -> gray.raw
    cmd_step2 = [".\\step2_rgb_to_gray.exe", str(width), str(height)]
    ret2 = subprocess.run(cmd_step2, stdout=subprocess.DEVNULL)
    if ret2.returncode != 0:
        return

    # 3. STEP 3: Chạy chương trình C thuật toán Directional Edge Feature Representation
    cmd_step3 = [".\\step3_gray_to_binary.exe", str(width), str(height)]
    ret3 = subprocess.run(cmd_step3, stdout=subprocess.DEVNULL)
    if ret3.returncode != 0:
        return

    # Xuất ảnh xem trước
    export_edge_previews(width, height)
    print("Đã xong")

if __name__ == "__main__":
    main()