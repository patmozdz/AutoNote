class Keybind:
    def __init__(self, name: str, description: str, key: str, action, action_params: tuple = ()):
        """
        :param name: The name of the keybind (eg "save")
        :param description: The description of the keybind (eg "Saves last 3 minutes")
        :param key: The key to activate keybind TODO: Make it so that it can have key combos as well
        :param action: A function to call when calling self.play_action()
        :param action_params: Optional. Must be a tuple even if single value (eg action_params=(42,))
        :return:
        """
        self.name = name
        self.description = description
        self.key = key
        self.action = action
        # As seen above, action_params is an empty tuple if none were given. This makes *action_params work correctly,
        # whether parameters were given or not.
        self.action_params = action_params

    def play_action(self):
        self.action(*self.action_params)

    def __str__(self):
        return f"{self.key}: {self.description}"

    # TODO: DELETE ALL BELOW, keybinds should be handled by reassigning a Keybind in the list to a new instance of Keybind with new values. (create_replay_keybind function?)
    def reassign_key(self, new_key):
        self.key = new_key

    def reassign_action(self, new_action, new_action_params: tuple = ()):
        self.action = new_action
        self.action_params = new_action_params
