import tcp_client_base
from tcp_system import tcp_system

class tcp_client(tcp_client_base.tcp_client_base):
    def __init__(self, ip, port, connected_cb = None , error_cb = None, msg_cb = None):
        super().__init__()
        self.ip = ip
        self.port = port
        self.connected_cb = connected_cb
        self.error_cb = error_cb
        self.msg_cb = msg_cb
        self.is_connected = False
        self.run_thread = None

    def connect(self):
        self.is_connected = True
        tcp_system.static_get().add_client(self)
        tcp_system.static_get().run()

    def close(self):
        self.is_connected = False
        tcp_system.static_get().remove_client(self)

    def on_connected_cb(self):
        self.start_work()
        if self.connected_cb :
            self.connected_cb()

    def on_error_cb(self):
        self.stop_work()
        if self.error_cb :
            self.error_cb()


    async def client_loop(self):

        pass

    #virtual
    def on_msg(self, data):
        print(data.decode())
        if self.msg_cb:
            self.msg_cb() #new msg
