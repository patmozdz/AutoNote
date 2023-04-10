import os


class Keybind:
    def __init__(self, name: str, description: str, default_key: str, action, action_params: tuple = ()):
        """
        :param name: The name of the keybind (eg "save")
        :param description: The description of the keybind (eg "Saves last 3 minutes")
        :param default_key: The default key to activate keybind TODO: Make it so that it can have key combos as well
        :param action: The function to call when calling self.play_action()
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
        self.action(*self.action_params)

    def __str__(self):
        return f"{self.get_key()}: {self.description}"

    def reassign_key(self, new_key):
        self.custom_key = new_key

    def get_key(self):
        if self.custom_key is None:
            return self.default_key
        else:
            return self.custom_key

    def set_to_default(self):
        self.custom_key = None

    # Below makes the objects hashable (can put the objects into a set and search by name directly)
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other_name):
        return self.name == other_name


# TODO: Modify below so that it reads from a file to get keybinds, creates new file with default keybinds if none found
if not os.path.exists("config.json"):
    # "config.json" = default_keybinds.convert_to_json
    pass

# current_keybinds = json.read
