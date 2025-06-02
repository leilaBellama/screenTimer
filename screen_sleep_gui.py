import tkinter as tk
import threading
import os
import configparser
from screen_timer import ScreenTimer

class ScreenSleep:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Monitor Controller")
        self.root.geometry("250x220")
        self.running = False

        # Config setup for defaults
        self.config_file = "settings.ini"
        self.config = configparser.ConfigParser()
        self.default_sleep_minutes = 30
        self.default_off_minutes = 5

        # Get defaults from file
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            try:
                self.default_sleep_minutes = int(self.config['DEFAULT']['sleep_minutes'])
            except (KeyError, ValueError):
                pass
            try:
                self.default_off_minutes = int(self.config['DEFAULT']['off_minutes'])
            except (KeyError, ValueError):
                pass

        self.screen_timer = ScreenTimer(self.default_sleep_minutes, self.default_off_minutes)

        # --- Sleep Input + Checkbox ---
        tk.Label(root, text="Sleep After (minutes):").pack()
        sleep_frame = tk.Frame(root)
        sleep_frame.pack()
        self.sleep_var = tk.StringVar(value=str(self.default_sleep_minutes))
        self.sleep_var.trace_add('write', self.on_sleep_entry_change)

        self.sleep_entry = tk.Entry(sleep_frame, textvariable=self.sleep_var, width=10)
        self.sleep_entry.pack(side="left")

        self.make_default_var = tk.BooleanVar(value=False)
        if self.sleep_var.get() == str(self.default_sleep_minutes):
            self.make_default_var.set(True)
        self.make_default_checkbox = tk.Checkbutton(
            sleep_frame, text="Default", variable=self.make_default_var,
            command=self.on_make_default_checked
        )
        self.make_default_checkbox.pack(side="left")

        # --- off Input + Checkbox ---
        tk.Label(root, text="Off After (minutes):").pack()
        off_frame = tk.Frame(root)
        off_frame.pack()
        self.off_var = tk.StringVar(value=str(self.default_off_minutes))
        self.off_var.trace_add('write', self.on_off_entry_change)

        self.off_entry = tk.Entry(off_frame, textvariable=self.off_var, width=10)
        self.off_entry.pack(side="left")

        self.make_default_off_var = tk.BooleanVar(value=False)
        if self.off_var.get() == str(self.default_off_minutes):
            self.make_default_off_var.set(True)
        self.make_default_off_checkbox = tk.Checkbutton(
            off_frame, text="Default", variable=self.make_default_off_var,
            command=self.on_make_default_off_checked
        )
        self.make_default_off_checkbox.pack(side="left")

        # --- Time Display ---
        self.time_label = tk.Label(root, text="Time Remaining: --:--", fg="blue")
        self.time_label.pack(pady=5)

        # --- Start/Stop Button ---
        self.start_button = tk.Button(root, text="Start", command=self.start_stop)
        self.start_button.pack(pady=5)

    # --- Checkbox logic ---
    # When user changes sleep entry, update checkbox state
    def on_sleep_entry_change(self, *args):
        self.update_checkbox_state()

    # When user changes off entry, update checkbox state
    def on_off_entry_change(self, *args):
        self.update_off_checkbox_state()

    def update_checkbox_state(self):
        try:
            current_value = int(self.sleep_var.get())
        except ValueError:
            # Invalid input: uncheck checkbox to avoid confusion
            self.make_default_var.set(False)
            return
        # Check the box if current value matches default, else uncheck
        self.make_default_var.set(current_value == self.default_sleep_minutes)

    def update_off_checkbox_state(self):
        try:
            current_value = int(self.off_var.get())
        except ValueError:
            # Invalid input: uncheck checkbox to avoid confusion
            self.make_default_off_var.set(False)
            return
        # Check the box if current value matches default, else uncheck
        self.make_default_off_var.set(current_value == self.default_sleep_minutes)

    # When default box is checked, save the input in config file
    # When default box is unchecked, keep original defaults
    def on_make_default_checked(self):
        if self.make_default_var.get():
            try:
                new_default = int(self.sleep_var.get())
            except ValueError:
                self.make_default_var.set(False)
                return
        else:
            new_default = 30
        
        self.config.read(self.config_file)
        if 'DEFAULT' not in self.config:
            self.config['DEFAULT'] = {}
        self.config['DEFAULT']['sleep_minutes'] = str(new_default)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        self.default_sleep_minutes = new_default
            
    # When default box is checked, save the input in config file
    # When default box is unchecked, keep original defaults
    def on_make_default_off_checked(self):
        if self.make_default_off_var.get():
            try:
                new_default = int(self.off_var.get())
            except ValueError:
                self.make_default_off_var.set(False)
                return
        else:
            new_default = 5

        self.config.read(self.config_file)
        if 'DEFAULT' not in self.config:
            self.config['DEFAULT'] = {}
        self.config['DEFAULT']['off_minutes'] = str(new_default)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        self.default_off_minutes = new_default

    # --- Program logic ---
    def start_stop(self):
        if not self.running:
            self.start_program()
        else:
            self.stop_program()

    def start_program(self):
        if not self.running:
            self.start_button.config(text="Stop")
            try:
                self.sleep_minutes = int(self.sleep_var.get())
                self.off_minutes = int(self.off_var.get())
                if self.sleep_minutes <= 0 or self.off_minutes <= 0:
                    raise ValueError
            except ValueError:
                self.time_label.config(text="Enter numbers > 0", fg="orange")
                return

            self.running = True
            self.screen_timer = ScreenTimer(self.sleep_minutes, self.off_minutes)
            self.time_label.config(text=f"Time Remaining: {self.sleep_minutes:02}:00", fg="blue")
            threading.Thread(target=self.background_task, daemon=True).start()
            
    def stop_program(self):
        self.start_button.config(text="Start")
        self.screen_timer.end()
        self.running = False
        self.time_label.config(text="Time Remaining: --:--", fg="blue")

    def background_task(self):
        self.update_timer()
        self.screen_timer.run()
        
    # Update remaning time display every second until stopped
    def update_timer(self):
        if self.running:
            if not self.screen_timer.sleep_activity_monitor.stop:
                seconds = getattr(self.screen_timer.sleep_activity_monitor, "remaining_seconds", None)
            else:
                seconds = getattr(self.screen_timer.off_activity_monitor, "remaining_seconds", None)
                if seconds == 0:
                    self.stop_program()

            if isinstance(seconds, int):
                mins, secs = divmod(seconds, 60)
                self.time_label.config(text=f"Time Remaining: {mins:02}:{secs:02}")
            else:
                self.time_label.config(text="Time Remaining: --:--")
            self.root.after(1000, self.update_timer)
        else:
            self.time_label.config(text="Time Remaining: --:--")

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenSleep(root)
    root.mainloop()
