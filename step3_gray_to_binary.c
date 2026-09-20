/**
 * Step 3: Chuyen anh xam gray.raw -> binary.raw (Binary scale) bang C
 * 
 * File dau vao: gray.raw (8 bit/pixel, kich thuoc: Width x Height bytes)
 * File dau ra:  binary.raw (8 bit/pixel: diem anh mang gia tri 0 hoac 255)
 * 
 * Nguyen ly phan nguong (Thresholding):
 *   Neu Gray >= Threshold: Pixel = 255 (Trang)
 *   Nguoc lai:              Pixel = 0   (Den)
 * 
 * Mac dinh Threshold = 128.
 * 
 * Cach bien dich (Compile):
 *   gcc -O2 step3_gray_to_binary.c -o step3_gray_to_binary.exe
 * 
 * Cach chay (Run):
 *   .\step3_gray_to_binary.exe [threshold] [width] [height]
 *   (Neu khong truyen tham so, mac dinh Threshold=128, kich thuoc tu doc image_dim.txt hoac 512x512)
 */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int threshold = 128;
    int width = 512;
    int height = 512;

    // 1. Doc tham so dong lenh hoac file image_dim.txt
    if (argc >= 2) {
        threshold = atoi(argv[1]);
    }
    if (argc >= 4) {
        width = atoi(argv[2]);
        height = atoi(argv[3]);
    } else {
        FILE *f_dim = fopen("image_dim.txt", "r");
        if (f_dim != NULL) {
            if (fscanf(f_dim, "%d %d", &width, &height) == 2) {
                printf("[Step 3 - C] Tu dong nhan dien kich thuoc tu image_dim.txt: %d x %d\n", width, height);
            }
            fclose(f_dim);
        }
    }

    const char *input_path = "gray.raw";
    const char *output_path = "binary.raw";

    // 2. Mo file gray.raw o che do doc nhi phan
    FILE *f_in = fopen(input_path, "rb");
    if (f_in == NULL) {
        printf("[Loi] Khong the mo file '%s'! Hay kiem tra file co ton tai khong.\n", input_path);
        return 1;
    }

    // 3. Mo file binary.raw o che do ghi nhi phan
    FILE *f_out = fopen(output_path, "wb");
    if (f_out == NULL) {
        printf("[Loi] Khong the tao file '%s' de ghi!\n", output_path);
        fclose(f_in);
        return 1;
    }

    int total_pixels = width * height;
    printf("[Step 3 - C] Dang doc '%s' (Nguong T = %d)...\n", input_path, threshold);

    // Cap phat bo nho dem cho anh xam va anh nhi phan
    unsigned char *gray_buf = (unsigned char *)malloc(total_pixels);
    unsigned char *bin_buf = (unsigned char *)malloc(total_pixels);

    if (gray_buf == NULL || bin_buf == NULL) {
        printf("[Loi] Khong du bo nho RAM!\n");
        if (gray_buf) free(gray_buf);
        if (bin_buf) free(bin_buf);
        fclose(f_in);
        fclose(f_out);
        return 1;
    }

    // 4. Doc toan bo du lieu anh xam
    size_t bytes_read = fread(gray_buf, 1, total_pixels, f_in);
    if (bytes_read != (size_t)total_pixels) {
        printf("[Canh bao] So byte doc duoc (%zu) khac voi du kien (%d)!\n", bytes_read, total_pixels);
    }

    // 5. Phan nguong tung pixel
    for (int i = 0; i < total_pixels; i++) {
        if (gray_buf[i] >= threshold) {
            bin_buf[i] = 255; // Diem sang (Trang)
        } else {
            bin_buf[i] = 0;   // Diem toi (Den)
        }
    }

    // 6. Ghi ket qua ra file binary.raw
    size_t bytes_written = fwrite(bin_buf, 1, total_pixels, f_out);
    if (bytes_written != (size_t)total_pixels) {
        printf("[Canh bao] So byte ghi duoc (%zu) khac voi du kien (%d)!\n", bytes_written, total_pixels);
    }

    // 7. Giai phong bo nho va dong file
    free(gray_buf);
    free(bin_buf);
    fclose(f_in);
    fclose(f_out);

    printf("[Step 3 - C] Da tao thanh cong file: '%s'\n", output_path);
    printf("             - Kich thuoc: %d x %d\n", width, height);
    printf("             - Phan nguong: Threshold = %d\n", threshold);
    printf("             - Gia tri pixel: 0 (den) va 255 (trang)\n");
    printf("             - Dung luong: %d bytes\n", total_pixels);

    return 0;
}

