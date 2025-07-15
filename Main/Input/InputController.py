from .ActionMap import ActionMap
from Logging import create_logger

logger = create_logger("INPUT_CONTROLLER")


class InputController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InputController, cls).__new__(cls)
            # Create class variables
            cls._instance._action_maps = []
            logger.debug("Created Input Controller instance")
        return cls._instance

    def __init__(self):
        self._action_maps: [ActionMap]

    def add_map(self, action_map: ActionMap):
        if any(action_map.name == _action_map.name for _action_map in self._action_maps):
            logger.warning("Action Map name already exists")
            return
        self._action_maps.append(action_map)

    def get_map(self, name) -> ActionMap | None:
        for action_map in self._action_maps:
            if action_map.name == name:
                return action_map
            else:
                logger.warning("Action Map does not exist")
                return None

    def remove_map(self, action_map: ActionMap):
        if action_map not in self._action_maps: return
        self._action_maps.remove(action_map)


if __name__ == "__main__":
    import tkinter as tk
    from KeyboardBindings import KeyboardBindings
    from Action import Action
    root = tk.Tk()

    # Create Controller
    controller = InputController()

    # Add actions and map
    A = ActionMap("Player_1")
    A2 = ActionMap("Player_1")
    a = Action("Move_Right")
    controller.add_map(A)
    controller.add_map(A2)
    controller.get_map("Player_1").add_action(a)

    # Bindings list
    b = [KeyboardBindings(root, "<d>"),
         KeyboardBindings(root, "<D>"),
         KeyboardBindings(root, "<Right>")]

    # Add Bindings
    for binding in b:
        InputController().get_map("Player_1").get_action("Move_Right").add_binding(binding)

    def on_move(player, *args):
        print(player, *args)

    a.onAction.add_listener(lambda *args: on_move(1, *args))

    root.mainloop()

