import sys
import selectors
import json
import io
import struct

from Events import player_joined

from Logging import create_logger
logger = create_logger("CLIENT")


class Message:
    def __init__(self, selector, sock, addr, request, game_screen):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request
        self.game_screen = game_screen
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
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
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

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

    def _json_encode(self, obj, encoding):
        # Encode obj using with the encoding "encoding"
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        # Convert json text to text wrapper
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        # Convert to object and then close json text
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

    def _process_response_json_content(self):
        # Get return value and print result
        content = self.response
        if 'result' in content:
            result = content.get("result")
            logger.info(f"Got result: {result}")
        # TODO Do something herese
        elif 'id' in content:
            player_id = content.get("id")
            logger.debug(f"Got ID: {player_id}")
            player = self.game_screen.game.create_player(content.get("player"), player_id, True)
            self.game_screen.game.add_player(player)

    def _process_response_binary_content(self):
        # Get return value and print result
        content = self.response
        logger.info(f"Got response: {content!r}")

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
            if self.response is None:
                self.process_response()

    def write(self):
        # If a request is not queued, queue the request
        if not self._request_queued:
            # Create new request and add to send buffer
            self.queue_request()

        self._write()

        # Tell selector.select() to stop monitoring the socket for write requests
        if self._request_queued:
            if not self._send_buffer:
                # Set selector to listen for read events, we're done writing.
                self._set_selector_events_mask("r")

    def close(self):
        # Close the connection
        # Unregister the socket
        logger.info(f"Closing MESSAGE connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            logger.error(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )
        finally:
            self.sock = None

        # # Close the socket
        # try:
        #     self.sock.close()
        # except OSError as e:
        #     print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        # finally:
        #     # Delete reference to socket object for garbage collection
        #     self.sock = None

    def queue_request(self):
        # Read the dictionary from the main Client to get the data
        content = self.request["content"]
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        # Request message is created and appended to the send buffer
        # This is then seen by and sent by ._write()
        message = self._create_message(**req)
        self._send_buffer += message
        # The state variable self._request_queued is set so that
        #   .queue_request() isn't called again
        self._request_queued = True
        # Client then waits for a response from the server

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
            # Remove from recieve buffer
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            # Decode and deserialize the JSON into a dictionary
            #   Saved to self.jsonheader
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            # Remove header from recieve buffer (checking if
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

    def process_response(self):
        # Get content length
        content_len = self.jsonheader["content-length"]
        # If receive buffer is smaller than the content length,
        # return as not all content is received
        if not len(self._recv_buffer) >= content_len:
            return
        # Get the message (excluding the headers)
        data = self._recv_buffer[:content_len]
        # Remove the message from receive buffer
        self._recv_buffer = self._recv_buffer[content_len:]
        # If the content is JSON, decode and serialize,
        #     otherwise, it is binary
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.response = self._json_decode(data, encoding)
            logger.info(f"Received response {self.response!r} from {self.addr}")
            # Process response
            self._process_response_json_content()
        else:
            # Binary or unknown content-type
            self.response = data
            logger.info(
                f"Received {self.jsonheader['content-type']} "
                f"response from {self.addr}"
            )
            # Process response
            self._process_response_binary_content()
        # Close when response has been processed
        logger.debug("About to close")
        self.close()

    def __str__(self):
        return str(self.request.get("content"))
