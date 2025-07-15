from .Action import Action
from Logging import create_logger

logger = create_logger("ACTION_MAP")


class ActionMap:

    def __init__(self, name):
        self.name: str = name
        self.active = True
        self.__actions = []

    def add_action(self, action: Action):
        if any(action.name == _action.name for _action in self.__actions):
            logger.warning(f"Action '{action.name}' already exists")
            return
        self.__actions.append(action)

    def get_action(self, name) -> Action | None:
        for action in self.__actions:
            if action.name == name:
                return action
        # No matching actions found
        logger.warning(f"Action '{name}' does not exist")
        return None

    def remove_action(self, action: Action):
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

    def debug_display(self):
        return str(self.__actions)

    def __repr__(self):
        return self.name
