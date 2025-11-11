import cv2
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "ISL_data")

NUM_IMAGES_TO_COLLECT = 105

def final_data_collection():
    sign_name = input("Enter the name of the sign (e.g., hello, one): ").strip().lower()
    if not sign_name.isalnum():
        print("[!!! ERROR] Invalid sign name. Please use simple letters and numbers only.")
        return

    sign_path = os.path.join(DATA_PATH, sign_name)
    os.makedirs(sign_path, exist_ok=True)

    print(f"\n[INFO] Will attempt to save images in this EXACT folder:")
    print(f"--> {os.path.abspath(sign_path)}")
    print("---------------------------------------------------\n")

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("[!!! ERROR] Could not open webcam.")
        return

    print("INSTRUCTIONS: A window will open. CLICK ON IT, then press 's' to start.")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "CLICK HERE, then press 's' to start", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('Setup Window', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    print("Starting collection...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(0.3)

    for i in range(NUM_IMAGES_TO_COLLECT):
        ret, frame = cap.read()
        if not ret:
            print(f"[!!! ERROR] Failed to capture frame for image {i+1}.")
            continue

        frame = cv2.flip(frame, 1)
        cv2.imshow('Setup Window', frame)
        cv2.waitKey(1)

        image_name = f"{sign_name}_{int(time.time())}_{i}.jpg"
        save_path = os.path.join(sign_path, image_name)

        success = cv2.imwrite(save_path, frame)
        if success:
            print(f"[SUCCESS] Image {i+1}/{NUM_IMAGES_TO_COLLECT} saved to {save_path}")
        else:
            print(f"[---FAILURE---] FAILED TO SAVE IMAGE {i+1} at {save_path}")

        time.sleep(1)

    print("\nCollection finished.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    final_data_collection()
