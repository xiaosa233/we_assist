from models import base
from modules.io_mod import tcp_client
class net_client_component(base.base) :

    def __init__(self, controller, ip, port, error_cb = None, connected_cb = None):
        super().__init__()
        self.controller = controller
        self.protocol_component = None
        self.client = None
        self.ip = ip
        self.port = port
        self.error_cb = error_cb
        self.connected_cb = connected_cb


    def initialize(self):
        self.protocol_component = self.controller.get_component('net_protocol_component')
        msg_cb = None
        if self.protocol_component :
            msg_cb = self.protocol_component.on_msg

        self.client = tcp_client.tcp_client(self.ip, self.port, msg_cb=msg_cb, error_cb=self.error_cb, connected_cb=self.connected_cb)
        self.client.connect()


    def destroy(self):
        super().destroy()
        if self.client :
            self.client.close()

    def send(self, data):
        if self.client:
            data += '`'
            self.client.send(data.encode())
