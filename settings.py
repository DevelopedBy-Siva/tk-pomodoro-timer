from customtkinter import *
from CTkSpinbox import CTkSpinbox

from constants import *


class Settings:

    def __init__(self, root):
        self.root = root
        self.popup = None
        self.configs = self.load_configs()
        self.user_inputs = {}
        self.setup_window()

    def setup_window(self):
        """
        Draw the top level window for settings
        """
        self.popup = CTkToplevel(self.root)
        self.close_window()
        self.popup.title(WINDOW["settings"]["title"])
        self.popup.config(background=WINDOW["bg"])
        self.popup.geometry(
            f'{WINDOW["settings"]["width"]}x{WINDOW["settings"]["height"]}'
        )
        # Disable window resizing
        self.popup.resizable(False, False)
        # Handle the close (X) button event
        self.popup.protocol("WM_DELETE_WINDOW", self.close_window)

        user_input_frame = CTkFrame(
            self.popup, fg_color=WINDOW["bg"], bg_color=WINDOW["bg"]
        )

        for idx, opt in enumerate(self.configs):
            # Input box label
            input_label = CTkLabel(
                user_input_frame,
                text=opt.title(),
                font=(TEXT["font-family"], 15),
                text_color=TEXT["light"],
            )
            input_label.grid(column=0, row=idx, padx=15, pady=15, sticky="w")

            # User input
            input_box = CTkSpinbox(
                user_input_frame,
                width=100,
                height=40,
                font=(TEXT["font-family"], 13),
                step_value=1,
                min_value=self.configs[opt],
                max_value=TIMER_LIMIT,
                button_color=BTN["bg"],
                text_color=TEXT["dark"],
                fg_color=BTN["nav-bg"],
                # background=BTN["nav-bg"],
                # borderwidth=1,
                # highlightthickness=0,
                # font=(TEXT["font-family"], 18),
                # from_=1,
                # to=TIMER_LIMIT,
            )
            input_box.grid(column=1, row=idx, padx=10, pady=15)
            self.user_inputs[opt] = input_box

            # Input units label
            units_label = CTkLabel(
                user_input_frame,
                text="minutes",
                font=(TEXT["font-family"], 15),
                text_color=TEXT["light"],
            )
            units_label.grid(column=2, row=idx, padx=10, pady=15)

        # Align the user input boxes to the center
        user_input_frame.place(relx=0.5, rely=0.4, anchor="center")

        save_btn = CTkButton(
            self.popup,
            text="Save",
            font=(TEXT["font-family"], 14),
            bg_color=BTN["nav-bg"],
            fg_color=BTN["bg"],
            hover_color=BTN["hover"],
            text_color=TEXT["dark"],
            height=30,
            width=100,
            command=self.capture_configs,
        )
        save_btn.place(relx=0.5, rely=0.82, anchor="center")

    def capture_configs(self):
        """
        Get values from spinbox and save it
        """
        options = []
        for opt, val in self.user_inputs.items():
            options.append((opt, val.get()))
        self.__save_configs(options)
        # Load new configs
        self.configs = {key: value for key, value in options}
        # Close window after saving
        self.close_window()

    def open_window(self):
        """
        Open settings window
        """
        if self.popup is not None:
            self.popup.deiconify()

    def close_window(self):
        """
        Close settings window
        """
        if self.popup is not None:
            self.popup.withdraw()

    def load_configs(self):
        """
        Load user settings
        Returns:
            dict: timer settings
        """
        configs = {}
        try:
            with open(CONFIG_FILE_NAME, mode="r") as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]
                for line in lines:
                    key, value = line.split("=")
                    time = int(value)
                    if time > TIMER_LIMIT:
                        raise ValueError(f"Time cannot be greater than {TIMER_LIMIT}")
                    configs[key] = time
        except:
            self.__save_configs()
        return {key: configs.get(key, value) for key, value in TIMER_OPTIONS}

    def __save_configs(self, timer_options=TIMER_OPTIONS):
        """
        If no user settings found, create default settings
        """
        with open(CONFIG_FILE_NAME, mode="w") as file:
            options = ""
            for key, value in timer_options:
                options += f"{key}={value}\n"
            file.write(options)
