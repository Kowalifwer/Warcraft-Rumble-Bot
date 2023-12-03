import cv2
import numpy as np
import pyautogui
import time

# Function to find objects on the screen
def find_objects(frame, template_images):
    objects = []

    for template_image in template_images:
        template_bgr = cv2.imread(template_image)
        result = cv2.matchTemplate(frame, template_bgr, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)

        for pt in zip(*locations[::-1]):
            objects.append((pt, (pt[0] + template_bgr.shape[1], pt[1] + template_bgr.shape[0])))

    return objects

def update_frame(window_name, template_images):
    while True:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        found_objects = find_objects(screenshot_bgr, template_images)

        # Visualize the detected objects
        for obj in found_objects:
            cv2.rectangle(screenshot_bgr, obj[0], obj[1], (0, 255, 0), 2)

        cv2.imshow("xd", screenshot_bgr)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(1)

    cv2.destroyAllWindows()

# List of template images to look for
template_images = ['clickables/bluestacks_rumble_cv2.png', 'clickables/bluestacks_home.png', 'clickables/bluestacks_recent_apps.png']

# Name of the OpenCV window
window_name = 'detection'

# Create the window
# cv2.namedWindow(window_name)

time.sleep(3)

# Call the function to continuously update the frame
update_frame(window_name, template_images)
