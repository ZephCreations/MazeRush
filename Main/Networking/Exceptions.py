

class ClientDisconnectedException(Exception):
    def __init__(self, addr, msg="Client Disconnected"):
        self.addr = addr
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.addr} -> {self.msg}'

