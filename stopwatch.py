import tkinter as tk
from tkinter import messagebox
import time
import win32gui
import win32con

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("400x200")

        self.running = False
        self.start_time = None
        self.elapsed_time = 0

        self.timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 40))
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_stopwatch)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_stopwatch, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_stopwatch, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=20)

        self.hour_label = tk.Label(root, text="Hours:")
        self.hour_label.pack(pady=5)

        self.hour_entry = tk.Entry(root)
        self.hour_entry.pack()

        self.minute_label = tk.Label(root, text="Minutes:")
        self.minute_label.pack(pady=5)

        self.minute_entry = tk.Entry(root)
        self.minute_entry.pack()

        self.set_timer_button = tk.Button(root, text="Set Timer", command=self.set_timer)
        self.set_timer_button.pack()

        # Add the extended window style to make the window stay on top
        self.root.attributes("-topmost", True)
        hwnd = self.root.winfo_id()
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOPMOST)

        # Handle deactivation manually
        self.root.protocol("WM_WINDOWPOSCHANGING", self.on_window_pos_changing)

        self.root.after(100, self.update_timer_label)

    def on_window_pos_changing(self):
        # Handle the window deactivation manually
        hwnd = self.root.winfo_id()
        self.root.attributes("-topmost", True)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def update_timer_label(self):
        if self.running:
            elapsed_time = time.time() - self.start_time + self.elapsed_time
            formatted_time = self.format_time(elapsed_time)
            self.timer_label.config(text=formatted_time)
        self.root.after(100, self.update_timer_label)

    def start_stopwatch(self):
        if self.start_time is None:
            self.start_time = time.time() - self.elapsed_time
        else:
            self.start_time = time.time() - self.elapsed_time
        self.running = True
        self.update_timer_label()
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def pause_stopwatch(self):
        self.elapsed_time = time.time() - self.start_time
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def reset_stopwatch(self):
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.timer_label.config(text="00:00:00")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def set_timer(self):
        try:
            hours = int(self.hour_entry.get())
            minutes = int(self.minute_entry.get())
            if hours < 0 or minutes < 0:
                raise ValueError("Please enter non-negative values for hours and minutes.")
            seconds = hours * 3600 + minutes * 60
            self.elapsed_time = seconds
            self.timer_label.config(text=self.format_time(seconds))
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    @staticmethod
    def format_time(seconds):
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
