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

class BotAction:
    
    def __init__(self, name: str, action_callable: callable, *args, **kwargs):
        self.name: str = name
        self.action_function: callable = action_callable
    
    def exectute(self, *args, **kwargs):
        success = self.action_function(*args, **kwargs)
        return success

def click_pvp():
    click_image("pvp")

def verify_in_game():
    pass

def verify_in_menu():
    pass

if __name__ == "__xd__":
    print("Starting bot...")

    for action in actions:
        action = BotAction(action)


# action setup:
# 1. start action
# 2. have optional action verification (i.e loading screen, or can see x on screen)
# 3. If action fails, retry action n times. If n times fails, fallback to fallback action OR to reset action.
# 4. If action succeeds, go to next action.

# Simple breakdown of Action:
# 1. input - Action name, will run Action code
# 2. output - Action to do next (either success or fallback action)

# If img not found -> instantly count as step fail and try again. If n fails, restart game action.

# Each step should also include a timeout, retry-count, a fallback step IF fails, and a success step IF succeeds.
#. 1. bluestacks_rumble -> wait at least 10 s and verify we in main menu.
#. 2. bluestacks_pvp


# PvP Farm
# 0. Click on the Battle button
# 1. Click on the PvP button
# 2. Click on the Rumble! button
# 3. Verify that 'searching for opponent' is displayed. If not, check that Rumble button is displayed and click it again. Otherwise, restart the game and try again.

# 4. Verify match is starting by also checking the Warfract Rumble big ass logo
# 5. Verify match started IF tower health is appeared.

# --Battle logic--
# 1. Place wolf down middle always. Think about chest intervals, and whether we should track chests.
# 2. Send Gryphon left and have arrow always turn towards bridge
# 3. Place miner always on enemy gold node
# 4. Place kobold on left lane.
# 5. Place baron Mid ?
# 6. Necromancer right ?

# Scan periodically for IF match ended. IDK if via TIMER, or by checking DEFEAT/VICTORY screens.

# notes:
# 1. think about what units to use in army and level and stuff. think if should hardcode tactics or just random select and place.
# 2. figure out if there is a way to track xp gain ?


# Launch game, wait a while (10 s +).