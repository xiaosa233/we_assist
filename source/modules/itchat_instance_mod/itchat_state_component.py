import itchat_base_component
from utils import function_dispatcher
class itchat_state_component(itchat_base_component.itchat_base_component):

    def __init__(self, outer):
        super().__init__()
        self.outer = outer
        self.dispatcher = function_dispatcher.function_dispatcher.open()
        self.dispatcher['ask_now_state'].add(self.on_ask_state)
        self.now_state = 'before_logging'

    def on_close(self):
        super().on_close()
        self.now_state = 'stop'
        self.update_state()
        self.dispatcher['ask_now_state'].remove(self.on_ask_state)

    def on_start(self):
        super().on_start()
        self.now_state = 'before_logging'
        self.update_state()


    def on_login(self):
        super().on_login()
        self.now_state = 'logging'
        self.update_state()

    def on_ask_state(self, out_data):
        out_data.append(self.now_state)

    def update_state(self):
        self.dispatcher['update_state'](self.now_state)
