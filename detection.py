import cv2
import pyautogui
import numpy as np

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    return screenshot_bgr

def find_template(template_path, screenshot):
    template = cv2.imread(template_path, 0)  # Convert to grayscale

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(template, None)
    kp2, des2 = orb.detectAndCompute(screenshot, None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()

    # Match descriptors
    matches = bf.knnMatch(des1, des2, k=2)

    # print(matches)

    # Apply ratio test
    good_matches = []
    for m, n in matches:
        # print(m.distance, n.distance)
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
    
    print(good_matches)

    if len(good_matches) >= 1:  # Adjust the threshold based on your needs
        return kp1, kp2, good_matches
    else:
        return None

if __name__ == "__alt__":
    # Take a screenshot of the whole screen
    screenshot = take_screenshot()

    # Specify the path to the template image
    template_path = "clickables/quest.png"

    # Example: Find the template image on the screen
    result = find_template(template_path, screenshot)

    # Example: If enough good matches are found, print the location
    if result:
        _, _, good_matches = result
        print(f"Template found with {len(good_matches)} good matches.")
        # You can perform additional actions based on the match, e.g., get the location
        location = pyautogui.locateOnScreen(template_path)
        print(f"Template location: {location}")
    else:
        print("Template not found.")

def click_image(image_name):
    location = pyautogui.locateOnScreen(f"clickables/{image_name}.png", confidence=0.75, grayscale=True)
    #move mouse to location
    pyautogui.moveTo(location[0], location[1])
    #click
    pyautogui.click(location[0], location[1])

if __name__ == "__main__":
    import sys
    # Assume the first command-line argument is the function to call
    function_name = sys.argv[1] if len(sys.argv) > 1 else None

    if function_name == "click_image":
        # Call the click_image function with the provided image name (second command-line argument)
        image_name = sys.argv[2] if len(sys.argv) > 2 else None
        click_image(image_name)
    else:
        print("Invalid function name. Available functions: click_image")

def scroll_down():
    pyautogui.scroll(-500) #-500 is max down scroll

def scroll_up():
    pyautogui.scroll(500)
