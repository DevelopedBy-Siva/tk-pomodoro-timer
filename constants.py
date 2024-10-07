# Assets
ASSETS = {
    "play": "./static/play.png",
    "stop": "./static/stop.png",
    "settings": "./static/settings.png",
}

# Window
WINDOW = {
    "title": "ZenFocus",
    "bg": "#798645",
    "width": 840,
    "height": 680,
    "txt": "#FEFAE0",
    "settings": {
        "width": 440,
        "height": 360,
        "title": "ZenFocus Settings",
    },
}

# Button
BTN = {
    "bg": "#FEFAE0",
    "nav-bg": "#798645",
    "hover": "#F2EED7",
    "inactive": "#B1AF9C",
}

# Spinbox
SPINBOX = {
    "fg": "#D6D6C2",
    "btn": "#C6C6B6",
    "btn-hover": "#C0C0AE",
}

# Timer options ("option name" : default timer value)
TIMER_OPTIONS = (
    ("pomodoro", 25),
    ("short break", 5),
    ("long break", 15),
)
# Timer limit in minutes
TIMER_LIMIT = 90

# Font
TEXT = {
    "font-family": "Ubuntu",
    "light": "#FEFAE0",
    "dark": "#181C14",
}

# Navigation buttons on hover/leave colors
NAV_HOVER = {
    "in": (BTN["bg"], TEXT["dark"]),
    "out": (BTN["nav-bg"], TEXT["light"]),
}

# User settings file
CONFIG_FILE_NAME = "configs.txt"
