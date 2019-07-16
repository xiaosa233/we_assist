from controllers import world_controller
import net_controller
import itchat_controller

from models.global_accessor import global_accessor
class itchat_world_controller(world_controller.world_controller) :

    def __init__(self):
        super().__init__()
        self.v_itchat = itchat_controller.itchat_controller()
        self.v_net_controller = net_controller.net_controller()
        global_accessor.set_value('net_controller', self.v_net_controller)


    def initialize(self, sys_argv):
        super().initialize(sys_argv)
        # now i don wanna to deal with system args
        self.v_itchat.start()
        self.v_net_controller.initialize()

    def destroy(self):
        super().destroy()
        self.v_itchat.close()
        self.v_net_controller.destroy()
