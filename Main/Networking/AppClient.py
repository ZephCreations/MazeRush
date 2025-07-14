
import socket
import selectors
import traceback

from .libClient import Message
import tkinter as tk

from Logging import create_logger
logger = create_logger("CLIENT")


class Client:
    def __init__(self, player, host, port, game_screen):
        self.sel = selectors.DefaultSelector()
        self.HOST = host
        self.PORT = port
        self.player = player
        self.game_screen = game_screen
        self.sock = None
        self.addr = (self.HOST, self.PORT)

        self.message = None

    def create_request(self, action, value):
        # TODO actual game processing here
        # Check what the action was and give a specific format
        # if action == "search":
        #     return dict(
        #         type="text/json",
        #         encoding="utf-8",
        #         content=dict(action=action, value=value),
        #     )
        logger.info("Creating Request")
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value, player=self.player),
        )
        # else:
        #     return dict(
        #         type="binary/custom-client-binary-type",
        #         encoding="binary",
        #         content=bytes(action + value, encoding="utf-8"),
        #     )

    def start_connection(self):
        # Create socket for server connection
        logger.info(f"Starting connection to {self.addr}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(self.addr)
        logger.info(f"Connected to {self.addr}")
        request = self.create_request('join', 0)
        self.send_message(request)

    def send_message(self, request):
        logger.info(f"Sending Message to {self.addr}")
        # Once the request is written, set to monitor for read events only
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # events = selectors.EVENT_WRITE
        # Message object associated with socket using sel.register()
        message = Message(self.sel, self.sock, self.addr, request, self.game_screen)
        self.sel.register(self.sock, events, data=message)

        try:
            while True:
                # Blocking waiting for input
                logger.debug("Waiting ... ")
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    logger.debug(f"Event {key.data} ... ")
                    message = key.data
                    try:
                        logger.debug(f"Process data ...")
                        message.process_events(mask)
                    except Exception:
                        logger.error(
                            f"Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                        self.close()
                        return
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    logger.info("Socket closed so go back to waiting")
                    break
        except KeyboardInterrupt:
            logger.info("Caught keyboard interrupt, exiting")
        logger.info(f"Message Completed")


    def close(self):
        # Call close on the message if it wasn't done already
        if self.message is not None:
            self.message.close()
        # Close the socket
        try:
            self.sock.close()
        except OSError as e:
            logger.error(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None
        # Close connection to selector
        logger.info(f"Closing Server Connection to {self.addr}")
        self.sel.close()
        quit()


def key_pressed(event):
    key = event.char
    if key in ("a", "A"):
        send_update("left")
    elif key in ("d", "D"):
        send_update("right")
    elif key in ("w", "W"):
        send_update("up")
    elif key in ("s", "S"):
        send_update("down")
    # print(event.char, event.keysym, event.keycode)


def send_update(value):
    request = client.create_request('update', value)
    client.send_message(request)


def button_pressed():
    logger.info("BUTTON: Closing Connection")
    client.close()
    quit()


if __name__ == "__main__":
    client = Client(1,
                    socket.gethostbyname(socket.gethostname()),
                    65432)

    # Connect to server:
    # HOST = socket.gethostbyname(socket.gethostname())
    # PORT = 65432
    client.start_connection()

    # Create and bind window
    window = tk.Tk()
    window.bind("<Key>", key_pressed)
    tk.Button(window, width=50, height=20, text="Exit", command=button_pressed).pack()
    window.mainloop()

    client.close()
