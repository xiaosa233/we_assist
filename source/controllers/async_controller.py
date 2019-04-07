from models import task_deque
import base_controller

class async_controller (base_controller.base_controller):
    def __init__(self):
        super().__init__()
        self.async_task = task_deque.async_task()

    def initialize(self):
        super().initialize()
        self.async_task.start()

    def destroy(self):
        super().destroy()
        self.async_task.stop(3)

    def get_async_task(self):
        return self.async_task
