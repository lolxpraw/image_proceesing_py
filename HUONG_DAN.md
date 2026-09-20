# Instructions: RAW Image Processing with Python (Assignment 2)

> Project directory: `D:\image processing`

---

## 1. File Overview

| File | Purpose |
| :--- | :--- |
| `step1_create_rgb_raw.py` | Generates 24-bit/pixel color image `rgb.raw` (3 bytes/pixel: R, G, B) |
| `step2_rgb_to_gray.py` | **Replaces C Program with Python**: Converts `rgb.raw` to 8-bit grayscale image `gray.raw` |
| `step3_gray_to_binary.py` | Converts `gray.raw` to binary scale image `binary.raw` |
| `run_all.py` | Automates all 3 steps in sequence |
| `README.md` | Standard project documentation for GitHub |
| `.gitignore` | Ignores `.raw`, `.png`, and Python cache files |

---

## 2. How to Run

Open your terminal (PowerShell or CMD) in `D:\image processing`:

### Method 1: Execute all steps with a single command (Recommended)
- **Using the synthetic 512x512 test image**:
  ```powershell
  python run_all.py
  ```
- **Using your custom image** (JPG, PNG, BMP,...):
  1. Copy your image into `D:\image processing` (e.g., `my_photo.jpg`).
  2. Run:
     ```powershell
     python run_all.py my_photo.jpg
     ```
     *(The program automatically detects original image dimensions, saves them to `image_dim.txt`, and processes all steps without requiring manual dimension parameters).*

### Method 2: Execute each step separately
```powershell
# Step 1: Create rgb.raw from test pattern or custom image
python step1_create_rgb_raw.py
# (Or with custom image: python step1_create_rgb_raw.py my_photo.jpg)

# Step 2: Convert to gray.raw (Automatically detects dimensions from Step 1)
python step2_rgb_to_gray.py

# Step 3: Convert to binary.raw (Automatically detects dimensions, optional threshold e.g. 128)
python step3_gray_to_binary.py
```

---

## 3. Opening & Verifying RAW Files in Adobe Photoshop

In Photoshop, choose **File -> Open As -> Photoshop Raw (*.RAW)**:

### A. For `rgb.raw` (Step 1):
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `3` (RGB Color)
- **Depth**: `8 Bits`
- **Interleaved**: Check `[x]`
- **Header**: `0` Bytes

### B. For `gray.raw` (Step 2):
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes

### C. For `binary.raw` (Step 3):
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes

---

## 4. Source Code Mapping: C vs. Python (For Reports / Viva)

| Task | C Language | Python (`step2_rgb_to_gray.py`) |
| :--- | :--- | :--- |
| **Open binary files** | `FILE *f_in = fopen("rgb.raw", "rb");`<br>`FILE *f_out = fopen("gray.raw", "wb");` | `with open("rgb.raw", "rb") as f_in:`<br>`with open("gray.raw", "wb") as f_out:` |
| **Allocate buffer** | `unsigned char *gray = malloc(W * H);` | `gray_buffer = bytearray(W * H)` |
| **Read raw data** | `fread(rgb, sizeof(unsigned char), 3, f_in);` | `r = raw_rgb[i*3]; g = raw_rgb[i*3+1]; b = raw_rgb[i*3+2]` |
| **Luminance formula** | `val = 0.299*r + 0.587*g + 0.114*b;` | `gray_val = int(0.299*r + 0.587*g + 0.114*b + 0.5)` |
| **Write raw bytes** | `fwrite(&val, sizeof(unsigned char), 1, f_out);` | `f_out.write(gray_buffer)` |
