
import tick_controller
from models import input_manager
class world_controller:
    
    def __init__(self) :
        self.v_tick_controller = tick_controller.tick_controller()
        self.v_input_manager = input_manager.input_manager()

    def initialize(self):
        #initialize all things here
        self.v_tick_controller.initialize()
        self.v_input_manager.initialize()
        self.v_input_manager.after_input_call_back = self.is_end

    def destroy(self):
        self.v_tick_controller.destroy()
        self.v_input_manager.destroy()

    def update(self, delta_time):
        self.v_tick_controller.tick(delta_time)

    def is_end(self):
        if self.v_input_manager.last_input == '0' :
            self.v_input_manager.set_should_end(True)
            return True
        return False

