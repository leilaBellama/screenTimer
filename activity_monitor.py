import time
import pyautogui

class ActivityMonitor:
    # Set the threshold for inactivity (in minutes)
    def __init__(self):
        self.repeats = True
        self.isActive = False
        self.stop = True

    # Function to monitor user activity, until time reached or activity detected
    def start(self, threshold = 5):
        self.remaining_seconds = threshold * 60
        self.stop = False
        self.isActive = False
        # Get start time and mouse position
        start_activity_time = time.time() 
        mouse_position = pyautogui.position()

        # Countdown until activity detected or time runs out
        while True and not self.stop:
            time.sleep(1)
            self.remaining_seconds -= 1
            # If activity detected, repeat or stop
            if mouse_position != pyautogui.position():
                if self.repeats:
                    self.remaining_seconds = threshold * 60
                    mouse_position = pyautogui.position()
                    start_activity_time = time.time()
                else: 
                    self.isActive = True
                    self.stop = True
                    break
            # If time reached, stop
            if time.time() - start_activity_time > (threshold * 60):
                self.stop = True
                break
