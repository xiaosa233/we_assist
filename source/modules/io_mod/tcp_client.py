import tcp_client_base
from enum import Enum
import asyncio


class eclient_state(Enum):
    unvalid = 0
    connecting = 1
    work = 2

class tcp_client(tcp_client_base.tcp_client_base):
    def __init__(self, ip, port, connected_cb = None , error_cb = None, msg_cb = None):
        super().__init__()
        self.ip = ip
        self.port = port
        self.connected_cb = connected_cb
        self.error_cb = error_cb
        self.msg_cb = msg_cb
        self.client_state = eclient_state.unvalid

    def connect(self):
        self.client_state = eclient_state.connecting
        super().start_work()

    def close(self):
        self.client_state = eclient_state.unvalid
        super().close()

    #virtual
    async def client_tick(self, delta):
        if self.client_state == eclient_state.connecting :
            #connected
            try:
                self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
                self.on_connected_cb()
                self.client_state = eclient_state.work
            except Exception as e:
                self.on_error_cb(e)

        elif self.client_state == eclient_state.work :
            await super().work(delta) #super.work



    #virtual
    def on_msg(self, data):
        if self.msg_cb:
            self.msg_cb(self, data) #new msg

    #virtual
    def on_read_error(self, exception):
        self.on_error_cb(exception)
        if exception.errno == 10054 or exception.errno == 10053: #force to close
            self.reader = None 
            self.writer = None
        if self.client_state == eclient_state.work:
            self.client_state = eclient_state.connecting #make it reconnect


    def close(self):
        self.is_connected = False

    def on_connected_cb(self):
        if self.connected_cb :
            self.connected_cb(self)

    def on_error_cb(self, exception):
        if self.error_cb :
            self.error_cb(self, exception)

        #reconnected
