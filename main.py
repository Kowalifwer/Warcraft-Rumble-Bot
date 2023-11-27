import pyautogui
import os
import sys

def get_image_location(image_name) -> tuple or None:
    location = None
    image_path = f"clickables/{image_name}"
    try:
        location = pyautogui.locateOnScreen(f"{image_path}.png", confidence=0.75, grayscale=True)
    except pyautogui.ImageNotFoundException:
        image_path = f"{image_path}_selected.png"
        # Check if fallback path exists in filesystem
        if not os.path.exists(image_path):
            return None

        # If it does, try to find it
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.75, grayscale=True)
        except pyautogui.ImageNotFoundException:
            location = None

    return location

def click_image(image_name):
    location = get_image_location(image_name)

    if location is None:
        print(f"Could not find image {image_name}")
        return

    #move mouse to location
    pyautogui.moveTo(location[0], location[1])
    #click
    pyautogui.click(location[0], location[1])

def scroll_down():
    pyautogui.scroll(-500) #-500 is max down scroll

def scroll_up():
    pyautogui.scroll(500)

def press_key(key):
    #click on bottom middle of screen to focus
    pyautogui.click(960, 900)

    #press key
    pyautogui.press(key)

if __name__ == "__main__":
    function_name = sys.argv[1] if len(sys.argv) > 1 else None

    # Assume the first command-line argument is the function to call
    if function_name:
        # Check if the function exists
        if function_name in globals() and callable(globals()[function_name]):
            # Retrieve the function and remaining arguments
            func = globals()[function_name]
            remaining_args = sys.argv[2:]
            # Call the function with the remaining arguments
            # Note this will work even if there are no arguments (it will just call func())
            func(*remaining_args)
        else:
            raise ValueError(f"Invalid function name. Available functions: {', '.join(globals().keys())}")
    else:
        print("No function name provided.")
