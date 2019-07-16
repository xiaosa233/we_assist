from models import base
import tcp_server
from net_protocol_component import net_protocol_component

class net_server_component(base.base):
    def __init__(self, controller, accept_port, override_msg_cb = None):
        super().__init__()
        self.server = None
        self.accept_port = accept_port
        self.controller = controller
        self.msg_cb = override_msg_cb
        self.protocol_component = None


    def initialize(self):
        self.protocol_component = self.controller.get_component('net_protocol_component')
        if self.msg_cb is None:
            self.msg_cb = self.default_msg_cb

        self.server = tcp_server.tcp_server('0.0.0.0', self.accept_port, msg_cb=self.msg_cb)
        self.server.start()

    def destroy(self):
        super().destroy()
        self.server.stop()


    def default_msg_cb(self, tcp_connection, msg):
        if self.protocol_component :
            self.protocol_component.on_msg(tcp_connection, msg)


    def broadcast_log(self, log_msg):
        if self.server :
            data = net_protocol_component.event_name['log']+'!'+log_msg + '`'
            self.server.broadcast(data.encode())

    def broadcast(self, data):
        if self.server:
            data = data + '`'
            self.server.broadcast(data.encode())