import pyautogui

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
