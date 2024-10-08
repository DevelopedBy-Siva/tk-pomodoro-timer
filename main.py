from customtkinter import *
from PIL import Image

from constants import *
from pm_timer import Timer
from settings import Settings


class TimerApp:
    def __init__(self, window):
        self.window = window
        self.timer = Timer()
        self.settings = Settings(root=self.window, refresh=self.configs_updated)
        self.nav_buttons = {}
        self.canvas = None
        # Load images for widget icons
        self.play_ico = self.load_widget_img("play")
        self.stop_ico = self.load_widget_img("stop")
        self.settings_ico = self.load_widget_img("settings", (25, 25))
        # Create Ui
        self.draw_ui()

    def load_widget_img(self, src, size=(14, 14)):
        """
        Load images for widgets
        Args:
            src (str): name of the image to load
        Returns:
            CTKImage: returns a image
        """
        img = Image.open(ASSETS[src])
        return CTkImage(light_image=img, dark_image=img, size=size)

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
        # Settings button
        self.setup_setting_btn()

        # Resize rows & columns wrt to how the window resize
        for index in range(3):
            self.window.grid_columnconfigure(index, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=1)

    def setup_navigation_buttons(self):
        """
        Widget container enabling navigation between different timers
        """
        nav_frame = CTkFrame(self.window, fg_color=WINDOW["bg"], bg_color=WINDOW["bg"])
        nav_frame.grid(column=0, row=0, columnspan=3, pady=25, sticky="s")

        nav_col = 0
        for key, _ in TIMER_OPTIONS:
            nav_btn = self.create_nav_button(container=nav_frame, txt=key)
            nav_btn.grid(column=nav_col, padx=6, row=0)
            nav_col += 1

        # Set the initial nav button active
        opt = TIMER_OPTIONS[0][0]
        self.switch_timer(self.nav_buttons[opt], opt)

    def create_nav_button(self, container, txt):
        """
        Helper method to create navigation buttons
        """
        nav_btn = CTkButton(
            container,
            text=txt.title(),
            font=(TEXT["font-family"], 13),
            text_color=TEXT["light"],
            hover_color=BTN["bg"],
            bg_color=BTN["nav-bg"],
            fg_color=BTN["nav-bg"],
            border_color=BTN["bg"],
            border_width=1,
            width=120,
            height=35,
            text_color_disabled=BTN["inactive"],
            state="normal",
        )
        nav_btn.configure(
            command=lambda nav_ref=nav_btn, key=txt: self.switch_timer(nav_ref, key)
        )

        # Handler mouse hover and leave
        nav_btn.bind(
            "<Enter>",
            lambda event, ref=nav_btn: self.nav_on_hover_exit(event, ref, "in"),
        )
        nav_btn.bind(
            "<Leave>",
            lambda event, ref=nav_btn: self.nav_on_hover_exit(event, ref, "out"),
        )

        self.nav_buttons[txt] = nav_btn
        return nav_btn

    def nav_on_hover_exit(self, _, ref, type):
        """
        Control navigation button behavior
        Args:
            _ (Event): button event
            ref (CTkButton): navigation button reference
            type (str): hover(in) or leave(out)
        """
        is_active = ref.cget("hover")
        state = ref.cget("state")
        # If button is not disabled and allowed hover, then customize the behavior
        if is_active and state != "disabled":
            ref.configure(fg_color=NAV_HOVER[type][0], text_color=NAV_HOVER[type][1])

    def setup_countdown_display(self):
        """
        Canvas widget that display the countdown
        """
        self.canvas = CTkCanvas(
            width=350, height=350, background=WINDOW["bg"], highlightthickness=0
        )
        self.canvas.create_oval(10, 10, 340, 340, width=1, outline=TEXT["light"])
        self.countdown_txt = self.canvas.create_text(
            175,
            175,
            text=self.timer.countdown_text(
                minutes=self.settings.active_timer_duration()
            ),
            font=(TEXT["font-family"], 92, "bold"),
            fill=TEXT["light"],
        )
        self.canvas.grid(column=0, row=1, columnspan=3, sticky="s")

    def start_reset_button(self):
        """
        Button widget to start and reset the timer
        """
        self.start_reset_btn = CTkButton(
            self.window,
            text="START",
            font=(TEXT["font-family"], 14),
            bg_color=BTN["nav-bg"],
            fg_color=BTN["bg"],
            hover_color=BTN["hover"],
            text_color=TEXT["dark"],
            image=self.play_ico,
            compound="left",
            height=40,
            width=140,
            command=self.launch_timer,
        )
        self.start_reset_btn.grid(column=0, row=2, pady=40, columnspan=3, sticky="n")

    def setup_setting_btn(self):
        settings_btn = CTkButton(
            self.window,
            image=self.settings_ico,
            text="",
            width=30,
            height=30,
            fg_color=BTN["nav-bg"],
            bg_color=BTN["nav-bg"],
            hover=False,
            command=self.settings.open_window,
        )
        settings_btn.place(x=25, y=30)

    def switch_timer(self, nav_ref, value):
        """
        Navigate across different timers and reset the countdown
        """
        if self.timer.is_running():
            return
        # Reset BG & Txt color in all nav widgets
        for _, ref in self.nav_buttons.items():
            ref.configure(fg_color=BTN["nav-bg"], text_color=TEXT["light"], hover=True)
        # Set active BG & Txt color for current nav
        nav_ref.configure(fg_color=BTN["bg"], text_color=TEXT["dark"], hover=False)

        self.settings.switch_timer_option(value)
        self.refresh_countdown(minutes=self.settings.active_timer_duration())

    def refresh_countdown(self, minutes=0, seconds=None):
        """
        Updates the countdown text
        """
        if self.canvas:
            self.canvas.itemconfig(
                self.countdown_txt,
                text=self.timer.countdown_text(minutes=minutes, seconds=seconds),
            )

    def launch_timer(self):
        """
        Begin the timer
        """
        # Timer is already running. So, stop and reset countdown
        if self.timer.is_running():
            self.clear_timer()
            return

        # Disable navigation buttons while timer is running
        for _, ref in self.nav_buttons.items():
            ref.configure(state="disabled")

        self.timer.start()
        self.start_reset_btn.configure(text="STOP", image=self.stop_ico)
        seconds = self.settings.active_timer_duration() * 60
        self.countdown(seconds)

    def countdown(self, seconds):
        """
        Track the countdown and refreshes the countdown text every second
        """
        if seconds <= 0:
            self.clear_timer()
            return

        seconds -= 1
        # Update UI timer text
        self.refresh_countdown(seconds=seconds)
        self.timer_id = self.window.after(1000, self.countdown, seconds)

    def clear_timer(self):
        """
        Reset all time timer process
        """
        # Kill the scheduled countdown
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        # Enable navigation buttons
        for _, ref in self.nav_buttons.items():
            ref.configure(state="normal")

        self.timer.stop()
        self.refresh_countdown(minutes=self.settings.active_timer_duration())
        self.start_reset_btn.configure(text="START", image=self.play_ico)

    def configs_updated(self):
        if not self.timer.is_running():
            self.refresh_countdown(minutes=self.settings.active_timer_duration())


window = CTk()
app = TimerApp(window)
window.mainloop()
