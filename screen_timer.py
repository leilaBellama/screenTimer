import ctypes
from activity_monitor import ActivityMonitor
import argparse
import os

class ScreenTimer:
    # Defaults: sleep_minutes = 30 minutes, off_minutes = 5 minutes
    def __init__(self, sleep_minutes = 30, off_minutes = 5):
        self.sleep_minutes = sleep_minutes 
        self.off_minutes = off_minutes 
        self.stop = True
        self.sleep_activity_monitor = ActivityMonitor()
        self.off_activity_monitor = ActivityMonitor()
        self.off_activity_monitor.repeats = False

    def run(self):
        self.stop = False
        self.sleep_activity_monitor.stop = False
        self.off_activity_monitor.stop = False

        # Repeats until shutdown or program stopped
        while True and not self.stop:
            # Begin monitoring for activity
            self.sleep_activity_monitor.start(self.sleep_minutes)

            if self.stop: break

            # After sleep_minutes with no activity, turn off screen
            ctypes.windll.user32.PostMessageW(0xFFFF, 0x112, 0xF170, 2)

            # Begin monitoring for activity to turn back on
            self.off_activity_monitor.start(self.off_minutes)

            # If no activity, shutdown
            if not self.off_activity_monitor.isActive:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                self.stop = True

    # Function to end program and both activity monitors
    def end(self):
        self.stop = True
        self.sleep_activity_monitor.stop = True
        self.off_activity_monitor.stop = True


# Function to handle command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser()
    
    # Adding optional arguments
    parser.add_argument("sleep_minutes", nargs="?", type=int, default=30, help="An optional sleep_minutes argument (default: 30)")
    parser.add_argument("off_minutes", nargs="?", type=int, default=5, help="An optional activity time argument (default: 5)")

    return parser.parse_args()

# Runs program with arguments from command line
if __name__ == "__main__":
    args = parse_arguments()
    app = ScreenTimer(sleep_minutes = args.sleep_minutes, off_minutes = args.off_minutes)
    app.run()