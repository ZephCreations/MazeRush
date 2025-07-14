from ActionMap import ActionMap


class InputController:

    def __init__(self, player=1):
        self.__action_maps: [ActionMap] = []
        self.player = player

    def add_map(self, action_map: ActionMap):
        if action_map in self.__action_maps: return
        self.__action_maps.append(action_map)

    def get_map(self, name) -> ActionMap:
        for action_map in self.__action_maps:
            if action_map.name == name:
                return action_map
            else:
                raise RuntimeError("Input Map does not exist")

    def remove_map(self, action_map: ActionMap):
        if action_map not in self.__action_maps: return
        self.__action_maps.remove(action_map)


if __name__ == "__main__":
    import tkinter as tk
    from KeyboardBindings import KeyboardBindings
    from Action import Action
    root = tk.Tk()
    controller = InputController()
    A = ActionMap("Player_1")
    a = Action("Move_Right")
    controller.add_map(A)
    controller.get_map("Player_1").add_action(a)

    b = [KeyboardBindings(root, "<d>"),
         KeyboardBindings(root, "<D>"),
         KeyboardBindings(root, "<Right>")]

    for binding in b:
        controller.get_map("Player_1").get_action("Move_Right").add_binding(binding)

    def onMove(player, *args):
        print(player, *args)

    a.onAction.add_listener(lambda *args: onMove(1, *args))

    root.mainloop()

