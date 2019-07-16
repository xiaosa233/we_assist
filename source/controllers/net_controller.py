import base_controller
from modules.io_mod import net_server_component
from modules.io_mod.net_protocol_component import net_protocol_component
import time

from utils.function_dispatcher import function_dispatcher

class net_controller (base_controller.base_controller):
    default_port=23332

    def __init__(self):
        super().__init__()
        self.server_component = None
        self.dispatcher = function_dispatcher.open()

        self.dispatcher['update_state'].add(self.on_update_state)

    def initialize(self):
        super().initialize()
        self.server_component = net_server_component.net_server_component(self, net_controller.default_port)
        self.components.append( self.server_component)
        protocol_component = net_protocol_component(self)
        self.setup_event(protocol_component)
        self.components.append(protocol_component)

        for it in self.components :
            it.initialize()

    def destroy(self):
        super().destroy()
        self.dispatcher['update_state'].remove(self.on_update_state)

    def setup_event(self, component):
        component.register_event(net_protocol_component.event_name['ask_state'], self.on_ask_now_state)

    def sendout_log(self, log):
        if self.server_component :
            self.server_component.broadcast_log(log)

    def send_arrive(self):
        if self.server_component:
            msg = net_protocol_component.event_name['arrive']+'!'+str(time.time())
            self.server_component.broadcast(msg)

    def on_ask_now_state(self, tcp_base, data):
        out_data = []
        self.dispatcher['ask_now_state'](out_data)
        #send state
        if len(out_data) > 0 :
            msg = net_protocol_component.event_name['asw_state'] + '!' + out_data[0]+'`'
            tcp_base.send(msg.encode())
            print(' send state ', msg)

    def on_update_state(self, state):
        if self.server_component:
            msg = net_protocol_component.event_name['asw_state'] + '!' + state
            self.server_component.broadcast(msg)