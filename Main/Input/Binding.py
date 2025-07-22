from Events import Event
from Logging import create_logger

logger = create_logger("BINDINGS")


class Binding:

    def __init__(self):
        self.trigger_event : Event = Event()
        self.__active = True
        logger.debug("Binding added")

    def _trigger(self, *args):
        if self.__active:
            self.trigger_event.trigger(*args)

    def disable_binding(self):
        self.__active = False

    def enable_binding(self):
        self.__active = True

