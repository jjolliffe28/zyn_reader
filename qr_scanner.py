import cv2
import pandas as pd
import pygame
import pyautogui
import time
import keyboard
import os

cwd = os.getcwd()
file_path = f"~/{cwd}"
full_path = os.path.expanduser(file_path)

pygame.mixer.init()

df = pd.DataFrame(columns=["Unique ID", "QR Value"])

def extract_value_from_url(url):
    return url.split('/')[-1]


def scan_qr_code():
    cap = cv2.VideoCapture(0) 
    qr_code_detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        decoded_text, points, _ = qr_code_detector.detectAndDecode(frame)
        if points is not None and len(points) > 0 and cv2.contourArea(points) > 0:
            if decoded_text:
                value = extract_value_from_url(decoded_text)
                if not df[df["QR Value"] == value].empty:
                    message = "Scanned already"
                    print(message)
                    
                else:
                    unique_id = len(df) + 1
                    df.loc[len(df)] = [unique_id, value]
                    message = f"Scanned: {value}"
                    pts = points[0].astype(int)
                    for i in range(len(pts)):
                        pt1 = tuple(pts[i])
                        pt2 = tuple(pts[(i + 1) % len(pts)])
                        cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
                    cv2.putText(frame, message, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    print(message)
                    upload_code_to_website(value)

                
    
        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def upload_code_to_website(value):
    try:
        pyautogui.write(value)
        pyautogui.press('enter')
        
        for _ in range(0, len(value) + 1):
            pyautogui.press('backspace')
            pyautogui.write('')
        time.sleep(1) 

        print(f"Successfully uploaded: {value}")

    except Exception as e:
        print(f"Failed to upload {value}: {e}")

if __name__ == "__main__":
    input("Navigate to the ZYN Rewards page and position the cursor on the input field. Press Enter to start scanning and uploading codes.")


    scan_qr_code()
