from models import input_handler
from utils import function_dispatcher
class input_manager:
    def __init__(self):
        self.v_input_handle = input_handler.input_handler()
        self.input_dispatcher = None


    def initialize(self):
        self.v_input_handle.after_input_call_back = self.on_after_input
        self.input_dispatcher = function_dispatcher.function_dispatcher.open('input')
        self.v_input_handle.initialize()

    def destroy(self):
        self.v_input_handle.destroy()
        if self.input_dispatcher is not None :
            function_dispatcher.function_dispatcher.close(self.input_dispatcher.name)

    def on_after_input(self):
        if self.v_input_handle.get_last_input() == '0' :
            self.v_input_handle.set_should_end(True)


    def deal_with_input(self):
        last_input = self.v_input_handle.get_reset_last_input()
        if self.input_dispatcher is not None :
            if last_input == '0':
                self.input_dispatcher['exit']()
