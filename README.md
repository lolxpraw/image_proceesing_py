# Digital Image Processing: RAW Image Processing with Python
# Digital Image Processing: RAW Image Processing (Python + C)

This project provides a complete Python implementation for reading, creating, and processing uncompressed RAW raster images (24-bit RGB, 8-bit Grayscale, and Binary Scale). It replaces traditional low-level C programs (`fread`, `fwrite`, byte pointer manipulation) with clean, high-performance Python implementations while maintaining 1:1 algorithmic and binary equivalency.
This repository contains the complete implementation for **Assignment 2 (BT2)**:
- **Step 1 (Python)**: Generates 24-bit/pixel color raw image `rgb.raw` (Interleaved RGB).
- **Step 2 (C Program)**: Reads `rgb.raw` and converts to 8-bit grayscale image `gray.raw` using standard luminance formula $Y = 0.299R + 0.587G + 0.114B$.
- **Step 3 (C Program)**: Reads `gray.raw` and converts to binary scale image `binary.raw` via thresholding ($T = 128$).

---

## 1. Project Structure
## 1. Project Files

| File | Description |
| :--- | :--- |
| **`step1_create_rgb_raw.py`** | **Step 1**: Generates an interleaved 24-bit/pixel RGB raw file (`rgb.raw`). Supports both synthetic color pattern generation and conversion from arbitrary image formats (`.jpg`, `.png`, `.bmp`). |
| **`step2_rgb_to_gray.py`** | **Step 2 (Replaces C program)**: Reads binary bytes from `rgb.raw`, calculates luminance grayscale values using standard ITU-R BT.601 formula, and outputs `gray.raw` (8 bits/pixel). |
| **`step3_gray_to_binary.py`** | **Step 3**: Reads `gray.raw` and applies thresholding ($T = 128$) to produce a binary scale image `binary.raw` (values 0 and 255). |
| **`run_all.py`** | Pipeline runner to execute Step 1, Step 2, and Step 3 seamlessly with a single command. |
| **`.gitignore`** | Excludes generated `.raw` binary files, `.png` previews, and Python cache from Git tracking. |
| File | Language | Description |
| :--- | :--- | :--- |
| **`step1_create_rgb_raw.py`** | Python | **Step 1**: Creates `rgb.raw` (24 bits/pixel). Supports auto-generating synthetic test images or converting custom images (`.jpg`, `.png`, `.bmp`). |
| **`step2_rgb_to_gray.c`** | C | **Step 2**: Reads `rgb.raw` byte-by-byte via `fread`, calculates grayscale value, and writes `gray.raw` (8 bits/pixel) via `fwrite`. |
| **`step3_gray_to_binary.c`** | C | **Step 3**: Reads `gray.raw`, applies thresholding ($T = 128$), and writes `binary.raw` (values 0 and 255). |
| **`run_all.py`** | Python | Orchestrates the entire pipeline (runs Step 1 in Python, auto-compiles C files with GCC if needed, and executes Steps 2 & 3). |
| **`.gitignore`** | Git | Excludes `.raw`, `.png`, compiled `.exe` files, and temporary cache. |

---

## 2. Requirements & Installation
## 2. Compilation (C Programs)

- Python 3.8+
- Required packages:
  ```bash
  pip install pillow numpy
  ```
Compile the C source files using GCC:

```bash
# Compile Step 2
gcc -O2 step2_rgb_to_gray.c -o step2_rgb_to_gray.exe

# Compile Step 3
gcc -O2 step3_gray_to_binary.c -o step3_gray_to_binary.exe
```

---

## 3. How to Run

Open your terminal (PowerShell, Command Prompt, or Bash) in the project directory:
### Method A: Automated All-in-One Execution
```powershell
# Using default synthetic test pattern (512x512)
python run_all.py

### Option A: Run the entire pipeline in one command (Recommended)
# Or using your own custom image
python run_all.py my_photo.jpg
```

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
### Method B: Manual Step-by-Step Execution

```bash
# Step 1: Create rgb.raw from test pattern or custom image
#### Step 1: Create RGB RAW (Python)
```powershell
python step1_create_rgb_raw.py
# (Or: python step1_create_rgb_raw.py my_image.jpg)
# (Or with custom image: python step1_create_rgb_raw.py my_photo.jpg)
```

# Step 2: Convert rgb.raw to gray.raw (8-bit grayscale)
python step2_rgb_to_gray.py
#### Step 2: Convert to Grayscale (C Program)
```powershell
.\step2_rgb_to_gray.exe
# (Optional custom dimensions: .\step2_rgb_to_gray.exe 512 512)
```

# Step 3: Convert gray.raw to binary.raw (Binary scale, default threshold = 128)
python step3_gray_to_binary.py
#### Step 3: Convert to Binary Scale (C Program)
```powershell
.\step3_gray_to_binary.exe
# (Optional custom threshold & dimensions: .\step3_gray_to_binary.exe 128 512 512)
```

---

## 4. Opening & Verifying RAW Files in Adobe Photoshop
## 4. Verification in Adobe Photoshop

Uncompressed raster `.raw` files do not contain file headers. When opening them in Adobe Photoshop (**File -> Open As -> Photoshop Raw (*.RAW)**), configure the dialog as follows:
To inspect the uncompressed RAW files in Adobe Photoshop (**File -> Open As -> Photoshop Raw (*.RAW)**):

### A. `rgb.raw` (Step 1)
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `3` (RGB Color)
- **Depth**: `8 Bits`
- **Interleaved**: Checked `[x]` (Stores sequential R, G, B triplets per pixel)
- **Header**: `0` Bytes
| File | Channels | Depth | Interleaved | Header |
| :--- | :--- | :--- | :--- | :--- |
| **`rgb.raw`** | `3` (RGB Color) | `8 Bits` | Checked `[x]` | `0` Bytes |
| **`gray.raw`** | `1` (Grayscale) | `8 Bits` | N/A | `0` Bytes |
| **`binary.raw`** | `1` (Grayscale) | `8 Bits` | N/A | `0` Bytes |

### B. `gray.raw` (Step 2)
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes
*Enter the image Width and Height as printed in your terminal (e.g. `512` x `512`).*

### C. `binary.raw` (Step 3)
- **Width**: `512` (or your image width)
- **Height**: `512` (or your image height)
- **Channels**: `1` (Grayscale)
- **Depth**: `8 Bits`
- **Header**: `0` Bytes

---

## 5. Technical Comparison: C vs. Python Implementation
## 5. File Size Verification

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

| File | Dimensions | Calculation | Expected Size |
| :--- | :--- | :--- | :--- |
| `rgb.raw` | $512 \times 512$ | $512 \times 512 \times 3$ bytes | **786,432 bytes** |
| `gray.raw` | $512 \times 512$ | $512 \times 512 \times 1$ bytes | **262,144 bytes** |
| `binary.raw` | $512 \times 512$ | $512 \times 512 \times 1$ bytes | **262,144 bytes** |
