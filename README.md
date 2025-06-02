# 🖥️ Screen Sleep Timer

A Windows-based utility that monitors keyboard activity and automatically turns off the screen or suspends the system after a period of inactivity. Built with Python and Tkinter.

---

## 🚀 Features

- ⏲️ Monitors keyboard and mouse activity.
- 💤 Turns off the screen after X minutes of inactivity.
- 🔌 If still inactive, suspends the system after Y more minutes.
- ✅ GUI with configurable sleep/off timers.
- 💾 Save timer values as defaults via checkboxes.
- 🔄 Automatically restarts monitoring after wake-up.
- 🪟 Windows-only (uses Win32 API calls).

---

## 🖼️ GUI Preview

![image](https://github.com/user-attachments/assets/73b3b9cd-abc9-4000-a7b5-5d3923d952bf)

---

## ⚙️ How It Works

1. **Sleep Phase** – After `sleep_minutes` of inactivity, the screen turns off. If activity is detected during this time, the timer restarts.
2. **Off Phase** – After another `off_minutes` with no activity, the system suspends. If activity is detected during this time, it restarts at the sleep phase.
3. The GUI provides controls to start/stop monitoring and update time settings.
4. Default sleep and off minutes can be stored for future use.

### 🖥️ Using the GUI

1. Launch the GUI:
   ```bash
   python screen_sleep_gui.py

2. In the app:

Set "Sleep After": Minutes of inactivity before screen turns off

Set "Off After": Minutes to restart program before the system suspends

3. Optional:

Check the "Default" box to save your current setting for future runs

Click Start to begin monitoring. The timer countdown will be shown.

4. To stop, click Stop.

## 🖥️ Run Without the GUI

Use command in terminal:
python screen_timer [optional arg sleep_minutes] [optional arg off_minutes]

