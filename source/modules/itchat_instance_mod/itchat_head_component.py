import itchat_base_component
from models import json_object
from models import task_deque
class itchat_head_component(itchat_base_component.itchat_base_component) :
    def __init__(self, in_outer) :
        super().__init__()
        self.outer = in_outer
        self.last_head_index = 0
        self.task_component = None

    def on_login(self):
        self.last_head_index = json_object.json_object.parse_with_file(self.get_cache_json(), 'last_head_index')
        pass


    def update_head_image(self):
        if self.task_component :
            self.task_component.add_task( task_deque.task_unit(self.update_head_image_impl))


    def clear_old_heads(self):
        
        pass


    def tick(self, delta_time):
        self.update_head_image()


    def update_head_image_impl(self):

    def on_start(self):
        self.register()
        self.task_component = self.outer.get_component('itchat_task_component')

    def on_close(self):
        pass




    def get_cache_json(self) :
        return self.outer.get_itchat_data_dir() + 'cache.json'

    def get_head_dir(self, index):
        return self.outer.get_itchat_data_dir() + 'head_imgs/' + str(index) + '/'