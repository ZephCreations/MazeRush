from Action import Action


class ActionMap:

    def __init__(self, name):
        self.name: str = name
        self.active = True
        self.__actions = []

    def add_action(self, action: Action):
        if action in self.__actions:
            return
        self.__actions.append(action)

    def get_action(self, name):
        for action in self.__actions:
            if action.name == name:
                return action
            else:
                raise RuntimeError("Action does not exist")

    def remove_binding(self, action: Action):
        if action not in self.__actions:
            return
        self.__actions.remove(action)

    def disable_map(self):
        self.active = False
        for action in self.__actions:
            action.disable_action()

    def enable_map(self):
        self.active = True
        for action in self.__actions:
            action.enable_action()



