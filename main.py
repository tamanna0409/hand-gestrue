import threading
import cv2
import brightness_control
import volume_control
import file_manager
import photo_capture

# Start capturing video
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

def main():
    print("Control System Using Keys:")
    print("b - Adjust Brightness")
    print("v - Adjust Volume")
    print("f - Open File Manager")
    print("p - Capture Photo")
    print("q - Exit & Close Camera")

    while True:
        choice = input("Enter your choice (b/v/f/p/q): ").strip().lower()

        if choice == 'b':
            threading.Thread(target=brightness_control.control_brightness).start()
        elif choice == 'v':
            threading.Thread(target=volume_control.control_volume).start()
        elif choice == 'f':
            threading.Thread(target=file_manager.open_file_manager).start()
        elif choice == 'p':
            threading.Thread(target=photo_capture.capture_photo).start()
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Use b, v, f, p, or q.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
