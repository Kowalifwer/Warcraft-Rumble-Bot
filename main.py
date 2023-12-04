import pyautogui
import os
import sys

SCREEN_LOCATE_PARAMS = {
    "confidence": 0.75,
    "grayscale": True,
    "region": None,
}

# Final unix

def get_image_location(image_name, centered=True) -> tuple or None:
    location = None
    image_path = f"clickables/{image_name}"

    # Make copy of global state locate params, so we can modify it under certain conditions
    screen_params = SCREEN_LOCATE_PARAMS.copy()

    # If we are dealing with bluestacks icons, we need to set the region to None, since the icons are not in the game screen.
    if "bluestacks" in image_name:
        screen_params["region"] = None

    # Check if image or fallback exists in filesystem
    if not (os.path.exists(f"{image_path}.png") or os.path.exists(f"{image_path}_selected.png")):
        raise FileNotFoundError(f"Could not find image {image_name}")

    try:
        location = pyautogui.locateOnScreen(f"{image_path}.png", **screen_params)
    except pyautogui.ImageNotFoundException:
        image_path = f"{image_path}_selected.png"
        # Check if fallback path exists in filesystem
        if not os.path.exists(image_path):
            return None

        # If it does, try to find it
        try:
            location = pyautogui.locateOnScreen(image_path, **screen_params)
        except pyautogui.ImageNotFoundException:
            location = None

    if location and centered:
        location = pyautogui.center(location)

    return location

def click_image(image_name, centered=True):
    location = get_image_location(image_name, centered=centered)

    if location is None:
        print(f"Could not find image {image_name}")
        return

    #move mouse to location
    pyautogui.moveTo(location[0], location[1], duration=0.5, tween=pyautogui.easeInOutQuad)
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

def start_game():
    def verify_loading():
        return get_image_location("logo")

    def verify_in_menu():
        return get_image_location("store")

    click_image("bluestacks_rumble")
    
    #wait for game to load
    loading = True if verify_loading() else False

    attempts = 1
    while not sleep(10, condition=verify_in_menu):
        if attempts > 5:
            print(f"Game failed to load after {attempts} attempts. RIP!")
            return False

        print(f"Game failed to load on attempt {attempts}/6. Trying again.")
        attempts += 1

    print("Game loaded!")
    return True #if we get here, we are in menu

def always_false(*args, **kwargs):
    return False

def sleep(timeout: int=2, condition: callable=always_false, *args, **kwargs):
    """
    Sleeps for the specified timeout, or until a condition is met.
    Note that a condition and its arguments must be passed, since state can change and needs to be re-evaluated.

    Args:
        timeout (int): The timeout in seconds.
        condition (callable): A function that returns False if it fails, whilst any other output will result in a pass.
        *args: Positional arguments to pass to the condition function.
        **kwargs: Keyword arguments to pass to the condition function.

    Returns:
        bool: True if the condition was met, False if the timeout was reached.
    """

    # If no condition parameter is provided (default), just sleep for the timeout.
    if condition is always_false:
        pyautogui.sleep(timeout)
        return True
    
    # Otherwise, sleep until the condition is met or the timeout is reached.
    attempt_interval = 0.25
    max_attempts = timeout / attempt_interval
    current_attempt = 0

    while current_attempt < max_attempts:
        print(f"Sleeping... {current_attempt * attempt_interval}s/{timeout}s")
        if condition(*args, **kwargs): #if condition met, exit sleep loop
            return True
        
        pyautogui.sleep(attempt_interval)
        current_attempt += 1
    
    return False # if we get here, we timed out

def start_pvp():
    while True:
        click_image("battle")

        sleep(5, get_image_location, "pvp")

        click_image("pvp")

        sleep(5, get_image_location, "pvp_start")

        click_image("pvp_start")

        sleep(1.5, get_image_location, "pvp_cancel")

        click_image("pvp_cancel")

        sleep(5, get_image_location, "back")

        click_image("back")

        sleep(5, get_image_location, "battle")

def restart_game():
    click_image("bluestacks_home")

    sleep(5, get_image_location, "bluestacks_home_search")
    print("On home screen, restarting game...")

    click_image("bluestacks_recent_apps")
    
    sleep(5, get_image_location, "bluestacks_clear_all")
    print("On recent apps screen")

    click_image("bluestacks_clear_all")
    
    sleep(5, get_image_location, "bluestacks_home_search")
    print("Cleared all apps")

    #start game
    game_started = start_game()
    if not game_started:
        print("Failed to start game. Restarting...")
        restart_game()

def detect_multiple_images(infinite=False):
    template_images = [
        "combat/1_gold_unit",
        "combat/2_gold_unit",
        "combat/3_gold_unit",
        "combat/4_gold_unit",
        "combat/5_gold_unit",
        "combat/6_gold_unit",
    ]
    _infinite = True

    while _infinite:
        if not infinite:
            _infinite = False

        count = 0
        for template_image in template_images:
            location = get_image_location(template_image)
            if location:
                print(f"Found {template_image} at {location}")
                count += 1
            else:
                print(f"Could not find {template_image}")
        
        if count == len(template_images):
            print("Found all images!")
        else:
            print(f"Found {count}/{len(template_images)} images")
        
        pyautogui.sleep(1)

