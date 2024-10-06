from constants import TIMER_OPTIONS, CONFIG_FILE_NAME


class Settings:

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
                    configs[key] = int(value)
        except:
            self.__save_default_configs()
        return {key: configs.get(key, value) for key, value in TIMER_OPTIONS}

    def __save_default_configs(self):
        """
        If no user settings found, create default settings
        """
        with open(CONFIG_FILE_NAME, mode="w") as file:
            options = ""
            for key, value in TIMER_OPTIONS:
                options += f"{key}={value}\n"
            file.write(options)
