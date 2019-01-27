from utils.function_dispatcher import *
#todo : maybe can add property  base.name
class base :
    g_base_creation_name = 'base_creation'
    g_base_destroy_name = 'base_destroy'
    def __init__(self):
        self.__is_tick = False
        function_dispatcher.open()[base.g_base_creation_name](self)

    def register(self):
        function_dispatcher.open()[base.g_base_creation_name](self)

    def destroy(self):
        function_dispatcher.open()[base.g_base_destroy_name](self)

    @property
    def is_tick(self):
        return self.__is_tick

    @is_tick.getter
    def is_tick(self):
        return self.__is_tick

    @is_tick.setter
    def is_tick(self, in_tick):
        self.__is_tick = in_tick