def select_unit_by_cost(cost: int):
    cost = int(cost)
    if cost < 1 or cost > 6:
        raise ValueError(f"Invalid cost {cost}. Must be between 1 and 6.")

    click_image(f"combat/{cost}_gold_unit")

def click_left_lane():
    if not SCREEN_LOCATE_PARAMS["region"]:
        raise ValueError("Cannot click left lane. Game screen bounds not established.")
    
    
    # get left lane cords. should be 1/4 of bound region in x, and 2/3 of bound region in y
    left_lane_x = SCREEN_LOCATE_PARAMS["region"][0] + (SCREEN_LOCATE_PARAMS["region"][2] / 4)
    left_lane_y = SCREEN_LOCATE_PARAMS["region"][1] + (SCREEN_LOCATE_PARAMS["region"][3] / 3 * 2)

    pyautogui.click(left_lane_x, left_lane_y, duration=0.25, tween=pyautogui.easeInOutQuad)

def click_middle_lane():
    if not SCREEN_LOCATE_PARAMS["region"]:
        raise ValueError("Cannot click middle lane. Game screen bounds not established.")
    
    # get middle lane cords. should be 1/2 of bound region in x, and 2/3 of bound region in y
    middle_lane_x = SCREEN_LOCATE_PARAMS["region"][0] + (SCREEN_LOCATE_PARAMS["region"][2] / 2)
    middle_lane_y = SCREEN_LOCATE_PARAMS["region"][1] + (SCREEN_LOCATE_PARAMS["region"][3] / 3 * 2)

    pyautogui.click(middle_lane_x, middle_lane_y, duration=0.25, tween=pyautogui.easeInOutQuad)

def click_right_lane():
    if not SCREEN_LOCATE_PARAMS["region"]:
        raise ValueError("Cannot click right lane. Game screen bounds not established.")
    
    # get right lane cords. should be 3/4 of bound region in x, and 2/3 of bound region in y
    right_lane_x = SCREEN_LOCATE_PARAMS["region"][0] + (SCREEN_LOCATE_PARAMS["region"][2] / 4 * 3)
    right_lane_y = SCREEN_LOCATE_PARAMS["region"][1] + (SCREEN_LOCATE_PARAMS["region"][3] / 3 * 2)

    pyautogui.click(right_lane_x, right_lane_y, duration=0.25, tween=pyautogui.easeInOutQuad)

def establish_game_screen_bounds(force_reset=False):
    # note currently relies on garrosh icon being in top left. TODO: make this more robust.
    print("Establishing game screen bounds...")

    # read from file bounds.txt

    bounds = SCREEN_LOCATE_PARAMS["region"]
    if bounds:
        print("Bounds fetched from global state.")
        return True

    else:
        try:
            with open("bounds.txt", "r") as f:
                bounds = f.read().split(",")
                print(bounds)
                bounds = [int(bound) for bound in bounds]
                SCREEN_LOCATE_PARAMS["region"] = tuple(bounds)
                print("Bounds fetched from bounds.txt.")
                return True
        except Exception as e:
            bounds = None
            print("Failed to read bounds.txt. Creating new bounds.")

    if force_reset or not bounds:
        top_left_icon_location = get_image_location("top_left_icon", centered=False)
        bottom_right_icon_location = get_image_location("bottom_right_icon", centered=False)

        # check we have both locations
        if not top_left_icon_location or not bottom_right_icon_location:
            print("Failed to create screen bounds. Could not find top left or bottom right icon.")
            return False

        # bottom right location is foudn at topleft, we need to add the width and height of the icon to get the bottom right
        bottom_right_icon_location = (bottom_right_icon_location[0] + bottom_right_icon_location.width, bottom_right_icon_location[1] + bottom_right_icon_location.height)

        # create a bounding box
        bounding_box = (top_left_icon_location[0], top_left_icon_location[1], bottom_right_icon_location[0] - top_left_icon_location[0], bottom_right_icon_location[1] - top_left_icon_location[1])

        SCREEN_LOCATE_PARAMS["region"] = bounding_box

        #override bounds.txt with new bounds
        with open("bounds.txt", "w") as f:
            f.write(",".join([str(bound) for bound in bounding_box]))

    return True

if __name__ == "__main__":
    establish_game_screen_bounds()

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
            

# Notes:
# 1.All x_gold_unit images get detected. Only from the active battle screen, as intended.

# Optimization ideas:
# 1. find a way to periodically detect the bounds of the game screen (its narrower than the actual screen), and only search within those bounds for gameplay.

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

def bluestacks_rumble():
    click_image("bluestacks_rumble")

def bluestacks_pvp():
    click_image("bluestacks_pvp")

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