import time
import pyautogui

def play_bot():
    while True:
        # Adjust these coordinates based on your game interface
        target_location = (500, 500)

        # Move mouse to target location
        pyautogui.moveTo(target_location[0], target_location[1], duration=1)

        # # Click (you might need to adjust the button and duration)
        # pyautogui.click(button='left', duration=0.5)

        # Add some delay to avoid rapid actions
        time.sleep(2)

        

if __name__ == "__main__":
    play_bot()