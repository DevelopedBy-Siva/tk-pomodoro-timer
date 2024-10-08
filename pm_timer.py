import datetime


class Timer:
    def __init__(self):
        self.running = False

    def countdown_text(self, minutes=0, seconds=None):
        if not seconds:
            seconds = minutes * 60
        countdown = str(datetime.timedelta(seconds=seconds))
        hrs_index = str(countdown).index(":") + 1
        return countdown[hrs_index:]

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running
