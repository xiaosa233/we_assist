import tcp_client_base
import threading
import asyncio
import time
class tcp_server_connection(tcp_client_base.tcp_client_base):
    def __init__(self, accept_server, reader, writer):
        super().__init__()
        self.reader = reader
        self.writer = writer
        self.accept_server = accept_server

        self.is_recv_ok = False


    #virtual
    def close(self):
        super().close()
        self.accept_server.close_connection(self)

    #virtual
    async def client_tick(self, delta):
        await super().work(delta)

    # virtual
    def on_msg(self, data):
        self.is_recv_ok = True
        self.accept_server.on_msg(self, data)

    # virtual
    def on_read_error(self, exception):
        self.accept_server.on_read_error(self, exception)

    async def recv_once(self):
        self.is_recv_ok = False
        await super().work(0)

        if self.is_recv_ok :
            asyncio.get_event_loop().create_task(self.recv_once())