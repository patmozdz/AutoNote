import os


class Keybind:
    def __init__(self, name: str, description: str, default_key: str, action: str, action_params: tuple = ()):
        """
        :param name: The name of the keybind (eg "save")
        :param description: The description of the keybind (eg "Saves last 3 minutes")
        :param key: The key to activate keybind TODO: Make it so that it can have key combos as well
        :param action: The name of the function to call when calling self.play_action()
        :param action_params: Optional. Must be a tuple even if single value (eg action_params=(42,))
        :return:
        """
        self.name = name
        self.description = description
        self.default_key = default_key
        self.action = action
        # As seen above, action_params is an empty tuple if none were given. This makes *action_params work correctly,
        # whether parameters were given or not.
        self.action_params = action_params
        self.custom_key = None

    def play_action(self):
        function = locals().get(self.action)
        if function and callable(function):
            function(*self.action_params)
        else:
            print(f"Function '{self.action}' not found or is not callable.")

    def __str__(self):
        return f"{self.key}: {self.description}"

    def reassign_key(self, new_key):
        self.custom_key = new_key

    def get_key(self):
        if self.custom_key is None:
            return self.default_key
        else:
            return self.custom_key

    def set_to_default(self):
        self.custom_key = None


# TODO: Modify below so that it reads from a file to get keybinds, creates new file with default keybinds if none found
if not os.path.exists("config.json"):
    # "config.json" = default_keybinds.convert_to_json
    pass

# current_keybinds = json.read
