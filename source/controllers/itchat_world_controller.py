from controllers import world_controller
import itchat_controller


class itchat_world_controller(world_controller.world_controller) :

    def __init__(self):
        super().__init__()
        self.v_itchat = itchat_controller.itchat_controller()


    def initialize(self, sys_argv):
        super().initialize(sys_argv)
        # now i don wanna to deal with system args
        self.v_itchat.start()

    def destroy(self):
        super().destroy()
        self.v_itchat.close()
