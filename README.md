# Real-Time License Plate Recognition

This project captures video from a webcam to detect and recognize license plate numbers in real-time using OpenCV and Tesseract OCR. The application preprocesses the image, isolates the license plate region, and extracts the text using OCR.

---

## Features

- **Real-Time Webcam Feed**: Captures live video and displays a centered Region of Interest (ROI) for license plate detection.
- **Image Preprocessing**: Applies grayscale conversion, histogram equalization, Gaussian blur, and edge detection to enhance text detection accuracy.
- **Contour Detection**: Identifies the largest contour to isolate the license plate region.
- **Text Recognition**: Utilizes Tesseract OCR to extract alphanumeric text from the detected license plate.
- **User Interaction**: 
  - Press `c` to capture and process the license plate from the ROI.
  - Press `q` to quit the application.

---

## Prerequisites

### Software
- **Python 3.7+**
- **Tesseract OCR**  
  Download and install Tesseract OCR: [Tesseract Installation Guide](https://github.com/tesseract-ocr/tesseract)

### Python Packages
Install the required Python packages using pip:
```bash
pip install opencv-python pytesseract
```

## Usage

- Position the license plate within the green rectangle (ROI) on the webcam feed.
- Press `c` to capture and process the image.
- The captured license plate is saved as captured_license_plate.jpg.
- The recognized license plate number is displayed in the terminal.
- Press `q` to exit the application.

## Known Issues

- The OCR accuracy may vary under poor lighting or due to blurry images.
- Incorrect results may occur if the license plate has non-standard fonts or designs.
