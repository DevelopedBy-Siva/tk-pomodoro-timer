from customtkinter import *

from constants import *
from pm_timer import Timer


class TimerApp:
    def __init__(self, window):
        self.timer = Timer()
        self.window = window
        self.draw_ui()

    def draw_ui(self):
        """
        Create the UI
        """
        # Windows configs
        self.window.title(WINDOW["title"])
        self.window.config(background=WINDOW["bg"])
        self.window.minsize(width=WINDOW["width"], height=WINDOW["height"])

        # Navigation Buttons
        self.setup_navigation_buttons()
        # Countdown display
        self.setup_countdown_display()
        # Start or Reset Button
        self.start_reset_button()

        # Resize columns wrt to how the window resize
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        # Resize columns wrt to how the window resize
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=1)

    def setup_navigation_buttons(self):
        """
        Widget container enabling navigation between different timers
        """
        nav_frame = CTkFrame(self.window, bg_color=WINDOW["bg"])
        nav_frame.grid(column=0, row=0, columnspan=3, pady=50, sticky="s")
        nav_col = 0
        for key, _ in TIMER_OPTIONS:
            nav_btn = CTkButton(
                nav_frame,
                text=key,
                command=lambda key=key: self.switch_timer(key),
            )
            nav_btn.grid(column=nav_col, padx=10, row=0)
            nav_col += 1

    def setup_countdown_display(self):
        """
        Canvas widget that display the countdown
        """
        self.canvas = CTkCanvas(
            width=350, height=350, background=WINDOW["bg"], highlightthickness=0
        )
        self.canvas.create_oval(10, 10, 340, 340, width=1, outline="#fff")
        self.countdown_txt = self.canvas.create_text(
            175,
            175,
            text=self.timer.countdown_text(minutes=self.timer.active),
            font=("Ubuntu", 92, "bold"),
            fill="#fff",
        )
        self.canvas.grid(column=0, row=1, columnspan=3, sticky="s")

    def start_reset_button(self):
        """
        Button widget to start and reset the timer
        """
        self.start_reset_btn = CTkButton(
            self.window,
            text="START",
            command=self.launch_timer,
            fg_color="#FEFAE0",
            hover_color="#F2EED7",
            text_color="#000",
            height=40,
            width=200,
            font=("Ubuntu", 14),
        )
        self.start_reset_btn.grid(column=0, row=2, pady=50, columnspan=3, sticky="n")

    def switch_timer(self, btn):
        """
        Navigate across different timers and reset the countdown
        """
        if self.timer.is_running():
            return
        self.timer.activate(btn)
        self.refresh_countdown(minutes=self.timer.active)

    def refresh_countdown(self, minutes=0, seconds=None):
        """
        Updates the countdown text
        """
        self.canvas.itemconfig(
            self.countdown_txt,
            text=self.timer.countdown_text(minutes=minutes, seconds=seconds),
        )

    def kill_timer(self):
        """
        Kill the scheduled countdown
        """
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

    def launch_timer(self):
        """
        Begin the timer
        """
        # Timer is already running. So, stop and reset countdown
        if self.timer.is_running():
            return self.clear_timer()
        self.timer.start()
        self.start_reset_btn.configure(text="STOP")
        seconds = self.timer.active * 60
        self.countdown(seconds)

    def countdown(self, seconds):
        """
        Track the countdown and refreshes the countdown text every second
        """
        if seconds <= 0:
            self.timer.stop()
            self.kill_timer()
            return
        seconds -= 1
        # Update UI timer text
        self.refresh_countdown(seconds=seconds)
        self.timer_id = self.window.after(1000, self.countdown, seconds)

    def clear_timer(self):
        """
        Reset all time timer process
        """
        self.timer.stop()
        self.kill_timer()
        self.refresh_countdown(minutes=self.timer.active)
        self.start_reset_btn.configure(text="START")


window = CTk()
app = TimerApp(window)
window.mainloop()
