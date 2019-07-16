from models import base
class base_controller(base.base):
    def __init__(self):
        super().__init__()
        self.components = []

    def initialize(self):
        pass

    def destroy(self):
        super().destroy()


    def get_component(self, component_name):
        for it in self.components :
            if type(it).__name__ == component_name :
                return it
        return None