import tcp_client_base
import threading
import enum from Enum


class eclient_state(Enum):
    unvalid = 0
    connecting = 1

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
        self.client_state = eclient_state.unvalid

    def connect(self):
        self.is_connected = True
        if self.run_thread is None :
            self.client_state = eclient_state.connecting
            self.run_thread  = threading.Thread(target=self.client_loop)
            self.run_thread.start()

    def close(self):
        self.is_connected = False

    def on_connected_cb(self):
        self.start_work()
        if self.connected_cb :
            self.connected_cb()

    def on_error_cb(self):
        self.stop_work()
        if self.error_cb :
            self.error_cb()


    def client_loop(self):
        while self.is_connected:
            if self.client_state == eclient_state.connecting:
                connect_impl()

    #virtual
    def on_msg(self, data):
        print(data.decode())
        if self.msg_cb:
            self.msg_cb() #new msg
