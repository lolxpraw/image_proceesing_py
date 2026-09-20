# HƯỚNG DẪN BÀI TẬP 2 (BT2) - XỬ LÝ ẢNH RAW BẰNG PYTHON

> Toàn bộ mã nguồn và dữ liệu đã được đặt tại: `D:\image processing`

---

## 1. Danh sách các file trong thư mục

| Tên File | Vai trò |
| :--- | :--- |
| `step1_create_rgb_raw.py` | Tạo file ảnh màu `rgb.raw` (24 bit/pixel = 3 byte/pixel) |
| `step2_rgb_to_gray.py` | **Chuyển từ C sang Python**: Chuyển `rgb.raw` thành ảnh xám `gray.raw` (8 bit/pixel) |
| `step3_gray_to_binary.py` | Chuyển ảnh xám `gray.raw` sang ảnh nhị phân `binary.raw` (Binary scale) |
| `run_all.py` | Chạy tự động cả 3 bước một cách liền mạch |
| `rgb.raw` | File RAW màu RGB (Dung lượng: 786,432 bytes) |
| `gray.raw` | File RAW ảnh xám (Dung lượng: 262,144 bytes) |
| `binary.raw` | File RAW nhị phân (Dung lượng: 262,144 bytes) |
| `*.png` | Ảnh xem trước (preview) để bạn mở xem trực tiếp mà chưa cần bật Photoshop |

---

## 2. Cách chạy chương trình bằng Python

Mở terminal (PowerShell hoặc CMD) tại thư mục `D:\image processing`:

### Cách 1: Chạy tất cả các bước chỉ với 1 lệnh
- **Dùng ảnh mẫu tự sinh (512x512)**:
  ```powershell
  python run_all.py
  ```
- **Dùng một bức ảnh bất kỳ của bạn** (JPG, PNG, BMP,...):
  1. Copy file ảnh vào thư mục `D:\image processing` (ví dụ file tên `anh_cua_toi.jpg`).
  2. Chạy lệnh:
     ```powershell
     python run_all.py anh_cua_toi.jpg
     ```
     *(Chương trình sẽ tự động lấy kích thước ảnh gốc, lưu vào `image_dim.txt` và chuyển qua tất cả các bước Step 1 -> 2 -> 3 mà bạn không cần tính toán hay gõ lại kích thước!)*

### Cách 2: Chạy từng bước riêng biệt
```powershell
# Bước 1: Tạo rgb.raw từ ảnh của bạn
python step1_create_rgb_raw.py anh_cua_toi.jpg

# Bước 2: Chuyển sang gray.raw (Tự động nhận diện kích thước từ ảnh ở Bước 1)
python step2_rgb_to_gray.py

# Bước 3: Chuyển sang binary.raw (Tự động nhận diện kích thước, có thể chỉ định ngưỡng tùy chọn ví dụ 128)
python step3_gray_to_binary.py
```

---

## 3. Hướng dẫn mở và kiểm tra file RAW trên Adobe Photoshop

File `.raw` (Photoshop Raw) là dữ liệu nhị phân thô không có header, do đó Photoshop sẽ yêu cầu bạn nhập các thông số hình học và kênh màu. Khi mở, hãy chọn định dạng **Photoshop Raw**:

### A. Mở file `rgb.raw` (Step 1):
Vào Photoshop: **File -> Open As -> Photoshop Raw (*.RAW)**, chọn `rgb.raw`:
- **Width**: `512` Pixels
- **Height**: `512` Pixels
- **Channels**: `3` (RGB Color)
- **Depth**: `8 Bits`
- **Interleaved**: Đánh dấu tích chọn `[x]` (vì lưu xen kẽ R, G, B liên tục)
- **Header**: `0` Bytes

### B. Mở file `gray.raw` (Step 2):
Vào Photoshop: **File -> Open As -> Photoshop Raw (*.RAW)**, chọn `gray.raw`:
- **Width**: `512` Pixels
- **Height**: `512` Pixels
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes

### C. Mở file `binary.raw` (Step 3):
Vào Photoshop: **File -> Open As -> Photoshop Raw (*.RAW)**, chọn `binary.raw`:
- **Width**: `512` Pixels
- **Height**: `512` Pixels
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes

---

## 4. Đối chiếu mã nguồn C và Python (Dành cho báo cáo / vấn đáp)

Khi thầy cô yêu cầu giải thích việc chuyển đổi từ C sang Python ở Step 2, bạn có thể trình bày bảng đối chiếu logic 1:1 này:

| Thao tác | Mã nguồn C | Mã nguồn Python (`step2_rgb_to_gray.py`) |
| :--- | :--- | :--- |
| **Mở file nhị phân** | `FILE *f_in = fopen("rgb.raw", "rb");`<br>`FILE *f_out = fopen("gray.raw", "wb");` | `with open("rgb.raw", "rb") as f_in:`<br>`with open("gray.raw", "wb") as f_out:` |
| **Cấp phát bộ nhớ đệm** | `unsigned char *gray = malloc(W * H);` | `gray_buffer = bytearray(W * H)` |
| **Đọc dữ liệu** | `fread(rgb, sizeof(unsigned char), 3, f_in);` | `r = raw_rgb[i*3]; g = raw_rgb[i*3+1]; b = raw_rgb[i*3+2]` |
| **Công thức Luminance** | `val = 0.299*r + 0.587*g + 0.114*b;` | `gray_val = int(0.299*r + 0.587*g + 0.114*b + 0.5)` |
| **Ghi ra file RAW** | `fwrite(&val, sizeof(unsigned char), 1, f_out);` | `f_out.write(gray_buffer)` |

