/**
 * Step 2: Chuyen doi tu RGB.raw -> gray.raw (8 bit/pixel) bang C
 * 
 * File dau vao: rgb.raw (24 bit/pixel, kich thuoc: Width x Height x 3 bytes)
 * File dau ra:  gray.raw (8 bit/pixel, kich thuoc: Width x Height bytes)
 * 
 * Cong thuc tinh muc xam (Standard Luminance ITU-R BT.601):
 *   Gray = round(0.299 * R + 0.587 * G + 0.114 * B)
 * 
 * Cach bien dich (Compile):
 *   gcc -O2 step2_rgb_to_gray.c -o step2_rgb_to_gray.exe
 * 
 * Cach chay (Run):
 *   .\step2_rgb_to_gray.exe [width] [height]
 *   (Neu khong truyen tham so, mac dinh se tu doc image_dim.txt hoac lay 512x512)
 */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int width = 512;
    int height = 512;

    // 1. Kiem tra tham so dong lenh hoac doc tu file image_dim.txt
    if (argc >= 3) {
        width = atoi(argv[1]);
        height = atoi(argv[2]);
    } else {
        FILE *f_dim = fopen("image_dim.txt", "r");
        if (f_dim != NULL) {
            fscanf(f_dim, "%d %d", &width, &height);
            fclose(f_dim);
        }
    }

    const char *input_path = "rgb.raw";
    const char *output_path = "gray.raw";

    // 2. Mo file dau vao rgb.raw o che do doc nhi phan ("rb")
    FILE *f_in = fopen(input_path, "rb");
    if (f_in == NULL) {
        printf("[Loi] Khong the mo file '%s'! Hay kiem tra file co ton tai khong.\n", input_path);
        return 1;
    }

    // 3. Mo file dau ra gray.raw o che do ghi nhi phan ("wb")
    FILE *f_out = fopen(output_path, "wb");
    if (f_out == NULL) {
        printf("[Loi] Khong the tao file '%s' de ghi!\n", output_path);
        fclose(f_in);
        return 1;
    }

    int total_pixels = width * height;

    // Cấp phát bộ nhớ đệm cho dữ liệu ảnh
    // Mỗi pixel RGB có 3 byte (R, G, B)
    size_t rgb_size = (size_t)total_pixels * 3;
    unsigned char *rgb_buf = (unsigned char *)malloc(rgb_size);
    unsigned char *gray_buf = (unsigned char *)malloc(total_pixels);

    if (rgb_buf == NULL || gray_buf == NULL) {
        printf("[Loi] Khong du bo nho RAM de cap phat buffer!\n");
        if (rgb_buf) free(rgb_buf);
        if (gray_buf) free(gray_buf);
        fclose(f_in);
        fclose(f_out);
        return 1;
    }

    // 4. Doc toan bo du lieu RGB vao buffer
    fread(rgb_buf, 1, rgb_size, f_in);

    // 5. Duyet qua tung pixel va tinh gia tri muc xam
    for (int i = 0; i < total_pixels; i++) {
        unsigned char r = rgb_buf[i * 3];
        unsigned char g = rgb_buf[i * 3 + 1];
        unsigned char b = rgb_buf[i * 3 + 2];

        // Tinh muc xam theo cong thuc Luminance BT.601 (+0.5f de lam tron)
        int gray_val = (int)(0.299f * r + 0.587f * g + 0.114f * b + 0.5f);

        // Clamp gia tri trong khoang [0, 255]
        if (gray_val > 255) gray_val = 255;
        if (gray_val < 0) gray_val = 0;

        gray_buf[i] = (unsigned char)gray_val;
    }

    // 6. Ghi du lieu anh xam vao file gray.raw
    fwrite(gray_buf, 1, total_pixels, f_out);

    // 7. Giai phong bo nho va dong file
    free(rgb_buf);
    free(gray_buf);
    fclose(f_in);
    fclose(f_out);

    printf("Đã xong\n");
    return 0;
}

