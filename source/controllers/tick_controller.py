from models.base import *
from utils.function_dispatcher import *
class tick_controller:
    def __init__(self):
        self.tick_objs = []
        function_dispatcher.open()[base.g_base_creation_name].add(self.on_base_creation)
        function_dispatcher.open()[base.g_base_destroy_name].add(self.on_base_destroy)


    def on_base_creation(self, base_obj):
        if base_obj.is_tick and base_obj not in self.tick_objs:
            self.tick_objs.append(base_obj)

    def on_base_destroy(self, base_obj):
        if base_obj in self.tick_objs:
            self.tick_objs.remove(base_obj)