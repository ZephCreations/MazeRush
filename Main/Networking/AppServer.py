import logging
import socket
import selectors
import traceback
from .libServer import Message
from .Exceptions import ClientDisconnectedException

from Logging import create_logger
logger = create_logger("SERVER")


class Server:
    def __init__(self, host, port):
        # Set sel value to default
        self.sel = selectors.DefaultSelector()
        self.HOST = host
        self.PORT = port

        # self.conn = self.addr = None
        # self.message = None
        self.lsock = None

    def start_server(self):
        # Create socket
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        # Servers remain with packets as a safeguard to ensure they aren't
        #   sent to wrong address, using this option circumnavigates the error
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind((self.HOST, self.PORT))
        self.lsock.listen()
        logger.info(f"Listening on {(self.HOST, self.PORT)}")
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                # Blocking, waiting for events
                logger.debug("Waiting ... ")
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    logger.debug(f"Event \"{key.data}\" ... ")
                    if key.data is None:
                        # Accept Connection from Client
                        self.accept_wrapper(key.fileobj)
                    else:
                        # Process Data from Client
                        # Get reference to message object using key.data
                        message = key.data
                        try:
                            message.process_events(mask)
                        except ClientDisconnectedException as e:
                            print(e)
                            self.close_wrapper(message)
                            break
                        except Exception:
                            logger.error(
                                f"Main: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            self.close_wrapper(message)
                            break
        except KeyboardInterrupt:
            logger.info("Caught keyboard interrupt, exiting")
        finally:
            if self.lsock is None:
                return
            self.close_server()

    def add_message(self, conn, addr):
        # print("Added Message")
        # Create message object
        # Associated with socket from sel.register(), initially set to be monitored
        #   for read events only
        message = Message(self, self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)

    def accept_wrapper(self, sock):
        # When events are ready on the socket they are returned by selector.select()
        conn, addr = sock.accept()
        logger.info(f"Accepted connection from {addr}")
        conn.setblocking(False)
        self.add_message(conn, addr)

    def close_wrapper(self, message):
        conn = message.sock
        addr = message.addr
        logger.info(f"Closing connection to {addr}")
        try:
            message.close(False)
            # conn.close()
        except OSError as e:
            logger.error(f"Error: conn.close() exception for {addr}: {e!r}")
        logger.info(f"Closed message wrapper connection to {addr}")

    def close_server(self):
        logger.info("Closing Server")
        self.sel.close()
        # Delete reference to socket object for garbage collection
        self.lsock = None
        logger.info(f"Stopped Listening on ({self.HOST})")


if __name__ == "__main__":
    server = Server(socket.gethostbyname(socket.gethostname()), 65432)
    server.start_server()

