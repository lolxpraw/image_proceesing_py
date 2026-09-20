# Digital Image Processing: RAW Image Processing with Python

This project provides a complete Python implementation for reading, creating, and processing uncompressed RAW raster images (24-bit RGB, 8-bit Grayscale, and Binary Scale). It replaces traditional low-level C programs (`fread`, `fwrite`, byte pointer manipulation) with clean, high-performance Python implementations while maintaining 1:1 algorithmic and binary equivalency.

---

## 1. Project Structure

| File | Description |
| :--- | :--- |
| **`step1_create_rgb_raw.py`** | **Step 1**: Generates an interleaved 24-bit/pixel RGB raw file (`rgb.raw`). Supports both synthetic color pattern generation and conversion from arbitrary image formats (`.jpg`, `.png`, `.bmp`). |
| **`step2_rgb_to_gray.py`** | **Step 2 (Replaces C program)**: Reads binary bytes from `rgb.raw`, calculates luminance grayscale values using standard ITU-R BT.601 formula, and outputs `gray.raw` (8 bits/pixel). |
| **`step3_gray_to_binary.py`** | **Step 3**: Reads `gray.raw` and applies thresholding ($T = 128$) to produce a binary scale image `binary.raw` (values 0 and 255). |
| **`run_all.py`** | Pipeline runner to execute Step 1, Step 2, and Step 3 seamlessly with a single command. |
| **`.gitignore`** | Excludes generated `.raw` binary files, `.png` previews, and Python cache from Git tracking. |

---

## 2. Requirements & Installation

- Python 3.8+
- Required packages:
  ```bash
  pip install pillow numpy
  ```

---

## 3. How to Run

Open your terminal (PowerShell, Command Prompt, or Bash) in the project directory:

### Option A: Run the entire pipeline in one command (Recommended)

- **Using the built-in synthetic test image ($512 \times 512$)**:
  ```bash
  python run_all.py
  ```

- **Using your own custom image** (e.g. `my_image.jpg`):
  ```bash
  python run_all.py my_image.jpg
  ```
  > **Note**: The script automatically inspects the image dimensions ($W \times H$), saves them to `image_dim.txt`, and propagates them across all steps without requiring manual dimension arguments.

---

### Option B: Run each step individually

```bash
# Step 1: Create rgb.raw from test pattern or custom image
python step1_create_rgb_raw.py
# (Or: python step1_create_rgb_raw.py my_image.jpg)

# Step 2: Convert rgb.raw to gray.raw (8-bit grayscale)
python step2_rgb_to_gray.py

# Step 3: Convert gray.raw to binary.raw (Binary scale, default threshold = 128)
python step3_gray_to_binary.py
```

---

## 4. Opening & Verifying RAW Files in Adobe Photoshop

Uncompressed raster `.raw` files do not contain file headers. When opening them in Adobe Photoshop (**File -> Open As -> Photoshop Raw (*.RAW)**), configure the dialog as follows:

### A. `rgb.raw` (Step 1)
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `3` (RGB Color)
- **Depth**: `8 Bits`
- **Interleaved**: Checked `[x]` (Stores sequential R, G, B triplets per pixel)
- **Header**: `0` Bytes

### B. `gray.raw` (Step 2)
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes

### C. `binary.raw` (Step 3)
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes

---

## 5. Technical Comparison: C vs. Python Implementation

For academic presentations, lab reports, or viva examinations, this table outlines the direct 1:1 mapping between the traditional C implementation and our Python implementation:

| Operation | C Implementation | Python Implementation (`step2_rgb_to_gray.py`) |
| :--- | :--- | :--- |
| **Binary File I/O** | `FILE *f = fopen("rgb.raw", "rb");` | `with open("rgb.raw", "rb") as f:` |
| **Buffer Allocation** | `unsigned char *buf = malloc(W * H);` | `gray_buffer = bytearray(W * H)` |
| **Byte Reading** | `fread(rgb, sizeof(unsigned char), 3, f);` | `r = raw_rgb[i*3]; g = raw_rgb[i*3+1]; b = raw_rgb[i*3+2]` |
| **Luminance Formula** | `gray = (unsigned char)(0.299*r + 0.587*g + 0.114*b);` | `gray = int(0.299*r + 0.587*g + 0.114*b + 0.5)` |
| **Writing RAW Data** | `fwrite(&gray, sizeof(unsigned char), 1, f_out);` | `f_out.write(gray_buffer)` |

---

## 6. Output Verification & File Sizes

| Output File | Dimensions | Data Type | Formula / Rule | Expected Size ($512 \times 512$) |
| :--- | :--- | :--- | :--- | :--- |
| `rgb.raw` | $W \times H$ | 24-bit RGB (3 bytes/px) | Interleaved [R, G, B] | $512 \times 512 \times 3 = 786,432$ bytes |
| `gray.raw` | $W \times H$ | 8-bit Gray (1 byte/px) | $Y = 0.299R + 0.587G + 0.114B$ | $512 \times 512 \times 1 = 262,144$ bytes |
| `binary.raw`| $W \times H$ | 8-bit Binary (1 byte/px) | $P = 255 \text{ if } Y \ge 128 \text{ else } 0$ | $512 \times 512 \times 1 = 262,144$ bytes |

