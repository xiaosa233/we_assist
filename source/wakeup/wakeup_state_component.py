from models import base
from enum import Enum
from models import ticker
from modules.io_mod.net_protocol_component import net_protocol_component
from utils.function_dispatcher import function_dispatcher
'''
ask for initialize state : no_response before_logging logging stop
register for state 
'''

class ewakeup(Enum):
    unvalid = 0
    ask_now_state = 1
    idle = 2
    before_logging = 3
    logging = 4
    stop = 5


class wakeup_state_component(base.base):

    g_state_map = { 'before_logging' : ewakeup.before_logging,
                    'logging' : ewakeup.logging,
                    'stop' : ewakeup.stop}

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.state = ewakeup.unvalid
        self.ask_ticker = ticker.ticker(1) #1second
        self.main_pid = -1
        self.pid_getter = ticker.ticker(10)
        function_dispatcher.open()['reset'].add(self.on_reset)


    def initialize(self):
        super().register()
        component = self.controller.get_component('net_protocol_component')
        if component :
            component.register_event(component.event_name['asw_state'], self.on_now_state)
            component.register_event(component.event_name['asw_pid'], self.on_pid)

        self.state = ewakeup.ask_now_state

    def destroy(self):
        super().destroy()
        component = self.controller.get_component('net_protocol_component')
        if component :
            component.unregister_event(component.event_name['asw_state'], self.on_now_state)
            component.unregister_event(component.event_name['asw_pid'], self.on_pid)

    def get_pid(self):
        return self.main_pid


    def on_now_state(self, tcp_base, data):
        print(' recv data ', data)
        if data in self.g_state_map :
            self.state = self.g_state_map[data]

        component = self.controller.get_component('wakeup_check_component')
        if component :
            component.on_now_state(data)

    def on_pid(self, tcp_base, data):
        print('recv pid = ', data)
        self.main_pid = int(data)

    def on_reset(self) :
        self.state = ewakeup.unvalid
        self.main_pid = -1

    def tick(self, delta_time):
        if self.state == ewakeup.ask_now_state and self.ask_ticker.tick(delta_time) :
            self.ask_now_state()

        if self.main_pid == -1 and self.pid_getter.tick(delta_time) :
            self.ask_pid()


    def ask_pid(self):
        component = self.controller.get_component('net_client_component')
        if component :
            msg = net_protocol_component.event_name['ask_pid'] + '!'
            component.send(msg)

    def ask_now_state(self):
        component = self.controller.get_component('net_client_component')
        if component :
            msg = net_protocol_component.event_name['ask_state']+'!'
            component.send(msg)