from controllers import world_controller
import wakeup_net_controller

class wakeup_world_controller(world_controller.world_controller) :

    def __init__(self):
        super().__init__()
        self.v_net_controller = wakeup_net_controller.wakeup_net_controller()


    def initialize(self, sys_argv):
        super().initialize(sys_argv)
        self.v_net_controller.initialize()

    def destroy(self):
        super().destroy()
        self.v_net_controller.destroy()
