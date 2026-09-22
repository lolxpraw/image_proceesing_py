/**
 * Step 3: Directional edge-based feature representation algorithm (Yamasaki & Shibata)
 * 
 * File dau vao: gray.raw (8 bit/pixel, Width x Height bytes)
 * File dau ra:  
 *   - binary.raw: Tong hop tat ca cac canh (0: canh, 255: nen)
 *   - edge_H.raw: Ban do canh huong Horizontal (FH)
 *   - edge_P.raw: Ban do canh huong +45 degree (FP)
 *   - edge_V.raw: Ban do canh huong Vertical (FV)
 *   - edge_M.raw: Ban do canh huong -45 degree (FM)
 * 
 * Thuat toan:
 *   1. Ap dung 4 kernel dinh huong 5x5: Horizontal, +45 deg, Vertical, -45 deg.
 *   2. Tinh tri tuyet doi cac dap ung: AH, AP, AV, AM.
 *   3. Tinh nguong cuc bo (Median Value): Trung vi cua 40 sai khac tuyet doi lan can.
 *   4. Winner-Take-All: Chon huong co dap ung lon nhat A_max.
 *   5. Thresholding: Neu A_max > Median thi pixel duoc gan huong canh tuong ung.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Lay gia tri pixel co clamp bien anh
static inline int get_pixel(const unsigned char *img, int w, int h, int x, int y) {
    if (x < 0) x = 0;
    else if (x >= w) x = w - 1;
    if (y < 0) y = 0;
    else if (y >= h) y = h - 1;
    return img[y * w + x];
}

// 4 Bo loc dinh huong 5x5 theo dung so do
static const int KH[5][5] = {
    { 0,  0,  0,  0,  0},
    { 1,  1,  1,  1,  1},
    { 0,  0,  0,  0,  0},
    {-1, -1, -1, -1, -1},
    { 0,  0,  0,  0,  0}
};

static const int KV[5][5] = {
    { 0,  1,  0, -1,  0},
    { 0,  1,  0, -1,  0},
    { 0,  1,  0, -1,  0},
    { 0,  1,  0, -1,  0},
    { 0,  1,  0, -1,  0}
};

static const int KP[5][5] = {
    { 0,  0,  0,  1,  0},
    { 0,  1,  1,  0, -1},
    { 0,  1,  0, -1,  0},
    { 1,  0, -1, -1,  0},
    { 0, -1,  0,  0,  0}
};

static const int KM[5][5] = {
    { 0, -1,  0,  0,  0},
    { 1,  0, -1, -1,  0},
    { 0,  1,  0, -1,  0},
    { 0,  1,  1,  0, -1},
    { 0,  0,  0,  1,  0}
};

int main(int argc, char *argv[]) {
    int width = 512;
    int height = 512;

    // 1. Doc kich thuoc anh tu tham so hoac file image_dim.txt
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

    const char *input_path = "gray.raw";
    FILE *f_in = fopen(input_path, "rb");
    if (f_in == NULL) {
        printf("[Loi] Khong the mo file '%s'!\n", input_path);
        return 1;
    }

    int total_pixels = width * height;
    unsigned char *gray = (unsigned char *)malloc(total_pixels);
    if (gray == NULL) {
        printf("[Loi] Khong du bo nho RAM!\n");
        fclose(f_in);
        return 1;
    }

    fread(gray, 1, total_pixels, f_in);
    fclose(f_in);

    // Cap phat cac buffer ket qua (Mac dinh khoi tao 255: nen trang nhu hinh Fig. 1)
    unsigned char *bin_comb = (unsigned char *)malloc(total_pixels);
    unsigned char *edge_H   = (unsigned char *)malloc(total_pixels);
    unsigned char *edge_P   = (unsigned char *)malloc(total_pixels);
    unsigned char *edge_V   = (unsigned char *)malloc(total_pixels);
    unsigned char *edge_M   = (unsigned char *)malloc(total_pixels);

    for (int i = 0; i < total_pixels; i++) {
        bin_comb[i] = 255;
        edge_H[i]   = 255;
        edge_P[i]   = 255;
        edge_V[i]   = 255;
        edge_M[i]   = 255;
    }

    int win[5][5];
    int diffs[40];

    // Duyet qua tung pixel cua anh
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int idx = y * width + x;

            // Lay cua so 5x5
            for (int r = -2; r <= 2; r++) {
                for (int c = -2; c <= 2; c++) {
                    win[r + 2][c + 2] = get_pixel(gray, width, height, x + c, y + r);
                }
            }

            // Tinh 4 tich chap dinh huong
            int sum_H = 0, sum_P = 0, sum_V = 0, sum_M = 0;
            for (int r = 0; r < 5; r++) {
                for (int c = 0; c < 5; c++) {
                    int val = win[r][c];
                    sum_H += val * KH[r][c];
                    sum_P += val * KP[r][c];
                    sum_V += val * KV[r][c];
                    sum_M += val * KM[r][c];
                }
            }

            int AH = abs(sum_H);
            int AP = abs(sum_P);
            int AV = abs(sum_V);
            int AM = abs(sum_M);

            // Tinh 40 sai khac tuyet doi lan can (20 ngang + 20 doc)
            int d_idx = 0;
            for (int r = 0; r < 5; r++) {
                for (int c = 0; c < 4; c++) {
                    diffs[d_idx++] = abs(win[r][c + 1] - win[r][c]);
                }
            }
            for (int r = 0; r < 4; r++) {
                for (int c = 0; c < 5; c++) {
                    diffs[d_idx++] = abs(win[r + 1][c] - win[r][c]);
                }
            }

            // Sap xep 40 gia tri de tim Median Value
            for (int i = 1; i < 40; i++) {
                int key = diffs[i];
                int j = i - 1;
                while (j >= 0 && diffs[j] > key) {
                    diffs[j + 1] = diffs[j];
                    j--;
                }
                diffs[j + 1] = key;
            }
            int T_med = (diffs[19] + diffs[20]) / 2;

            // Winner-Take-All: Tim gia tri lon nhat va huong thang cuoc
            int A_max = AH;
            int winner = 0; // 0: H, 1: P, 2: V, 3: M
            if (AP > A_max) { A_max = AP; winner = 1; }
            if (AV > A_max) { A_max = AV; winner = 2; }
            if (AM > A_max) { A_max = AM; winner = 3; }

            // Thresholding: So sanh A_max voi Median Value
            if (A_max > T_med && A_max > 5) {
                // Diem canh mau den (0) tren nen trang (255) dung theo hinh Fig. 1
                bin_comb[idx] = 0;
                if (winner == 0) edge_H[idx] = 0;
                else if (winner == 1) edge_P[idx] = 0;
                else if (winner == 2) edge_V[idx] = 0;
                else if (winner == 3) edge_M[idx] = 0;
            }
        }
    }

    // Ghi cac file ket qua
    FILE *f_bin = fopen("binary.raw", "wb");
    if (f_bin) { fwrite(bin_comb, 1, total_pixels, f_bin); fclose(f_bin); }

    FILE *f_h = fopen("edge_H.raw", "wb");
    if (f_h) { fwrite(edge_H, 1, total_pixels, f_h); fclose(f_h); }

    FILE *f_p = fopen("edge_P.raw", "wb");
    if (f_p) { fwrite(edge_P, 1, total_pixels, f_p); fclose(f_p); }

    FILE *f_v = fopen("edge_V.raw", "wb");
    if (f_v) { fwrite(edge_V, 1, total_pixels, f_v); fclose(f_v); }

    FILE *f_m = fopen("edge_M.raw", "wb");
    if (f_m) { fwrite(edge_M, 1, total_pixels, f_m); fclose(f_m); }

    // Giai phong bo nho
    free(gray);
    free(bin_comb);
    free(edge_H);
    free(edge_P);
    free(edge_V);
    free(edge_M);

    printf("Đã xong\n");
    return 0;
}
