import cv2
import os

# Create the folder if it doesn't exist
output_folder = 'calibration_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Open the camera
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print(f"Press 's' to save an image to '{output_folder}/'.")
print("Press 'q' or 'Esc' to quit.")

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('Camera Feed', frame)

    k = cv2.waitKey(1)
    if k == 27 or k == ord('q'):
        # ESC pressed or 'q'
        print("Escape hit, closing...")
        break
    elif k == ord('s'):
        # 's' pressed
        img_name = os.path.join(output_folder, "calibration_img_{}.png".format(img_counter))
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cap.release()
cv2.destroyAllWindows()