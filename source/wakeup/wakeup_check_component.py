from models import base
from models import ticker
import time

class wakeup_check_component( base.base):
    def __init__(self, controller, limit_time):
        super().__init__()
        self.controller = controller
        #self.limit_time = limit_time
        self.limit_time = 60
        self.is_enable = False
        self.is_client_good = False
        self.check_ticker = ticker.ticker(5)
        self.last_arrive_time = 0


    def initialize(self):
        super().register()
        component = self.controller.get_component('net_protocol_component')
        if component :
            component.register_event(component.event_name['arrive'], self.on_arrive)

    def destroy(self):
        super().destroy()
        component = self.controller.get_component('net_protocol_component')
        if component :
            component.unregister_event(component.event_name['arrive'], self.on_arrive)


    def tick(self, delta_time):
        if self.is_client_good and self.is_enable :
            if self.check_ticker.tick(delta_time) and time.time() - self.last_arrive_time > self.limit_time:
                #to do somethine
                self.awake_itchat()


    def on_arrive(self, tcp_base, data):
        #data Z: key!time
        self.last_arrive_time = float(data)
        print('last arrive time : ', self.last_arrive_time)

    def awake_itchat(self):
        print('need to awake')
        pass

    def on_now_state(self, data):
        if data == 'logging':
            self.is_enable = True
        else :
            self.is_enable = False

        print(' on now state : ', self.is_enable)