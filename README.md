# Digital Image Processing: RAW Image Processing (Python + C)

This repository contains the complete implementation for **Assignment 2 (BT2)**:
- **Step 1 (Python)**: Generates a 24-bit/pixel color raw image `rgb.raw` (Interleaved RGB).
- **Step 2 (C Program)**: Reads `rgb.raw` and converts to an 8-bit grayscale image `gray.raw` using the standard luminance formula:
  $$Y = 0.299 \times R + 0.587 \times G + 0.114 \times B$$
- **Step 3 (C Program)**: Reads `gray.raw` and converts to a binary scale image `binary.raw` via thresholding ($T = 128$).

---

## 1. Project Structure

| File | Language | Description |
| :--- | :--- | :--- |
| **`step1_create_rgb_raw.py`** | Python | **Step 1**: Creates `rgb.raw` (24 bits/pixel). Supports auto-generating synthetic test images or converting custom images (`.jpg`, `.png`, `.bmp`). |
| **`step2_rgb_to_gray.c`** | C | **Step 2**: Reads `rgb.raw` byte-by-byte via `fread`, calculates grayscale luminance, and writes `gray.raw` (8 bits/pixel) via `fwrite`. |
| **`step3_gray_to_binary.c`** | C | **Step 3**: Reads `gray.raw`, applies thresholding ($T = 128$), and writes `binary.raw` (values 0 and 255). |
| **`run_all.py`** | Python | Orchestrates the entire pipeline (runs Step 1 in Python, auto-compiles C files with GCC if needed, and executes Steps 2 & 3). |
| **`HUONG_DAN.md`** | Markdown | Detailed Vietnamese user guide and report reference. |
| **`.gitignore`** | Git | Excludes `.raw`, `.png`, compiled `.exe` files, and temporary cache from Git tracking. |

---

## 2. Requirements & Compilation

### Requirements
- **Python 3.8+** with `pillow` and `numpy`:
  ```bash
  pip install pillow numpy
  ```
- **GCC Compiler** (MinGW-w64 on Windows):
  ```bash
  gcc --version
  ```

### Compiling C Programs Manually
```bash
# Compile Step 2
gcc -O2 step2_rgb_to_gray.c -o step2_rgb_to_gray.exe

# Compile Step 3
gcc -O2 step3_gray_to_binary.c -o step3_gray_to_binary.exe
```
*(Note: `run_all.py` will also automatically compile these for you if the executables are not found).*

---

## 3. How to Run

### Method A: Automated All-in-One Execution (Recommended)
```powershell
# Using default synthetic test pattern (512x512)
python run_all.py

# Or using your own custom image
python run_all.py my_photo.jpg
```

---

### Method B: Manual Step-by-Step Execution

#### Step 1: Create RGB RAW (Python)
```powershell
# Generates 512x512 rgb.raw
python step1_create_rgb_raw.py

# Or from custom image:
python step1_create_rgb_raw.py my_photo.jpg
```

#### Step 2: Convert to Grayscale (C Program)
```powershell
.\step2_rgb_to_gray.exe
# (Optional custom dimensions: .\step2_rgb_to_gray.exe 512 512)
```

#### Step 3: Convert to Binary Scale (C Program)
```powershell
.\step3_gray_to_binary.exe
# (Optional custom threshold & dimensions: .\step3_gray_to_binary.exe 128 512 512)
```

---

## 4. Verification in Adobe Photoshop

To inspect the uncompressed RAW files in Adobe Photoshop (**File -> Open As -> Photoshop Raw (*.RAW)**):

| File | Channels | Depth | Interleaved | Header |
| :--- | :--- | :--- | :--- | :--- |
| **`rgb.raw`** | `3` (RGB Color) | `8 Bits` | Checked `[x]` | `0` Bytes |
| **`gray.raw`** | `1` (Grayscale) | `8 Bits` | N/A | `0` Bytes |
| **`binary.raw`** | `1` (Grayscale) | `8 Bits` | N/A | `0` Bytes |

*Enter the image Width and Height as printed in your terminal (e.g. `512` x `512`).*

---

## 5. File Size Verification

| File | Dimensions | Calculation | Expected Size |
| :--- | :--- | :--- | :--- |
| `rgb.raw` | $512 \times 512$ | $512 \times 512 \times 3$ bytes | **786,432 bytes** |
| `gray.raw` | $512 \times 512$ | $512 \times 512 \times 1$ bytes | **262,144 bytes** |
| `binary.raw` | $512 \times 512$ | $512 \times 512 \times 1$ bytes | **262,144 bytes** |
