from Events import Event
from .Binding import Binding
from Logging import create_logger

logger = create_logger("BINDINGS")


class Action:

    def __init__(self, name):
        self.name: str = name
        self.onAction = Event()
        self.active = True
        self.__bindings = []

    def add_binding(self, binding: Binding):
        if binding in self.__bindings:
            return
        self.__bindings.append(binding)
        # Trigger action when binding is triggered
        binding.trigger_event.add_listener(self.__trigger)

    def remove_binding(self, binding: Binding):
        if binding not in self.__bindings:
            return
        self.__bindings.remove(binding)
        binding.trigger_event.remove_listener(self.__trigger)

    def __trigger(self, *args):
        # self.onAction.trigger(self.name, *args)
        self.onAction.trigger(*args)

    def disable_action(self):
        self.active = False
        for binding in self.__bindings:
            binding.disable_binding()

    def enable_action(self):
        self.active = True
        for binding in self.__bindings:
            binding.enable_binding()

    def __repr__(self):
        return f"{self.name}  {self.__bindings}"

