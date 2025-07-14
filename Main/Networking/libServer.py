import sys
import selectors
import json
import io
import struct
from .Exceptions import ClientDisconnectedException

from Logging import create_logger
logger = create_logger("SERVER")

# If searching for content on the SERVER, this is said content.

# request_search = {
#     "morpheus": "Follow the white rabbit. \U0001f430",
#     "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
#     "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
# }

data = {}
last_player_update = None


class Message:
    def __init__(self, server, selector, sock, addr):
        self.server = server
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

    def _set_selector_events_mask(self, mode):
        # Set selector to listen for events: mode is 'r', 'w', or 'rw'.
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        except ConnectionResetError:
            logger.error("PEER DISCONNECTED: fail receive\n")
            # self.close(False)
            # self.server.close_wrapper()
            raise RuntimeError("Peer Disconnected")
        else:
            if data:
                self._recv_buffer += data
            else:
                logger.debug("======================\n"
                             "PEER CLOSED: No data\n"
                             "======================")
                # self.close(False)
                # self.server.close_wrapper()
                raise ClientDisconnectedException(self.addr)

    def _write(self):
        # If send buffer has content
        if self._send_buffer:
            logger.info(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    logger.debug("======================"
                                 "    CLOSING NORMAL    "
                                 "======================")
                    self.close()

    def _json_encode(self, obj, encoding):
        # encode obj using with the encoding "encoding"
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        # convert json text to content
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        # convert to object and then close json text
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
            self, *, content_bytes, content_type, content_encoding
    ):
        # Format json header
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        # Convert to bytes
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        # Set the two byte message header
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        # Create the message with the proto_header, header, and content
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    # TODO content processing here
    def _create_response_json_content(self):
        # Get action from JSON content
        action = self.request.get("action")

        # TODO actual game stuff goes here.
        if action == 'update':
            player = self.request.get("player")
            # print(player)
            moves = self.request.get("value")
            if player is not None:
                # print(f"{data}    {player}")
                # print(type(player))
                data[player].append(moves)

                content = {"result": f"Moves: {moves}"}
        elif action == 'join':
            player = self.request.get("player")
            data[player] = []
            content = {"id": f"{len(data)}", "player": f"{self.request.get('player')}"}
        else:
            # Otherwise return invalid action
            content = {"result": f"Error: invalid action '{action}'."}
        # Set the encoding and return the response
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        logger.debug(f"Processed request from {self.addr}")
        return response

    def _create_response_binary_content(self):
        # IDK ... witchcraft here.
        response = {
            "content_bytes": b"First 10 bytes of request: "
                             + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def process_events(self, mask):
        # If socket is available to read, read
        if mask & selectors.EVENT_READ:
            self.read()
        # If socket is available to write, write
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        # Call read function (get data)
        self._read()

        # Check and process (create) proto header
        if self._jsonheader_len is None:
            self.process_protoheader()

        # Check and process (create) json header
        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        # Check and process (create) content
        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        # If there is a request, and one hasn't been created, create one
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def close(self, new_message=True):

        # Close the connection (and message)
        # Unregister the socket
        logger.info(f"Closing message connection")
        try:
            self.selector.unregister(self.sock)
            # # Added stuff
            # if new_message:
            #     self.server.add_message(self.sock, self.addr)
            self.sock = None
            logger.info(f"Closed message connection to {self.addr}")
        except Exception as e:
            logger.error(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )

        # Close the Socket
        # try:
        #     self.sock.close()
        # except OSError as e:
        #     print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        # finally:
        #     # Delete reference to socket object for garbage collection
        #     self.sock = None

    def process_protoheader(self):
        # Two byte header in network (big-endian) byte order
        # Contains the length of the JSON header
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            # decode the value, read it and store in
            #   self._jsonheader_len
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            # Remove from receive buffer
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            # Decode and deserialize the JSON into a dictionary
            #   Saved to self.jsonheader
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            # Remove header from receive buffer (checking if
            #   anything is missing)
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                    "byteorder",
                    "content-length",
                    "content-type",
                    "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")

    def process_request(self):
        # Check all the message is received
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        # Save message to the data variable
        data = self._recv_buffer[:content_len]
        # Remove from receive buffer
        self._recv_buffer = self._recv_buffer[content_len:]
        # If the content is JSON, decode and serialize,
        #   otherwise it is binary
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            logger.info(f"Received request {self.request!r} from {self.addr}")
        else:
            # Binary or unknown content-type
            self.request = data
            logger.info(
                f"Received {self.jsonheader['content-type']} "
                f"request from {self.addr}"
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self):
        # Create JSON response
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        # Create Binary response
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        # Create message using generated response
        message = self._create_message(**response)
        # Set response_created to True so .write() isn't called again
        self.response_created = True
        # Append response to send buffer (seen and send by ._write())
        self._send_buffer += message
