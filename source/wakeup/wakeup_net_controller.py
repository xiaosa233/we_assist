from controllers import base_controller
from modules.io_mod import net_protocol_component
from modules.io_mod import net_client_component
from utils.function_dispatcher import function_dispatcher
import wakeup_check_component
import wakeup_state_component
import wakeup_sysexec_component

class wakeup_net_controller(base_controller.base_controller) :
    default_port = 23332
    def __init__(self):
        super().__init__()

    def initialize(self):
        super().initialize()

        function_dispatcher.open()['reset'].add(self.on_reset)

        protocol_component = net_protocol_component.net_protocol_component(self)
        self.components.append(protocol_component)
        self.components.append(net_client_component.net_client_component(self, '127.0.0.1', self.default_port, error_cb=self.on_error_cb, connected_cb=self.on_connected_cb))
        self.components.append(wakeup_check_component.wakeup_check_component(self, 60))
        self.components.append(wakeup_state_component.wakeup_state_component(self))
        self.components.append(wakeup_sysexec_component.wakeup_sysexec_component(self))
        for it in self.components :
            it.initialize()

    def destroy(self):
        super().destroy()
        for it in self.components:
            it.destroy()

    def on_error_cb(self, tpc_base, exception):
        #print(' wakeup error: ', str(exception))
        check_component = self.get_component('wakeup_check_component')
        if check_component :
            check_component.is_client_good = False

    def on_connected_cb(self, tcp_base):
        print('wakeup : connected!')
        check_component = self.get_component('wakeup_check_component')
        if check_component:
            check_component.is_client_good = True

    def send_close_cmd(self):
        client_component = self.get_component('net_client_component')
        if client_component :
            msg = net_protocol_component.net_protocol_component.event_name['close'] + '!'
            print('WAKEUP send close cmd', msg)
            client_component.send(msg)

    def on_reset(self):
        client_component = self.get_component('net_client_component')
        if client_component :
            print('closing')
            client_component.close()
            client_component.connect()
            print('reconnect !!')



