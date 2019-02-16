
import tick_controller
import input_manager
from utils import function_dispatcher

class world_controller:
    
    def __init__(self) :
        self.v_tick_controller = tick_controller.tick_controller()
        self.v_input_manager = input_manager.input_manager()
        self.should_end = False
        self.input_dispatcher = None

    def initialize(self, sys_argv):
        #initialize all things here
        self.input_dispatcher = function_dispatcher.function_dispatcher.open('input')
        self.input_dispatcher ['exit'].add(self.on_input_event_exit)
        self.v_tick_controller.initialize()
        self.v_input_manager.initialize()

    def destroy(self):
        self.v_tick_controller.destroy()
        self.v_input_manager.destroy()
        if self.input_dispatcher is not None :
            function_dispatcher.function_dispatcher.close(self.input_dispatcher.name)

    def update(self, delta_time):
        self.v_input_manager.deal_with_input()
        self.v_tick_controller.do_ticks(delta_time)

    def is_end(self):
        return self.should_end

    def on_input_event_exit(self):
        self.should_end = True