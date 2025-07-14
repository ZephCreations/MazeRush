import threading
from .AppServer import Server
from .AppClient import Client


def start_server(host, port):
    server = Server(host, port)

    server_thread = threading.Thread(target=server.start_server, args=())

    server_thread.start()

    return server


def join_server(name, host, port, game_screen):
    client = Client(name, host, port, game_screen)
    client_thread = threading.Thread(target=client.start_connection, args=())
    client_thread.start()
    return client

