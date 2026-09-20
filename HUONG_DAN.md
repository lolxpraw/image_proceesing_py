# HƯỚNG DẪN BÀI TẬP 2 (BT2) - XỬ LÝ ẢNH RAW (PYTHON + C)

> Thư mục làm việc: `D:\image processing`

Theo đúng yêu cầu của đề bài:
- **Step 1 (Python)**: Tạo ảnh màu `rgb.raw` (24 bit/pixel).
- **Step 2 (C)**: Viết chương trình C chuyển từ `rgb.raw` -> `gray.raw` (8 bit/pixel).
- **Step 3 (C)**: Viết chương trình C chuyển từ `gray.raw` -> `binary.raw` (nhị phân hóa, 8 bit/pixel: 0 và 255).

---

## 1. Danh sách các file trong thư mục

| File | Ngôn ngữ | Vai trò |
| :--- | :--- | :--- |
| **`step1_create_rgb_raw.py`** | Python | Tạo file `rgb.raw` (tự động sinh ảnh màu mẫu hoặc chuyển từ ảnh JPG/PNG bất kỳ) |
| **`step2_rgb_to_gray.c`** | C | Đọc `rgb.raw`, tính mức xám $Y = 0.299R + 0.587G + 0.114B$, ghi ra `gray.raw` |
| **`step3_gray_to_binary.c`** | C | Đọc `gray.raw`, phân ngưỡng với $T = 128$, ghi ra `binary.raw` |
| **`run_all.py`** | Python | Script tự động chạy cả 3 bước (tự biên dịch C bằng `gcc` và chạy) |
| **`README.md`** | Markdown | Tài liệu tiếng Anh chuẩn để hiển thị trên GitHub |
| **`.gitignore`** | Git | Loại bỏ các file `.raw`, `.png`, file `.exe` đã biên dịch khỏi Git |

---

## 2. Cách biên dịch chương trình C bằng GCC

Nếu muốn tự biên dịch thủ công bằng dòng lệnh:

```powershell
# Biên dịch Step 2
gcc -O2 step2_rgb_to_gray.c -o step2_rgb_to_gray.exe

# Biên dịch Step 3
gcc -O2 step3_gray_to_binary.c -o step3_gray_to_binary.exe
```

---

## 3. Cách chạy chương trình

### Cách 1: Chạy tự động trọn gói (Khuyên dùng)
```powershell
# Dùng ảnh mẫu 512x512
python run_all.py

# Hoặc dùng ảnh của bạn:
python run_all.py my_photo.jpg
```

---

### Cách 2: Chạy từng bước độc lập

#### Bước 1 (Python):
```powershell
python step1_create_rgb_raw.py
# (Hoặc: python step1_create_rgb_raw.py my_photo.jpg)
```

#### Bước 2 (C):
```powershell
.\step2_rgb_to_gray.exe
```

#### Bước 3 (C):
```powershell
.\step3_gray_to_binary.exe
```

---

## 4. Kiểm tra trên Adobe Photoshop

Mở Photoshop: **File -> Open As -> Photoshop Raw (*.RAW)**:

- **`rgb.raw`**: Width & Height (ví dụ: `512` x `512`), Channels: `3`, Depth: `8 Bits`, Interleaved: `[x]`, Header: `0` Bytes.
- **`gray.raw`**: Width & Height (ví dụ: `512` x `512`), Channels: `1`, Depth: `8 Bits`, Header: `0` Bytes.
- **`binary.raw`**: Width & Height (ví dụ: `512` x `512`), Channels: `1`, Depth: `8 Bits`, Header: `0` Bytes.

---

## 5. Đẩy cập nhật lên GitHub

```powershell
git add step2_rgb_to_gray.c step3_gray_to_binary.c run_all.py README.md HUONG_DAN.md .gitignore
git commit -m "Update Step 2 and Step 3 to C implementation, remove py"
git push
```

