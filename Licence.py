import cv2
import pytesseract
import numpy as np

# Set the Tesseract executable path (for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enhance contrast using histogram equalization
    equalized = cv2.equalizeHist(gray)

    # Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(equalized, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 100, 200)
    dilated_edges = cv2.dilate(edges, None, iterations=1)

    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    possible_rois = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 2.0 < aspect_ratio < 5.5 and w > 100 and h > 20:
            roi_candidate = image[y:y + h, x:x + w]
            possible_rois.append(roi_candidate)

    if possible_rois:
        roi = max(possible_rois, key=lambda r: r.shape[0] * r.shape[1])
        print("✅ Suitable ROI detected.")
    else:
        print("⚠️ No suitable contour detected; using entire image.")
        roi = image

    # Resize
    roi = cv2.resize(roi, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    # Final preprocessing for Tesseract
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Morphological operation to connect characters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.dilate(thresh, kernel, iterations=1)

    # Debug: show what OCR sees
    cv2.imshow("Processed ROI", processed)

    return processed

def recognize_text_from_image(image):
    processed_image = preprocess_image(image)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    return text.strip()

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("🎥 Press 'c' to capture and recognize license plate.")
print("❌ Press 'q' to quit.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    h, w, _ = frame.shape
    x1, y1, x2, y2 = int(w * 0.3), int(h * 0.3), int(w * 0.7), int(h * 0.7)
    roi = frame[y1:y2, x1:x2]

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow('Webcam Feed', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        captured_image = roi.copy()
        cv2.imwrite('captured_license_plate.jpg', captured_image)
        print("📸 Captured image saved as 'captured_license_plate.jpg'.")

        recognized_text = recognize_text_from_image(captured_image)
        if recognized_text:
            print("🔍 Recognized License Plate Number:", recognized_text)
        else:
            print("❌ No text recognized. Try again with better lighting/angle.")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
