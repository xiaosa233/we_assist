from utils.function_dispatcher import *
#todo : maybe can add property  base.name
class base :
    g_base_register_name = 'base_register'
    g_base_destroy_name = 'base_destroy'
    g_function_dispatcher = None
    def __init__(self):
        self.__is_tick = False
        self.__is_pending_kill = False
        if base.g_function_dispatcher is None :
            base.g_function_dispatcher = function_dispatcher.open()

    def register(self):
        base.g_function_dispatcher[base.g_base_register_name](self)

    def destroy(self):
        base.g_function_dispatcher[base.g_base_destroy_name](self)

    #virtual
    def tick(self, delta_time):
        pass

    @property
    def is_tick(self):
        return self.__is_tick
    @is_tick.setter
    def is_tick(self, in_tick):
        self.__is_tick = in_tick

    @property
    def is_pending_kill(self):
        return self.__is_pending_kill
    @is_pending_kill.setter
    def is_pending_kill(self, b_pending_kill):
        self.__is_pending_kill = b_pending_kill